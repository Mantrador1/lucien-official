import json
from eth_account import Account
from cryptography.fernet import Fernet

def generate_wallets(n):
    wallets = []
    for _ in range(n):
        acct = Account.create()
        wallets.append({
            'address': acct.address,
            'private_key': acct.key.hex()
        })
    return wallets

def save_encrypted_wallets(wallets, filename, key):
    from cryptography.fernet import Fernet
    fernet = Fernet(key)
    data = json.dumps(wallets).encode()
    encrypted = fernet.encrypt(data)
    with open(filename, 'wb') as f:
        f.write(encrypted)

if __name__ == '__main__':
    import os
    n = 100
    key_file = 'wallet_key.key'
    wallets_file = 'wallets.enc'

    if not os.path.exists(key_file):
        key = Fernet.generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)
    else:
        with open(key_file, 'rb') as f:
            key = f.read()

    wallets = generate_wallets(n)
    save_encrypted_wallets(wallets, wallets_file, key)
    print(f'{n} wallets generated and saved encrypted in {wallets_file}')





