from fastapi import APIRouter
from sqlalchemy import text
from app.database import engine
import pandas as pd

router = APIRouter()

@router.get("/summary")
def get_summary():
    query = """
        SELECT 
            COUNT(*) AS total_rows,
            COUNT(DISTINCT transaction_id) AS unique_transactions,
            SUM(CASE WHEN status = 'success' AND retry_count = 0 THEN 1 ELSE 0 END) AS direct_success,
            SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) AS total_failures,
            SUM(CASE WHEN status = 'success' AND retry_count > 0 THEN 1 ELSE 0 END) AS success_after_retry,
            ROUND(SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS failure_rate_pct
        FROM transactions
    """
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")[0]

@router.get("/method-health")
def get_method_health():
    query = """
        SELECT 
            payment_method,
            COUNT(*) AS total,
            SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) AS failures,
            ROUND(SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS failure_pct,
            ROUND(AVG(latency_ms), 0) AS avg_latency_ms
        FROM transactions
        GROUP BY payment_method
        ORDER BY failure_pct DESC
    """
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")

@router.get("/hourly-pattern")
def get_hourly_pattern():
    query = """
        SELECT 
            HOUR(timestamp) AS hour,
            COUNT(*) AS total,
            SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) AS failures,
            ROUND(SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS failure_pct
        FROM transactions
        GROUP BY HOUR(timestamp)
        ORDER BY hour
    """
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")

@router.get("/gateway-health")
def get_gateway_health():
    query = """
        SELECT 
            gateway,
            COUNT(*) AS total,
            SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) AS failures,
            ROUND(SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS failure_pct,
            ROUND(AVG(latency_ms), 0) AS avg_latency_ms
        FROM transactions
        GROUP BY gateway
        ORDER BY failure_pct DESC
    """
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")

@router.get("/retry-analytics")
def get_retry_analytics():
    query = """
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
    """
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")

@router.get("/top-failing-merchants")
def get_top_failing_merchants():
    query = """
        SELECT 
            merchant_id,
            COUNT(*) AS total,
            SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) AS failures,
            ROUND(SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS failure_pct
        FROM transactions
        GROUP BY merchant_id
        ORDER BY failure_pct DESC
        LIMIT 10
    """
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")