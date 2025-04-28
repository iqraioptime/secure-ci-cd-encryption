from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import time
import csv

# Read balances
balances = []
with open('bank.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        balances.append(int(row['balance']))

# Generate AES key
key = os.urandom(32)  # 256-bit key
iv = os.urandom(16)   # 128-bit IV

backend = default_backend()
cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)

encryptor = cipher.encryptor()
decryptor = cipher.decryptor()

# Prepare data (convert balances to bytes)
data = ",".join(map(str, balances)).encode()

# Encrypt
start_encrypt = time.perf_counter()  # Changed from time.time() to time.perf_counter()
ciphertext = encryptor.update(data) + encryptor.finalize()
end_encrypt = time.perf_counter()  # Changed from time.time() to time.perf_counter()

# Decrypt
start_decrypt = time.perf_counter()  # Changed from time.time() to time.perf_counter()
plaintext = decryptor.update(ciphertext) + decryptor.finalize()
end_decrypt = time.perf_counter()  # Changed from time.time() to time.perf_counter()

# Results
print(f"AES Encryption Time: {(end_encrypt - start_encrypt) * 1000:.6f} ms")  # Time in milliseconds
print(f"AES Decryption Time: {(end_decrypt - start_decrypt) * 1000:.6f} ms")  # Time in milliseconds
print(f"Original balances: {balances}")
print(f"Decrypted balances: {list(map(int, plaintext.decode().split(',')))}")
