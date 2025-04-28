from phe import paillier
import csv
import time

# Read balances
balances = []
with open('bank.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        balances.append(int(row['balance']))

# Generate Paillier keypair
public_key, private_key = paillier.generate_paillier_keypair()

# Encrypt balances
start_encrypt = time.time()
encrypted_balances = [public_key.encrypt(balance) for balance in balances]
end_encrypt = time.time()

# Decrypt balances
start_decrypt = time.time()
decrypted_balances = [private_key.decrypt(enc) for enc in encrypted_balances]
end_decrypt = time.time()

# Results
print(f"Paillier Encryption Time: {end_encrypt - start_encrypt:.6f} seconds")
print(f"Paillier Decryption Time: {end_decrypt - start_decrypt:.6f} seconds")
print(f"Original balances: {balances}")
print(f"Decrypted balances: {decrypted_balances}")

