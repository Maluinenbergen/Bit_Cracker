import secrets
import hashlib
import base58
import ecdsa

def generate_private_key():
    private_key_bytes = secrets.token_bytes(32)
    private_key_hex = private_key_bytes.hex()
    extended_key = b'\x80' + private_key_bytes
    first_sha = hashlib.sha256(extended_key).digest()
    second_sha = hashlib.sha256(first_sha).digest()
    checksum = second_sha[:4]
    final_key = extended_key + checksum
    wif = base58.b58encode(final_key).decode('utf-8')
    return private_key_hex, wif

def private_key_to_public_key(private_key_hex):
    private_key_bytes = bytes.fromhex(private_key_hex)
    sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    public_key_bytes = b'\x04' + vk.to_string()
    return public_key_bytes.hex()

def public_key_to_address(public_key_hex):
    public_key_bytes = bytes.fromhex(public_key_hex)
    sha256_hash = hashlib.sha256(public_key_bytes).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256_hash)
    hashed_public_key = ripemd160.digest()
    network_byte = b'\x00' + hashed_public_key
    first_sha = hashlib.sha256(network_byte).digest()
    second_sha = hashlib.sha256(first_sha).digest()
    checksum = second_sha[:4]
    binary_address = network_byte + checksum
    address = base58.b58encode(binary_address).decode('utf-8')
    return address