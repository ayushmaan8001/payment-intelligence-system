# 💳 Payment Intelligence System

> An end-to-end real-time payment transaction failure monitoring and intelligence system — built with Python, FastAPI, MySQL, Scikit-learn, and Tableau.

---

## 🧠 What This Project Does

Every payment app — Swiggy, PhonePe, Amazon — deals with transaction failures daily. This system:

- Ingests live transactions through a REST API built with FastAPI
- Scores each transaction in real-time using a Random Forest ML model
- Monitors failure patterns across payment methods, gateways, and time
- Identifies peak failure hours, weak gateways, and top failure reasons
- Visualizes everything on a live Tableau dashboard connected to MySQL

---

## 🏗️ Project Structure

```
payment-intelligence-system/
│
├── app/                        # FastAPI backend (Phase 2)
│     ├── main.py               # App entry point
│     ├── database.py           # Database connection
│     ├── routers/
│     │     ├── transactions.py # POST /api/transaction
│     │     └── analytics.py    # GET analytics endpoints
│     └── services/
│           └── ml_service.py   # ML scoring service
│
├── simulator.py                # Synthetic dataset generator
├── live_simulator.py           # Real-time transaction stream
├── load_data.py                # MySQL data pipeline
├── analysis.py                 # SQL analytical queries
├── ml_model.py                 # Random Forest model training
├── requirements.txt            # Python dependencies
└── Book1.twb                   # Tableau dashboard
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/ayushmaan8001/payment-intelligence-system.git
cd payment-intelligence-system
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup MySQL
```sql
CREATE DATABASE payment_intelligence;
```

### 4. Create .env file
```
DB_PASSWORD=your_mysql_password
```

### 5. Run the pipeline
```bash
python simulator.py       # Generate 100k transactions
python load_data.py       # Load into MySQL
python analysis.py        # Run SQL analysis
python ml_model.py        # Train ML model
```

### 6. Start FastAPI backend
```bash
uvicorn app.main:app --reload --port 8001
```

### 7. Start live simulator
```bash
python live_simulator.py  # Stream live transactions to API
```

### 8. Open Tableau Dashboard
Open `Book1.twb` in Tableau Desktop and connect to MySQL when prompted.

---

## 📊 Key Insights

| Metric | Finding |
|--------|---------|
| Overall Failure Rate | 20.76% |
| Peak Failure Hours | 8PM - 10PM (30%+ failure rate) |
| Weakest Gateway | GW_C (24% failure vs 19% average) |
| Top Failure Reason | INSUFFICIENT_FUNDS (25.33%) |
| ML Model ROC-AUC | 0.85 (Random Forest) |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/transaction | Ingest transaction + ML score |
| GET | /api/summary | Overall metrics |
| GET | /api/method-health | Failure by payment method |
| GET | /api/hourly-pattern | Hourly failure trends |
| GET | /api/gateway-health | Gateway performance |
| GET | /api/retry-analytics | Retry intelligence |
| GET | /api/top-failing-merchants | Merchant risk |

---

## 🛠️ Tech Stack

- **Python** — Data generation, analysis, ML
- **FastAPI + Uvicorn** — REST API backend
- **MySQL** — Structured data storage
- **SQLAlchemy + PyMySQL** — Database connectivity
- **Scikit-learn** — Machine learning
- **Tableau Desktop** — Interactive dashboard
- **pandas / numpy** — Data processing

---

## 🚀 Roadmap

- [x] Synthetic transaction simulator
- [x] MySQL data pipeline
- [x] SQL analytical engine
- [x] Random Forest ML model (ROC-AUC: 0.85)
- [x] FastAPI REST backend
- [x] Real-time ML scoring
- [x] Live transaction simulator
- [x] Tableau dashboard
- [ ] Docker containerization
- [ ] Surge prediction model