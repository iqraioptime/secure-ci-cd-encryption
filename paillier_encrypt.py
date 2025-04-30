from phe import paillier
import csv
import time

# Function to convert strings with commas to float
def parse_money(value):
    return float(value.replace(',', '').replace(' ', ''))

# Read data from the CSV
debits = []
credits = []
balances = []

with open('bank.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Extract numeric values, convert them to floats
        if row['Debit']:  # Make sure there is a value in Debit
            debits.append(parse_money(row['Debit']))
        else:
            debits.append(0.0)  # If no debit value, assume 0

        if row['Credit']:  # Make sure there is a value in Credit
            credits.append(parse_money(row['Credit']))
        else:
            credits.append(0.0)  # If no credit value, assume 0

        if row['Balance']:  # Make sure there is a value in Balance
            balances.append(parse_money(row['Balance']))
        else:
            balances.append(0.0)  # If no balance value, assume 0

# Generate Paillier keypair
public_key, private_key = paillier.generate_paillier_keypair()

# Encrypt data
start_encrypt = time.time()

# Encrypt debits, credits, and balances
encrypted_debits = [public_key.encrypt(debit) for debit in debits]
encrypted_credits = [public_key.encrypt(credit) for credit in credits]
encrypted_balances = [public_key.encrypt(balance) for balance in balances]

end_encrypt = time.time()

# Decrypt data
start_decrypt = time.time()
decrypted_debits = [private_key.decrypt(enc) for enc in encrypted_debits]
decrypted_credits = [private_key.decrypt(enc) for enc in encrypted_credits]
decrypted_balances = [private_key.decrypt(enc) for enc in encrypted_balances]

end_decrypt = time.time()

# Results
print(f"Paillier Encryption Time: {end_encrypt - start_encrypt:.6f} seconds")
print(f"Paillier Decryption Time: {end_decrypt - start_decrypt:.6f} seconds")
#print(f"Original debits: {debits[:5]}")  # Print the first 5 values for debits
#print(f"Original credits: {credits[:5]}")  # Print the first 5 values for credits
#print(f"Original balances: {balances[:5]}")  # Print the first 5 values for balances
#print(f"Decrypted debits: {decrypted_debits[:5]}")
#print(f"Decrypted credits: {decrypted_credits[:5]}")
#print(f"Decrypted balances: {decrypted_balances[:5]}")

