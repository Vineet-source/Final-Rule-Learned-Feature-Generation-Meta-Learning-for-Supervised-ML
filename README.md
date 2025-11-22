# Hybrid Fraud Detection System with Meta-Learning

A real-time fraud detection system combining **XGBoost Machine Learning** with a **Rule-Based Engine** to detect illicit Bitcoin transactions.

## 🏗️ Tech Stack
- **Frontend:** Streamlit
- **Backend:** FastAPI
- **Database:** PostgreSQL
- **ML Model:** XGBoost (Trained on Elliptic Dataset)

## 🚀 How to Run

### 1. Setup Database
Ensure PostgreSQL is running and create the database:
```sql
CREATE DATABASE fraud_db;

### 2. Install Dependencies
pip install -r backend/requirements.txt

### 3. Configure Environment
create a .env file in backend/ folder and put this :
DB_HOST=localhost
DB_NAME=fraud_db
DB_USER=postgres
DB_PASSWORD=your_password #your_postgres_password
DB_PORT=5432

### 4. Run the System :

Terminal 1(backend):
cd backend
uvicorn app:app --reload

Terminal 2(frontend):
streamlit run streamlit_app/Home.py
