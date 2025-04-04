import os
from bitcoinlib.wallets import Wallet as BitcoinWallet
from web3 import Web3
from solana.keypair import Keypair as SolanaKeypair
from mnemonic import Mnemonic
import time

w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))
# Untuk BNB

# Daftar blockchain yang didukung
blockchains = {
    "1": "bitcoin",
    "2": "ethereum",
    "3": "solana",
    "4": "bnb"
}

# Fungsi untuk membuat folder jika belum ada
def create_folder(blockchain_name):
    if not os.path.exists(blockchain_name):
        os.makedirs(blockchain_name)

# Fungsi untuk menyimpan data ke file terpisah tanpa label
def save_to_files(address, private_key, mnemonic, blockchain_name):
    create_folder(blockchain_name)
    with open(os.path.join(blockchain_name, "yuri_address.txt"), "a") as f_addr:
        f_addr.write(f"{address}\n")
    with open(os.path.join(blockchain_name, "yuuri_privatekeys.txt"), "a") as f_pk:
        f_pk.write(f"{private_key}\n")
    with open(os.path.join(blockchain_name, "yuuri_phrase.txt"), "a") as f_mn:
        f_mn.write(f"{mnemonic}\n")

# Fungsi generate wallet
def generate_wallet(blockchain_name, index):
    mnemo = Mnemonic("english")
    seed = mnemo.generate(strength=256)
    
    if blockchain_name == "bitcoin":
        wallet = BitcoinWallet.create(f"btc_wallet_{int(time.time())}_{index}", keys=seed, network="bitcoin")
        address = wallet.get_key().address
        private_key = wallet.get_key().wif
        return address, private_key, seed
    
    elif blockchain_name == "ethereum":
        account = w3.eth.account.create()
        private_key = account._private_key.hex()  # Diperbaiki: gunakan _private_key
        return account.address, private_key, "Not natively provided by Web3.py"
    
    elif blockchain_name == "solana":
        keypair = SolanaKeypair()
        return str(keypair.public_key), keypair.secret_key.hex(), seed
    
    elif blockchain_name == "bnb":
        account = w3.eth.account.create()
        private_key = account._private_key.hex()  # Diperbaiki: gunakan _private_key
        return account.address, private_key, "Not natively provided by Web3.py"

# Fungsi utama
def main():
    print("Pilih blockchain untuk membuat wallet:")
    for key, value in blockchains.items():
        print(f"{key}. {value.capitalize()}")
    
    choice = input("Masukkan nomor blockchain (1-4): ")
    if choice not in blockchains:
        print("Pilihan tidak valid!")
        return
    
    blockchain_name = blockchains[choice]
    try:
        jumlah = int(input("Masukkan jumlah wallet yang ingin dibuat: "))
        if jumlah <= 0:
            raise ValueError
    except ValueError:
        print("Jumlah harus berupa angka positif!")
        return
    
    # Generate dan simpan wallet
    for i in range(jumlah):
        address, private_key, mnemonic = generate_wallet(blockchain_name, i)
        save_to_files(address, private_key, mnemonic, blockchain_name)
        print(f"Wallet {i+1} untuk {blockchain_name.capitalize()} telah dibuat.")
    
    print(f"Selesai! {jumlah} wallet untuk {blockchain_name.capitalize()} telah dibuat di folder {blockchain_name}/")

if __name__ == "__main__":
    main()
