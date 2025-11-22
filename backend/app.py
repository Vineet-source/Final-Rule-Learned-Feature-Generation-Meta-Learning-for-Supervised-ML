import json  
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from database import init_pool, create_tables, get_conn, release_conn  
from rules import hybrid_predict  

app = FastAPI(title="Hybrid Fraud Detection Backend")

class TxIn(BaseModel):
    user_id: int
    tx_id: str
    time_step: int
    features: Dict[str, float]

@app.on_event("startup")
def startup():
    """Initialize DB pool and ensure tables exist on startup"""
    init_pool()
    create_tables()

@app.post("/transactions")
def process_transaction(tx: TxIn):
    try:
        # 1. Run the Hybrid Model (XGBoost + Rules)
        # Returns: ml_prob (float), rule_score (float), fired (dict), fraud (bool)
        ml_prob, rule_score, fired, fraud = hybrid_predict(tx.features, tx.time_step)
        
        status = "REJECTED" if fraud else "APPROVED"

        # 2. Persist to PostgreSQL
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO transactions
            (user_id, tx_id, time_step, features, ml_probability, rule_score, 
            total_rule_score, fired_rules, final_decision, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            tx.user_id, 
            tx.tx_id, 
            tx.time_step,
            json.dumps(tx.features),  
            float(ml_prob),           
            float(rule_score),
            float(rule_score),        # Assuming total score is current score
            json.dumps(fired),
            bool(fraud),
            status
        ))

        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        release_conn(conn)

        return {
            "id": new_id,
            "fraud": fraud,
            "status": status,
            "ml_probability": ml_prob,
            "rule_score": rule_score,
            "fired_rules": fired
        }

    except Exception as e:
        print(f"Error processing transaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))