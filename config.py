import os
from dotenv import load_dotenv

load_dotenv() # Load variables from .env

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "fraud_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secure_password")
DB_PORT = os.getenv("DB_PORT", 5432)
MODEL_PATH = "elliptic_xgb_hybrid_model.json"

# ... Keep your existing Rule thresholds below ...