# Payment Intelligence System 💳

A complete **Payment Failure Monitoring & Predictive Intelligence System** built using **Python, MySQL, Machine Learning, and Tableau**.

The project focuses on simulating payment transactions, identifying transaction failures, analyzing operational patterns, and predicting future payment failures using machine learning techniques.

It is designed to represent how modern fintech and digital payment platforms monitor transaction reliability and improve operational efficiency through data-driven insights.

---

## 🚀 Key Features

- Synthetic payment transaction data generation
- MySQL-based data storage and management
- Failure monitoring and operational analytics
- SQL-driven business insights
- Machine Learning model for payment failure prediction
- Tableau dashboard for visualization
- End-to-end analytics workflow

---

## 🛠️ Technologies Used

| Technology | Usage |
|------------|-------|
| Python | Data generation, analysis, ML |
| MySQL | Database management |
| Pandas & NumPy | Data processing |
| Scikit-learn | Machine learning |
| SQL | Analytical queries |
| Tableau | Dashboard & visualization |

---

# 📂 Project Structure

```bash
payment-intelligence-system/
│
├── simulator.py
├── load_data.py
├── analysis.py
├── ml_model.py
├── requirements.txt
├── Book1.twb
└── README.md
```

---

# ⚙️ Setup Instructions

## 1. Clone the Repository

```bash
git clone https://github.com/ayushmaan8001/payment-intelligence-system.git
cd payment-intelligence-system
```

---

## 2. Install Required Dependencies

Make sure Python 3.10 or above is installed.

```bash
pip install -r requirements.txt
```

---

## 3. Configure MySQL

Install MySQL 8.0 and create the database:

```sql
CREATE DATABASE payment_intelligence;
```

---

## 4. Create Environment File

Create a `.env` file inside the project directory.

```env
DB_PASSWORD=your_mysql_password
```

Optional configuration:

```env
DB_HOST=localhost
DB_USER=root
DB_NAME=payment_intelligence
```

---

# ▶️ Running the Project

## Step 1 - Generate Transaction Dataset

```bash
python simulator.py
```

This script generates synthetic payment transaction records containing:

- Successful and failed payments
- Transaction timestamps
- Payment methods
- Bank responses
- Geographic information
- Failure reasons

---

## Step 2 - Load Data into MySQL

```bash
python load_data.py
```

The script:
- Creates database tables
- Cleans the generated dataset
- Loads transaction records into MySQL

---

## Step 3 - Run Data Analysis

```bash
python analysis.py
```

This performs:
- Failure rate analysis
- Gateway performance analysis
- Transaction trend analysis
- Operational intelligence reporting

---

## Step 4 - Train Machine Learning Model

```bash
python ml_model.py
```

The machine learning pipeline:
- Preprocesses transaction data
- Trains a Random Forest classifier
- Predicts transaction failure probability
- Evaluates model performance

---

# 📈 Tableau Dashboard

The project includes a Tableau dashboard file:

```bash
Book1.twb
```

The dashboard can be used to visualize:

- Transaction success vs failure trends
- Payment gateway analytics
- Regional transaction activity
- Operational KPIs
- Failure distribution patterns

> Tableau dashboard requires an active MySQL connection.

---

# 🤖 Machine Learning Overview

The system uses a **Random Forest Classifier** to predict whether a transaction is likely to fail.

### Prediction Factors

The model considers multiple attributes such as:

- Transaction amount
- Payment method
- Gateway response
- Transaction timing
- Bank behavior
- Location/device indicators

---

# 📊 Example Applications

- FinTech monitoring systems
- Banking analytics projects
- Operational intelligence platforms
- Payment gateway analysis
- Failure prediction systems
- Data analytics portfolio projects

---

# 🔮 Future Improvements

Some possible future enhancements:

- Real-time transaction monitoring
- FastAPI backend integration
- Docker-based deployment
- Live analytics dashboard
- Advanced fraud detection
- Kafka-based event streaming
- Cloud deployment support

---

# 📌 Workflow

```text
Synthetic Data Generation
            ↓
      MySQL Database
            ↓
      SQL Analytics
            ↓
   Machine Learning
            ↓
   Tableau Dashboard
```

---

# 🤝 Contribution

Contributions and improvements are always welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

# 📜 License

This project is created for educational and learning purposes.

---

# 👨‍💻 Author

**Ayushmaan Singh**

GitHub: https://github.com/ayushmaan8001
