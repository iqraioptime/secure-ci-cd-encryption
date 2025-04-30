import pandas as pd
import time
import psutil
import os
import matplotlib.pyplot as plt
from cryptography.fernet import Fernet
from phe import paillier

# Load dataset
dataset = pd.read_csv('bank.csv')

# Convert to numeric, remove commas if present
for col in ['Debit', 'Credit', 'Balance']:
    dataset[col] = dataset[col].apply(lambda x: float(str(x).replace(",", "").strip()) if isinstance(x, str) else float(x))

# Flatten values into one list
values = dataset[['Debit', 'Credit', 'Balance']].values.flatten().tolist()

# Limit values for Paillier (too slow on large sets)
aes_values = values
paillier_values = values[:100]  # Run only on 100 for faster processing

# Generate AES and Paillier keys
aes_key = Fernet.generate_key()
fernet = Fernet(aes_key)
pub_key, priv_key = paillier.generate_paillier_keypair()

print(f"\n🔐 AES Key: {aes_key.decode()}")
print(f"🔐 Paillier Public Key (n): {pub_key.n}")
print(f"🔐 Paillier Private Key (p, q): ({priv_key.p}, {priv_key.q})\n")  # Optional for educational view

# AES encryption/decryption
def aes_encrypt_decrypt(values):
    enc_times, dec_times = [], []
    for value in values:
        plaintext = str(value).encode()

        start = time.time()
        encrypted = fernet.encrypt(plaintext)
        enc_times.append(time.time() - start)

        start = time.time()
        decrypted = fernet.decrypt(encrypted).decode()
        dec_times.append(time.time() - start)

        assert decrypted == str(value)
    return sum(enc_times), sum(dec_times)

# Paillier encryption/decryption
def paillier_encrypt_decrypt(values):
    enc_times, dec_times = [], []
    for value in values:
        start = time.time()
        encrypted = pub_key.encrypt(value)
        enc_times.append(time.time() - start)

        start = time.time()
        decrypted = priv_key.decrypt(encrypted)
        dec_times.append(time.time() - start)

        assert abs(decrypted - value) < 0.01
    return sum(enc_times), sum(dec_times)

# Measure performance with CPU/memory
def measure(label, func):
    print(f"\n⏳ Running {label}...")
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / 1024 / 1024

    start = time.time()
    result = func()
    duration = time.time() - start

    mem_after = process.memory_info().rss / 1024 / 1024
    mem_used = max(0, mem_after - mem_before)  # Prevent negative
    cpu_usage = psutil.cpu_percent(interval=1.0)

    print(f"✅ {label} - Time: {duration:.4f}s, CPU: {cpu_usage:.2f}%, Mem Used: {mem_used:.2f} MB")
    return result, duration, cpu_usage, mem_used

# Run encryption/decryption for AES
(aes_enc_time, aes_dec_time), aes_total_time, aes_cpu, aes_mem = measure(
    "AES Encryption/Decryption",
    lambda: aes_encrypt_decrypt(aes_values)
)

# Run encryption/decryption for Paillier
(phe_enc_time, phe_dec_time), phe_total_time, phe_cpu, phe_mem = measure(
    "Paillier Encryption/Decryption",
    lambda: paillier_encrypt_decrypt(paillier_values)
)

# --- GRAPH 1: Encryption/Decryption Times ---
plt.figure(figsize=(10, 6))
plt.bar(['AES Encrypt', 'AES Decrypt', 'Paillier Encrypt', 'Paillier Decrypt'],
        [aes_enc_time, aes_dec_time, phe_enc_time, phe_dec_time],
        color=['blue', 'skyblue', 'green', 'lightgreen'])
plt.title('Encryption/Decryption Time Comparison (AES vs Paillier)')
plt.ylabel('Time (seconds)')
plt.xlabel('Operation')
plt.tight_layout()
plt.savefig("encryption_decryption_times.png")
plt.show()

# --- GRAPH 2: CPU and Memory Usage ---
labels = ['AES CPU %', 'AES Mem MB', 'Paillier CPU %', 'Paillier Mem MB']
values = [aes_cpu, aes_mem, phe_cpu, phe_mem]

plt.figure(figsize=(10, 6))
plt.bar(labels, values, color=['blue', 'skyblue', 'green', 'lightgreen'])
plt.title('CPU and Memory Usage Comparison')
plt.ylabel('Usage')
plt.xlabel('Metric')
plt.tight_layout()
plt.savefig("cpu_memory_usage.png")
plt.show()
