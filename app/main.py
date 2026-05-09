from fastapi import FastAPI
from app.routers import transactions, analytics
from app.services.ml_service import load_model

app = FastAPI(
    title="Payment Intelligence System",
    description="Real-time payment transaction failure monitoring and intelligence API",
    version="2.0"
)

# Load ML model on startup
@app.on_event("startup")
def startup_event():
    load_model()

# Register routers
app.include_router(transactions.router, prefix="/api", tags=["Transactions"])
app.include_router(analytics.router, prefix="/api", tags=["Analytics"])

@app.get("/")
def root():
    return {
        "system": "Payment Intelligence System",
        "version": "2.0",
        "status": "running",
        "docs": "/docs"
    }