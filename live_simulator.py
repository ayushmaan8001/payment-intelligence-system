import requests
import random
import time
from datetime import datetime

API_URL = "http://127.0.0.1:8001/api/transaction"

PAYMENT_METHODS = ["UPI", "Card", "Wallet"]
GATEWAYS = ["GW_A", "GW_B", "GW_C"]
FAILURE_REASONS = [
    "INSUFFICIENT_FUNDS", "NETWORK_TIMEOUT",
    "GATEWAY_ERROR", "BANK_DECLINED",
    "LIMIT_EXCEEDED", "FRAUD_FLAGGED"
]

METHOD_FAILURE_RATE = {"UPI": 0.10, "Card": 0.08, "Wallet": 0.05}

def generate_transaction():
    method = random.choices(PAYMENT_METHODS, weights=[0.50, 0.30, 0.20])[0]
    gateway = random.choice(GATEWAYS)
    amount = round(random.uniform(50, 5000), 2)
    hour = datetime.now().hour

    failure_rate = METHOD_FAILURE_RATE[method]
    if 20 <= hour <= 21:
        failure_rate = min(failure_rate * 1.8, 0.40)
    if gateway == "GW_C":
        failure_rate = min(failure_rate * 1.3, 0.45)

    failed = random.random() < failure_rate

    return {
        "user_id": random.randint(1001, 1500),
        "merchant_id": random.randint(2001, 2050),
        "amount": amount,
        "payment_method": method,
        "gateway": gateway,
        "status": "failure" if failed else "success",
        "failure_reason": random.choice(FAILURE_REASONS) if failed else "NONE",
        "retry_count": 0,
        "attempt_number": 1,
        "latency_ms": random.randint(700, 1500) if failed else random.randint(200, 500)
    }

def run():
    print("Live simulator started — sending transactions every 2 seconds")
    print("Press Ctrl+C to stop\n")
    count = 0
    while True:
        txn = generate_transaction()
        try:
            response = requests.post(API_URL, json=txn)
            data = response.json()
            count += 1
            risk = data['ml_prediction']['risk_level']
            prob = data['ml_prediction']['failure_probability']
            print(f"[{count}] {txn['payment_method']} | {txn['gateway']} | ₹{txn['amount']} | {txn['status'].upper()} | Risk: {risk} ({prob})")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(2)

if __name__ == "__main__":
    run()