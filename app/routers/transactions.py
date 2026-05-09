from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db
from app.services.ml_service import predict_failure

router = APIRouter()

class TransactionInput(BaseModel):
    user_id: int
    merchant_id: int
    amount: float
    payment_method: str
    gateway: str
    status: str
    failure_reason: str = None
    retry_count: int = 0
    attempt_number: int = 1
    latency_ms: int = 300

@router.post("/transaction")
def add_transaction(txn: TransactionInput, db: Session = Depends(get_db)):
    
    # Get ML prediction
    hour = datetime.now().hour
    ml_result = predict_failure(
        amount=txn.amount,
        payment_method=txn.payment_method,
        gateway=txn.gateway,
        hour=hour
    )

    # Insert into DB
    query = text("""
        INSERT INTO transactions 
        (transaction_id, user_id, merchant_id, amount, payment_method,
         gateway, status, failure_reason, retry_count, attempt_number,
         timestamp, latency_ms)
        VALUES 
        (:transaction_id, :user_id, :merchant_id, :amount, :payment_method,
         :gateway, :status, :failure_reason, :retry_count, :attempt_number,
         :timestamp, :latency_ms)
    """)

    # Get next transaction_id
    result = db.execute(text("SELECT MAX(transaction_id) FROM transactions"))
    max_id = result.scalar() or 0

    db.execute(query, {
        "transaction_id": max_id + 1,
        "user_id": txn.user_id,
        "merchant_id": txn.merchant_id,
        "amount": txn.amount,
        "payment_method": txn.payment_method,
        "gateway": txn.gateway,
        "status": txn.status,
        "failure_reason": txn.failure_reason,
        "retry_count": txn.retry_count,
        "attempt_number": txn.attempt_number,
        "timestamp": datetime.now(),
        "latency_ms": txn.latency_ms
    })
    db.commit()

    return {
        "message": "Transaction recorded",
        "transaction_id": max_id + 1,
        "ml_prediction": ml_result
    }