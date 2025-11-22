import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import average_precision_score
import time
import os

print("Hybrid pipeline started...")

# --- Configuration ---
base_path = "elliptic_bitcoin_dataset/"
file_features = os.path.join(base_path, "elliptic_txs_features.csv")
file_classes = os.path.join(base_path, "elliptic_txs_classes.csv")

# --- 0. Data Validation ---
if not os.path.exists(file_features) or not os.path.exists(file_classes):
    print(f"Error: Data files not found in directory '{base_path}'")
    exit()

# --- 1. Load and Preprocess Data ---
print("Loading data...")
col_names = ['txId', 'time_step'] + [f'feat_{i}' for i in range(165)]
df_features = pd.read_csv(file_features, header=None, names=col_names)
df_classes = pd.read_csv(file_classes)
df_merged = df_features.merge(df_classes, on='txId', how='left')
df_labeled = df_merged[df_merged['class'] != 'unknown'].copy()
df_labeled['class'] = df_labeled['class'].map({'1': 1, '2': 0})
print("Data loading and preprocessing complete.")

# --- 2. Phase 1: Rule Engine (Feature Generation) ---
def rule_engine_feature_generation(df):
    # Thresholds (Used for Training)
    TH_HIGH_VALUE = 50000.0
    TH_ZERO_FEE = 0.0
    TH_EARLY_STEP = 5
    TH_LOW_VALUE = 50.0
    TH_AGGREGATE = 0.8
    TH_VELOCITY = 10.0
    TH_STRUCTURAL = 2.0

    # R1: High-Value Outflow
    df['R1_Fired'] = np.where(df['feat_3'] > TH_HIGH_VALUE, 1, 0)

    # R2: Zero-Fee
    df['R2_Fired'] = np.where(df['feat_4'] <= TH_ZERO_FEE, 1, 0)

    # R3: Initial Activity
    df['R3_Fired'] = np.where(df['time_step'] <= TH_EARLY_STEP, 1, 0)

    # R4: Low Value Structuring
    df['R4_Fired'] = np.where((df['feat_3'] < TH_LOW_VALUE) & (df['R1_Fired'] == 0), 1, 0)

    # R5: Neighbor Aggregation
    df['R5_Fired'] = np.where(df['feat_100'] > TH_AGGREGATE, 1, 0)

    # R6: High Velocity
    df['R6_Fired'] = np.where(df['feat_10'] > TH_VELOCITY, 1, 0)

    # R7: Structural Anomaly
    df['R7_Fired'] = np.where(df['feat_15'] / (df['feat_20'] + 1e-6) > TH_STRUCTURAL, 1, 0)

    # Create Aggregate Score Meta-Feature for training context
    df['Total_Rule_Score'] = (df['R1_Fired'] * 15 + df['R2_Fired'] * 10 + 
                              df['R3_Fired'] * 5 + df['R4_Fired'] * 10 + 
                              df['R5_Fired'] * 15 + df['R6_Fired'] * 5 + 
                              df['R7_Fired'] * 10)

    return df

print("Generating meta-features...")
df_augmented = rule_engine_feature_generation(df_labeled)

# --- 3. Creating Train/Test Splits ---
split_time_step = 34
train_indices = df_augmented[df_augmented['time_step'] <= split_time_step].index
test_indices = df_augmented[df_augmented['time_step'] > split_time_step].index

y_train = df_augmented['class'].loc[train_indices]
y_test = df_augmented['class'].loc[test_indices]

# Hybrid Data (Includes Rules + Anon Features)
X_augmented = df_augmented.drop(columns=['txId', 'time_step', 'class'])
X_train_hybrid = X_augmented.loc[train_indices]
X_test_hybrid = X_augmented.loc[test_indices]

scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

# --- 4. Training Hybrid Model ---
print(f"\nTraining Hybrid XGBoost Model (Scale Weight: {scale_pos_weight:.2f})...")
model = xgb.XGBClassifier(
    objective='binary:logistic',
    eval_metric='aucpr',
    scale_pos_weight=scale_pos_weight,
    n_estimators=200,
    learning_rate=0.1,
    max_depth=5,
    use_label_encoder=False,
    tree_method='hist'
)

model.fit(X_train_hybrid, y_train, eval_set=[(X_test_hybrid, y_test)], verbose=False)
model.save_model("elliptic_xgb_hybrid_model.json")
print("Model saved.")

# --- 5. PREPARE DATA FOR REAL-TIME APP (CRITICAL FIX) ---
print("\nGenerating Simulation Data for Streamlit App...")

# Get the "Base Confidence" from the ML model
y_probs = model.predict_proba(X_test_hybrid)[:, 1]

# Identify specific feature columns needed for the app sliders
# These correspond to the features used in rule_engine_feature_generation
required_features = ['feat_3', 'feat_4', 'time_step', 'feat_100', 'feat_10', 'feat_15', 'feat_20']

# Select ONLY the test set rows
df_test_data = df_augmented.loc[test_indices].copy()

# Create the lightweight dataframe
# We save the RAW features so the App can recalculate rules dynamically
simulation_data = df_test_data[required_features].copy()
simulation_data['Hybrid_Confidence'] = y_probs
simulation_data['True_Label'] = y_test.values

# Save to CSV
simulation_data.to_csv("simulation_data.csv", index=False)
print("Success! 'simulation_data.csv' saved with RAW features (feat_3, etc.) for the dashboard.")