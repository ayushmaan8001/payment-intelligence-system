import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# ─── Seed for reproducibility ───────────────────────────────────────────────
random.seed(42)
np.random.seed(42)

# ─── Configuration ───────────────────────────────────────────────────────────
NUM_TRANSACTIONS = 100000
SIMULATION_DAYS  = 30
START_DATE       = datetime(2025, 1, 1)
OUTPUT_PATH      = r"D:\projects\payment-intelligence-system\transactions.csv"

# ─── Reference Data ──────────────────────────────────────────────────────────
PAYMENT_METHODS  = ["UPI", "Card", "Wallet"]
GATEWAYS         = ["GW_A", "GW_B", "GW_C"]
FAILURE_REASONS  = [
    "INSUFFICIENT_FUNDS", "NETWORK_TIMEOUT",
    "GATEWAY_ERROR", "BANK_DECLINED",
    "LIMIT_EXCEEDED", "FRAUD_FLAGGED"
]

# Failure probability per payment method (base rate)
METHOD_FAILURE_RATE = {
    "UPI":    0.10,
    "Card":   0.08,
    "Wallet": 0.05
}

# Failure reason weights per method
METHOD_FAILURE_REASONS = {
    "UPI":    [0.10, 0.40, 0.25, 0.10, 0.10, 0.05],
    "Card":   [0.35, 0.15, 0.15, 0.20, 0.10, 0.05],
    "Wallet": [0.15, 0.25, 0.30, 0.15, 0.10, 0.05]
}

# Retry success probability per failure reason
RETRY_SUCCESS_PROB = {
    "INSUFFICIENT_FUNDS": 0.08,
    "NETWORK_TIMEOUT":    0.65,
    "GATEWAY_ERROR":      0.55,
    "BANK_DECLINED":      0.10,
    "LIMIT_EXCEEDED":     0.05,
    "FRAUD_FLAGGED":      0.02
}

# ─── Helper: generate realistic timestamp ────────────────────────────────────
def random_timestamp(base_date):
    day_offset = random.randint(0, SIMULATION_DAYS - 1)
    dt = base_date + timedelta(days=day_offset)

    # Peak hour weighting: 8PM-10PM gets 3x more traffic
    hour_weights = [1]*8 + [1.5]*10 + [3]*2 + [1.5]*2 + [1]*2
    hour = random.choices(range(24), weights=hour_weights)[0]
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    return dt.replace(hour=hour, minute=minute, second=second)

# ─── Helper: is peak hour ────────────────────────────────────────────────────
def is_peak_hour(ts):
    return 20 <= ts.hour <= 21

# ─── Main Simulator ──────────────────────────────────────────────────────────
def simulate():
    rows = []
    transaction_id = 1

    # Pre-generate user and merchant pools
    user_ids     = list(range(1001, 1501))   # 500 users
    merchant_ids = list(range(2001, 2051))   # 50 merchants

    for _ in range(NUM_TRANSACTIONS):
        user_id     = random.choice(user_ids)
        merchant_id = random.choice(merchant_ids)
        amount      = round(random.uniform(50, 5000), 2)
        method      = random.choices(
                          PAYMENT_METHODS,
                          weights=[0.50, 0.30, 0.20]
                      )[0]
        gateway     = random.choice(GATEWAYS)
        ts          = random_timestamp(START_DATE)

        # Failure rate increases during peak hours
        failure_rate = METHOD_FAILURE_RATE[method]
        if is_peak_hour(ts):
            failure_rate = min(failure_rate * 1.8, 0.40)

        # Gateway C is less reliable
        if gateway == "GW_C":
            failure_rate = min(failure_rate * 1.3, 0.45)

        failed = random.random() < failure_rate

        if not failed:
            # Direct success
            latency = random.randint(200, 500)
            rows.append({
                "transaction_id": transaction_id,
                "user_id":        user_id,
                "merchant_id":    merchant_id,
                "amount":         amount,
                "payment_method": method,
                "gateway":        gateway,
                "status":         "success",
                "failure_reason": None,
                "retry_count":    0,
                "attempt_number": 1,
                "timestamp":      ts,
                "latency_ms":     latency
            })
            transaction_id += 1

        else:
            # First attempt — failure
            failure_reason = random.choices(
                FAILURE_REASONS,
                weights=METHOD_FAILURE_REASONS[method]
            )[0]
            latency = random.randint(700, 1500)

            rows.append({
                "transaction_id": transaction_id,
                "user_id":        user_id,
                "merchant_id":    merchant_id,
                "amount":         amount,
                "payment_method": method,
                "gateway":        gateway,
                "status":         "failure",
                "failure_reason": failure_reason,
                "retry_count":    0,
                "attempt_number": 1,
                "timestamp":      ts,
                "latency_ms":     latency
            })

            # Retry logic — max 3 retries
            retry_success_prob = RETRY_SUCCESS_PROB[failure_reason]
            max_retries = 3
            retry_count = 0
            succeeded_after_retry = False

            for attempt in range(2, max_retries + 2):
                retry_count += 1
                retry_ts = ts + timedelta(seconds=random.randint(30, 90))

                if random.random() < retry_success_prob:
                    # Retry succeeded
                    rows.append({
                        "transaction_id": transaction_id,
                        "user_id":        user_id,
                        "merchant_id":    merchant_id,
                        "amount":         amount,
                        "payment_method": method,
                        "gateway":        gateway,
                        "status":         "success",
                        "failure_reason": None,
                        "retry_count":    retry_count,
                        "attempt_number": attempt,
                        "timestamp":      retry_ts,
                        "latency_ms":     random.randint(200, 600)
                    })
                    succeeded_after_retry = True
                    break
                else:
                    # Retry also failed
                    rows.append({
                        "transaction_id": transaction_id,
                        "user_id":        user_id,
                        "merchant_id":    merchant_id,
                        "amount":         amount,
                        "payment_method": method,
                        "gateway":        gateway,
                        "status":         "failure",
                        "failure_reason": failure_reason,
                        "retry_count":    retry_count,
                        "attempt_number": attempt,
                        "timestamp":      retry_ts,
                        "latency_ms":     random.randint(700, 1500)
                    })

                if retry_count >= max_retries:
                    break

            transaction_id += 1

    df = pd.DataFrame(rows)
    df.sort_values("timestamp", inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Done. {len(df)} rows generated.")
    print(f"Saved to: {OUTPUT_PATH}")
    print(f"\nQuick stats:")
    print(df["status"].value_counts())
    print(f"\nFailure by method:")
    print(df[df["status"]=="failure"]["payment_method"].value_counts())

# ─── Run ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    simulate()