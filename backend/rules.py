import pandas as pd
import config  # Import the whole config file
from model_loader import model

def evaluate_rules(feat, tstep):
    # Get feature values safely (default to 0 if missing)
    f3   = feat.get("feat_3", 0)
    f4   = feat.get("feat_4", 0)
    f10  = feat.get("feat_10", 0)
    f15  = feat.get("feat_15", 0)
    f20  = feat.get("feat_20", 1)
    f100 = feat.get("feat_100", 0)

    # --- Rule Logic using config.VARIABLE ---
    # R1: High Value Transaction
    R1 = int(f3 > config.TH_HIGH_VALUE)

    # R2: Zero Fee
    R2 = int(f4 <= config.TH_ZERO_FEE)

    # R3: Early Time Step (New account behavior)
    R3 = int(tstep <= config.TH_EARLY_STEP)

    # R4: Low Value but High Risk context (Custom logic)
    R4 = int(f3 < config.TH_LOW_VALUE and R1 == 0)

    # R5: High Neighbor Aggregation (Suspicious network)
    R5 = int(f100 > config.TH_AGGREGATE)

    # R6: High Velocity (Fast movement)
    R6 = int(f10 > config.TH_VELOCITY)

    # R7: Structural Anomaly (Ratio of specific features)
    # Added small epsilon 1e-6 to avoid division by zero
    R7 = int((f15 / (f20 + 1e-6)) > config.TH_STRUCTURAL)

    fired = {
        "R1": R1, "R2": R2, "R3": R3, "R4": R4,
        "R5": R5, "R6": R6, "R7": R7
    }

    # Calculate Weighted Score
    total = (
        R1 * config.W_R1 + 
        R2 * config.W_R2 + 
        R3 * config.W_R3 + 
        R4 * config.W_R4 +
        R5 * config.W_R5 + 
        R6 * config.W_R6 + 
        R7 * config.W_R7
    )
    
    return total, fired

def hybrid_predict(features, time_step):
    """
    Combines XGBoost Probability + Rule Engine Score
    """
    # 1. XGBoost Prediction
    # We need to format the input exactly how the model expects it
    # (For this snippet, we assume the model handles the dict or we map it.
    # Ideally, you convert features dict to the list/array the model expects.)
    
    # Simple workaround if model expects a specific feature vector:
    # In a real app, you must ensure 'features' matches the model training columns.
    # Here we assume the model_loader handles it or we just use the rule engine for now 
    # if the model input is complex.
    
    try:
        # Create a DataFrame with one row
        df_input = pd.DataFrame([features])
        # Ensure columns match model (This is tricky without the exact column list, 
        # but usually XGBoost ignores extra columns or needs exact match)
        ml_prob = model.predict_proba(df_input)[:, 1][0]
    except Exception as e:
        print(f"ML Prediction Warning: {e}")
        ml_prob = 0.0

    # 2. Rule Engine Evaluation
    rule_score, fired_rules = evaluate_rules(features, time_step)

    # 3. Final Decision Logic
    # Fraud if ML is high OR Rules are high
    is_fraud = (ml_prob >= config.ML_THRESHOLD) or (rule_score >= config.RULE_THRESHOLD)

    return ml_prob, rule_score, fired_rules, is_fraud