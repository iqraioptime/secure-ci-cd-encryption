from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import time
import csv
import numpy as np
import matplotlib.pyplot as plt

# Read Debit, Credit, and Balance columns from CSV
debits = []
credits = []
balances = []

with open('bank.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            debits.append(float(row['Debit'].replace(",", "").replace(" ", "")) if row['Debit'] else 0.0)
            credits.append(float(row['Credit'].replace(",", "").replace(" ", "")) if row['Credit'] else 0.0)
            balances.append(float(row['Balance'].replace(",", "").replace(" ", "")) if row['Balance'] else 0.0)
        except ValueError:
            continue

# Generate AES key
key = os.urandom(32)  # 256-bit key
iv = os.urandom(16)   # 128-bit IV

backend = default_backend()
cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)

encryptor = cipher.encryptor()
decryptor = cipher.decryptor()

# Prepare data
data = ",".join(
    [f"{debit},{credit},{balance}" for debit, credit, balance in zip(debits, credits, balances)]
).encode()

# Encrypt
start_encrypt = time.perf_counter()
ciphertext = encryptor.update(data) + encryptor.finalize()
end_encrypt = time.perf_counter()

# Decrypt
start_decrypt = time.perf_counter()
plaintext = decryptor.update(ciphertext) + decryptor.finalize()
end_decrypt = time.perf_counter()

# Results
encryption_time_ms = (end_encrypt - start_encrypt) * 1000
decryption_time_ms = (end_decrypt - start_decrypt) * 1000

print(f"AES Encryption Time: {encryption_time_ms:.6f} ms")
print(f"AES Decryption Time: {decryption_time_ms:.6f} ms")

# Plotting functions

def plot_encryption_decryption_times():
    # First Graph (Thin Bars)
    times = {
        "Encryption Time (ms)": encryption_time_ms,
        "Decryption Time (ms)": decryption_time_ms
    }
    
    plt.figure(figsize=(1,6))
    plt.bar(times.keys(), times.values(), width=0.2, color=['blue', 'orange'])  # <--- THIN bar (width=0.3)
    
    plt.ylabel("Time (Milliseconds)")
    plt.xlabel("AES Encryption and Decryption Times")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_encryption_decryption_times_detailed():
    # Second Graph (Comparison - Thin Bars)
    labels = ['Encryption', 'Decryption']
    times = [encryption_time_ms, decryption_time_ms]

    x = np.arange(len(labels))
    bar_width = 0.25  # <--- THINNER bars

    plt.figure(figsize=(8, 5))

    plt.bar(x, times, width=bar_width, color=['purple', 'cyan'])

    plt.xlabel('Operation')
    plt.ylabel('Execution Time (Milliseconds)')
    plt.xticks(x, labels)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Call the plotting functions
plot_encryption_decryption_times()          # First thin chart
plot_encryption_decryption_times_detailed() # Second thin chart
