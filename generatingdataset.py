import pandas as pd
import random
import string

# Function to generate a single random transaction
def random_transaction():
    date = pd.Timestamp('2024-11-01') + pd.Timedelta(days=random.randint(0, 100))
    debit = round(random.uniform(1000, 25000), 2)
    credit = round(random.uniform(0, 25000), 2)
    balance = round(random.uniform(10000, 500000), 2)
    return {
        'Date': date.strftime("%d %b %Y"),
        'Value Date': date.strftime("%d %b %Y"),
        'Instrument No.': ''.join(random.choices(string.digits, k=6)) if random.random() < 0.5 else "",
        'Particulars': random.choice([
            'Raast IBFT to IQRA PARVEEN', 'Raast IBFT to OMAR ZAMAN',
            'INET Inter Bank Fund Transfer Charges', 'Mobile App MARYAM BEGUM'
        ]),
        'Debit': debit,
        'Credit': credit,
        'Balance': balance
    }

# Generate 10,000 transactions and save to CSV
df = pd.DataFrame([random_transaction() for _ in range(10000)])
df.to_csv("full_transaction_dataset.csv", index=False)
print("Dataset saved as full_transaction_dataset.csv")
