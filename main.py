import sys
import time
import requests
import secrets
import hashlib
import base58
import threading
from concurrent.futures import ThreadPoolExecutor
import numpy as np

try:
    from numba import cuda
    CUDA_AVAILABLE = cuda.is_available()
except ImportError:
    CUDA_AVAILABLE = False

from crypto_utils import generate_private_key, private_key_to_public_key, public_key_to_address

API_URL = "https://blockchain.info/balance?active="
BATCH_SIZE = 64 if CUDA_AVAILABLE else 32
THREADS = 4

def check_balance(address):
    try:
        response = requests.get(API_URL + address, timeout=5)
        if response.status_code == 200:
            data = response.json()
            satoshi = data.get(address, {}).get('final_balance', 0)
            btc = satoshi / 100_000_000.0
            return btc
        else:
            return 0.0
    except Exception:
        return 0.0

def generate_batch_cpu(count):
    batch = []
    for _ in range(count):
        private_hex, wif = generate_private_key()
        pub_key = private_key_to_public_key(private_hex)
        address = public_key_to_address(pub_key)
        batch.append((private_hex, wif, pub_key, address))
    return batch

def cpu_worker(stats):
    while True:
        private_hex, wif, pub_key, address = generate_batch_cpu(1)[0]
        balance = check_balance(address)
        with stats['lock']:
            stats['attempts'] += 1
            attempts = stats['attempts']
        status_line = f"Attempt: {attempts} | Address: {address} | Balance: {balance:.8f} BTC"
        print(status_line, end='\r')
        if balance > 0.0:
            with stats['lock']:
                print("\n" + "!" * 60)
                print("FOUND NON-ZERO BALANCE")
                print(f"Private HEX: {private_hex}")
                print(f"Private WIF: {wif}")
                print(f"Public Key: {pub_key}")
                print(f"Address: {address}")
                print(f"Balance: {balance:.8f} BTC")
                print("!" * 60 + "\n")
                with open("found.txt", "a") as f:
                    f.write(f"Address: {address}\n")
                    f.write(f"Private HEX: {private_hex}\n")
                    f.write(f"Private WIF: {wif}\n")
                    f.write(f"Balance: {balance:.8f} BTC\n")
                    f.write("-" * 40 + "\n")

@cuda.jit
def gpu_generate_keys(rng_states, priv_keys, pub_keys_x, pub_keys_y):
    idx = cuda.grid(1)
    if idx < priv_keys.shape[0]:
        state = rng_states[idx]
        for i in range(32):
            a = cuda.random.xoroshiro128p_next_uint64(state)
            priv_keys[idx, i] = cuda.byte(a & 0xFF)
        rng_states[idx] = state

def gpu_worker(stats):
    import ecdsa
    threads_per_block = 256
    blocks = (BATCH_SIZE + threads_per_block - 1) // threads_per_block
    rng_states = cuda.random.create_xoroshiro128p_states(BATCH_SIZE, seed=secrets.randbits(64))
    d_priv_keys = cuda.device_array((BATCH_SIZE, 32), dtype=np.uint8)
    while True:
        gpu_generate_keys[blocks, threads_per_block](rng_states, d_priv_keys)
        cuda.synchronize()
        priv_keys_host = d_priv_keys.copy_to_host()
        for i in range(BATCH_SIZE):
            private_key_bytes = bytes(priv_keys_host[i])
            private_key_hex = private_key_bytes.hex()
            sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
            vk = sk.get_verifying_key()
            public_key_bytes = b'\x04' + vk.to_string()
            pub_key = public_key_bytes.hex()
            address = public_key_to_address(pub_key)
            wif_raw = b'\x80' + private_key_bytes
            sha = hashlib.sha256(wif_raw).digest()
            sha2 = hashlib.sha256(sha).digest()
            wif = base58.b58encode(wif_raw + sha2[:4]).decode()
            balance = check_balance(address)
            with stats['lock']:
                stats['attempts'] += 1
                attempts = stats['attempts']
            status_line = f"Attempt: {attempts} | Address: {address} | Balance: {balance:.8f} BTC"
            print(status_line, end='\r')
            if balance > 0.0:
                with stats['lock']:
                    print("\n" + "!" * 60)
                    print("FOUND NON-ZERO BALANCE")
                    print(f"Private HEX: {private_key_hex}")
                    print(f"Private WIF: {wif}")
                    print(f"Public Key: {pub_key}")
                    print(f"Address: {address}")
                    print(f"Balance: {balance:.8f} BTC")
                    print("!" * 60 + "\n")
                    with open("found.txt", "a") as f:
                        f.write(f"Address: {address}\n")
                        f.write(f"Private HEX: {private_key_hex}\n")
                        f.write(f"Private WIF: {wif}\n")
                        f.write(f"Balance: {balance:.8f} BTC\n")
                        f.write("-" * 40 + "\n")

def main():
    print("=" * 50)
    print("Bitcoin Key Seeker (Educational Only)")
    print("=" * 50)
    stats = {'attempts': 0, 'lock': threading.Lock()}
    if CUDA_AVAILABLE:
        print("GPU (CUDA) mode active.")
        try:
            gpu_worker(stats)
        except KeyboardInterrupt:
            print("\nStopped.")
    else:
        print("CPU mode active (multithreaded).")
        with ThreadPoolExecutor(max_workers=THREADS) as executor:
            futures = [executor.submit(cpu_worker, stats) for _ in range(THREADS)]
            try:
                while True:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                print("\nStopping threads...")
                for f in futures:
                    f.cancel()
        print(f"Total attempts: {stats['attempts']}")

if __name__ == "__main__":
    main()