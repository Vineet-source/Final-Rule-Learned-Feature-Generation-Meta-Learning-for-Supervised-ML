import pandas as pd
import numpy as np
from config import *
from model_loader import model

def evaluate_rules(feat, tstep):
    # Safe get with defaults
    f3   = feat.get("feat_3", 0)
    f4   = feat.get("feat_4", 0)
    f10  = feat.get("feat_10", 0)
    f15  = feat.get("feat_15", 0)
    f20  = feat.get("feat_20", 1)
    f100 = feat.get("feat_100", 0)

    # --- Rule Logic ---
    R1 = int(f3 > TH_HIGH_VALUE)
    R2 = int(f4 <= TH_ZERO_FEE)
    R3 = int(tstep <= TH_EARLY_STEP)
    R4 = int(f3 < TH_LOW_VALUE and R1 == 0)
    R5 = int(f100 > TH_AGGREGATE)
    R6 = int(f10 > TH_VELOCITY)
    R7 = int((f15 / (f20 + 1e-6)) > TH_STRUCTURAL)

    fired = {
        "R1": R1, "R2": R2, "R3": R3, "R4": R4,
        "R5": R5, "R6": R6, "R7": R7
    }

    total = (
        R1 * W_R1 + 
        R2 * W_R2 + 
        R3 * W_R3 + 
        R4 * W_R4 +
        R5 * W_R5 + 
        R6 * W_R6 + 
        R7 * W_R7
    )
    
    return total, fired

def hybrid_predict(features, time_step):
    """
    1. Run Rule Engine
    2. Construct Full Feature Vector (Features + Rules)
    3. Run ML Model
    """
    # 1. Run Rule Engine FIRST
    rule_score, fired_rules = evaluate_rules(features, time_step)

    # 2. Prepare ML Input
    try:
        # Start with the input features
        input_data = features.copy()
        input_data['time_step'] = time_step
        
        # Add the Rule Features (Model likely trained on these names)
        for r_key, val in fired_rules.items():
            input_data[f"{r_key}_Fired"] = val  # e.g., "R1_Fired"
            
        input_data['Total_Rule_Score'] = rule_score

        # Convert to DataFrame
        df_input = pd.DataFrame([input_data])

        # --- CRITICAL FIX: Align columns with Model ---
        # Get the list of columns the model was actually trained on
        booster = model.get_booster()
        expected_cols = booster.feature_names
        
        if expected_cols:
            # Reindex ensures we have exactly the right columns in the right order.
            # Missing columns (like feat_0, feat_1, etc.) are filled with 0.
            df_final = df_input.reindex(columns=expected_cols, fill_value=0)
        else:
            # Fallback if feature names aren't saved in model
            df_final = df_input

        # 3. ML Prediction
        ml_prob = float(model.predict_proba(df_final)[:, 1][0])
        
    except Exception as e:
        print(f"⚠️ ML Prediction Failed (Using Fallback): {e}")
        # If ML fails (e.g. shape mismatch), fallback to just rules
        ml_prob = 0.0

    # 4. Final Decision
    is_fraud = (ml_prob >= ML_THRESHOLD) or (rule_score >= RULE_THRESHOLD)

    return ml_prob, rule_score, fired_rules, is_fraud
