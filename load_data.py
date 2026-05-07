import os
import pandas as pd
import mysql.connector
from datetime import datetime

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.environ.get('DB_PASSWORD'),
    database="payment_intelligence"
)
cursor = conn.cursor()

# Load CSV
print("Loading CSV...")
df = pd.read_csv(r"D:\projects\payment-intelligence-system\transactions.csv")

# Replace NaN with None for MySQL
df = df.where(pd.notnull(df), None)

# Convert timestamp column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

print(f"Total rows to insert: {len(df)}")

# Insert rows in batches
batch_size = 1000
total = len(df)
inserted = 0

for i in range(0, total, batch_size):
    batch = df.iloc[i:i+batch_size]
    rows = []
    for _, row in batch.iterrows():
        rows.append((
            int(row['transaction_id']),
            int(row['user_id']),
            int(row['merchant_id']),
            float(row['amount']),
            str(row['payment_method']),
            str(row['gateway']),
            str(row['status']),
            row['failure_reason'] if row['failure_reason'] else None,
            int(row['retry_count']),
            int(row['attempt_number']),
            row['timestamp'],
            int(row['latency_ms'])
        ))

    cursor.executemany("""
        INSERT INTO transactions 
        (transaction_id, user_id, merchant_id, amount, payment_method, 
         gateway, status, failure_reason, retry_count, attempt_number, 
         timestamp, latency_ms)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, rows)
    conn.commit()
    inserted += len(batch)
    print(f"Inserted {inserted}/{total} rows...")

print("Done! All data loaded into MySQL.")
cursor.close()
conn.close()