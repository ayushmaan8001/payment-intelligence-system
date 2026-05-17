# 💳 Payment Intelligence System
> An end-to-end real-time payment transaction failure monitoring and intelligence system — built with Python, FastAPI, MySQL, Scikit-learn, Tableau, and Docker.

---

## 🧠 What This Project Does

Every payment app - Swiggy, PhonePe, Amazon — deals with transaction failures daily. This system:
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
├── app/                        # FastAPI backend
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
├── Dockerfile                  # FastAPI container
├── docker-compose.yml          # FastAPI + MySQL orchestration
├── requirements.txt            # Python dependencies
└── Book1.twb                   # Tableau dashboard
```

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.13
- Docker Desktop
- Tableau Desktop (for dashboard)

### 1. Clone the repository
```bash
git clone https://github.com/ayushmaan8001/payment-intelligence-system.git
cd payment-intelligence-system
```

### 2. Create .env file
```
DB_PASSWORD=your_mysql_password
DB_HOST=db
```

### 3. Generate dataset and train ML model
```bash
pip install -r requirements.txt
python simulator.py
python ml_model.py
```

### 4. Start everything with Docker
```bash
docker-compose up --build
```

### 5. Load data into MySQL
```bash
python load_data.py
```

### 6. API is live at
```
http://localhost:8001/docs
```

### 7. Start live simulator
```bash
python live_simulator.py
```

### 8. Open Tableau Dashboard
Open `Book1.twb` in Tableau Desktop and connect to MySQL on port 3307 when prompted.

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
- **Docker + Docker Compose** — Containerization
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
- [x] Docker containerization
