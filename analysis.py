import os
import pandas as pd
from sqlalchemy import create_engine

# Database connection
db_password = "121212"
engine = create_engine(f"mysql+pymysql://root:{db_password}@localhost/payment_intelligence")

def run_query(query):
    return pd.read_sql(query, engine)

# ── 1. Overall Summary ────────────────────────────────────────────────────────
print("\n===== OVERALL SUMMARY =====")
summary = run_query("""
    SELECT 
        COUNT(*) AS total_rows,
        COUNT(DISTINCT transaction_id) AS unique_transactions,
        SUM(CASE WHEN status = 'success' AND retry_count = 0 THEN 1 ELSE 0 END) AS direct_success,
        SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) AS total_failures,
        SUM(CASE WHEN status = 'success' AND retry_count > 0 THEN 1 ELSE 0 END) AS success_after_retry,
        ROUND(SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS failure_rate_pct
    FROM transactions
""")
print(summary.to_string(index=False))

# ── 2. Failure by Payment Method ─────────────────────────────────────────────
print("\n===== FAILURE BY PAYMENT METHOD =====")
method_health = run_query("""
    SELECT 
        payment_method,
        COUNT(*) AS total,
        SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) AS failures,
        ROUND(SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS failure_pct,
        ROUND(AVG(latency_ms), 0) AS avg_latency_ms
    FROM transactions
    GROUP BY payment_method
    ORDER BY failure_pct DESC
""")
print(method_health.to_string(index=False))

# ── 3. Failure Reason Breakdown ───────────────────────────────────────────────
print("\n===== FAILURE REASON BREAKDOWN =====")
reasons = run_query("""
    SELECT 
        failure_reason,
        COUNT(*) AS count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM transactions WHERE status = 'failure'), 2) AS pct_of_failures
    FROM transactions
    WHERE status = 'failure'
    GROUP BY failure_reason
    ORDER BY count DESC
""")
print(reasons.to_string(index=False))

# ── 4. Retry Analytics ────────────────────────────────────────────────────────
print("\n===== RETRY ANALYTICS =====")
retry = run_query("""
    SELECT
        failure_reason,
        COUNT(*) AS failed_attempts,
        ROUND(AVG(retry_count), 2) AS avg_retries,
        MAX(retry_count) AS max_retries
    FROM transactions
    WHERE status = 'failure'
    AND failure_reason IS NOT NULL
    GROUP BY failure_reason
    ORDER BY avg_retries DESC
""")
print(retry.to_string(index=False))

# ── 5. Hourly Failure Pattern ─────────────────────────────────────────────────
print("\n===== HOURLY FAILURE PATTERN =====")
hourly = run_query("""
    SELECT 
        HOUR(timestamp) AS hour,
        COUNT(*) AS total,
        SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) AS failures,
        ROUND(SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS failure_pct
    FROM transactions
    GROUP BY HOUR(timestamp)
    ORDER BY hour
""")
print(hourly.to_string(index=False))

# ── 6. Gateway Health ─────────────────────────────────────────────────────────
print("\n===== GATEWAY HEALTH =====")
gateway = run_query("""
    SELECT 
        gateway,
        COUNT(*) AS total,
        SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) AS failures,
        ROUND(SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS failure_pct,
        ROUND(AVG(latency_ms), 0) AS avg_latency_ms
    FROM transactions
    GROUP BY gateway
    ORDER BY failure_pct DESC
""")
print(gateway.to_string(index=False))

# ── 7. Top 10 Failing Merchants ───────────────────────────────────────────────
print("\n===== TOP 10 FAILING MERCHANTS =====")
merchants = run_query("""
    SELECT 
        merchant_id,
        COUNT(*) AS total,
        SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) AS failures,
        ROUND(SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS failure_pct
    FROM transactions
    GROUP BY merchant_id
    ORDER BY failure_pct DESC
    LIMIT 10
""")
print(merchants.to_string(index=False))
print("\n===== ANALYSIS COMPLETE =====")