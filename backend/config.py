import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "fraud_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password") 
DB_PORT = int(os.getenv("DB_PORT", 5432))

MODEL_PATH = os.getenv("MODEL_PATH", "elliptic_xgb_hybrid_model.json")

# Hybrid Model Thresholds
ML_THRESHOLD = 0.5
RULE_THRESHOLD = 40

# Rule engine thresholds
TH_HIGH_VALUE = 50000
TH_ZERO_FEE = 0.0
TH_EARLY_STEP = 5
TH_LOW_VALUE = 50
TH_AGGREGATE = 0.8
TH_VELOCITY = 10.0
TH_STRUCTURAL = 2.0

# Rule weights
W_R1, W_R2, W_R3, W_R4 = 15, 10, 5, 10
W_R5, W_R6, W_R7 = 15, 5, 10
