# Hybrid Fraud Detection System with Meta-Learning

A real-time fraud detection system combining **XGBoost Machine Learning** with a **Rule-Based Engine** to detect illicit Bitcoin transactions.

---

## 🏗️ Tech Stack
- **Frontend:** Streamlit  
- **Backend:** FastAPI  
- **Database:** PostgreSQL  
- **ML Model:** XGBoost (Trained on Elliptic Dataset)  

---

## 🚀 How to Run

### 1️⃣ Setup Database
Ensure PostgreSQL is running and create the database:

```sql
CREATE DATABASE fraud_db;
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

### 3️⃣ Configure Environment

Create a `.env` file inside the `backend/` folder and add:

```
DB_HOST=localhost
DB_NAME=fraud_db
DB_USER=postgres
DB_PASSWORD=your_password  # replace with your postgres password
DB_PORT=5432
```

---

### 4️⃣ Run the System

#### 🖥 Backend (Terminal 1)

```bash
cd backend
uvicorn app:app --reload
```

#### 🎨 Frontend (Terminal 2)

```bash
streamlit run streamlit_app/Home.py
```

---

✨ You're ready to detect fraud in real-time!
