import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import LabelEncoder
import pickle

# ── Connect to DB ─────────────────────────────────────────────────────────────
db_password = os.environ.get('DB_PASSWORD')
engine = create_engine("mysql+pymysql://root:121212@localhost/payment_intelligence")

print("Loading data...")
df = pd.read_sql("SELECT * FROM transactions", engine)
print(f"Loaded {len(df)} rows")

# ── Feature Engineering ───────────────────────────────────────────────────────
df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
df['is_peak_hour'] = df['hour'].apply(lambda x: 1 if 20 <= x <= 21 else 0)
df['is_high_amount'] = df['amount'].apply(lambda x: 1 if x > 3000 else 0)
df['target'] = df['status'].apply(lambda x: 1 if x == 'failure' else 0)

# ── Encode Categorical Features ───────────────────────────────────────────────
le_method = LabelEncoder()
le_gateway = LabelEncoder()

df['payment_method_enc'] = le_method.fit_transform(df['payment_method'])
df['gateway_enc'] = le_gateway.fit_transform(df['gateway'])

# ── Select Features ───────────────────────────────────────────────────────────
features = [
    'amount',
    'payment_method_enc',
    'gateway_enc',
    'hour',
    'is_peak_hour',
    'is_high_amount'
]

X = df[features]
y = df['target']

print(f"\nTarget distribution:")
print(y.value_counts())

# ── Train Test Split ──────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── Model 1: Logistic Regression (Baseline) ───────────────────────────────────
print("\n===== LOGISTIC REGRESSION =====")
lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)
print(classification_report(y_test, y_pred_lr))
print(f"ROC-AUC: {roc_auc_score(y_test, lr.predict_proba(X_test)[:,1]):.4f}")

# ── Model 2: Random Forest ────────────────────────────────────────────────────
print("\n===== RANDOM FOREST =====")
rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
print(classification_report(y_test, y_pred_rf))
print(f"ROC-AUC: {roc_auc_score(y_test, rf.predict_proba(X_test)[:,1]):.4f}")

# ── Feature Importance ────────────────────────────────────────────────────────
print("\n===== FEATURE IMPORTANCE (Random Forest) =====")
importance = pd.DataFrame({
    'feature': features,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)
print(importance.to_string(index=False))

# ── Save Model ────────────────────────────────────────────────────────────────
model_data = {
    'model': rf,
    'le_method': le_method,
    'le_gateway': le_gateway,
    'features': features
}

with open(r"D:\projects\payment-intelligence-system\model.pkl", 'wb') as f:
    pickle.dump(model_data, f)

print("\n===== MODEL SAVED TO model.pkl =====")
engine.dispose()