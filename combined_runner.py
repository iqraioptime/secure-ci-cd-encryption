import subprocess

print("Running AES Encryption/Decryption Test:")
subprocess.run(["python", "aes_encrypt.py"])

print("\nRunning Paillier Encryption/Decryption Test:")
subprocess.run(["python", "paillier_encrypt.py"])