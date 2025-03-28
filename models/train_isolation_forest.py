import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.preprocess import preprocess_data

# Load preprocessed data
df, df_scaled = preprocess_data()

# Drop User_ID if it exists
if "User_ID" in df_scaled.columns:
    df_scaled = df_scaled.drop(columns=["User_ID"])

# Train Isolation Forest Model
model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
model.fit(df_scaled)

# Save Model
joblib.dump(model, "models/isolation_forest.pkl")

# Predict Anomalies
df["Anomaly_Score"] = model.predict(df_scaled)
df["Anomaly"] = df["Anomaly_Score"].apply(lambda x: 1 if x == -1 else 0)

# Ensure correct user ID column
if "User_ID" in df.columns:
    user_column = "User_ID"
elif "user_id" in df.columns:
    user_column = "user_id"
else:
    raise ValueError("User ID column not found in dataset!")

# Save anomaly detection results
anomaly_results = pd.DataFrame({
    user_column: df[user_column],
    "anomaly_score": df["Anomaly_Score"]
})

anomaly_results.to_csv("anomaly_results.csv", index=False)
print("✅ Anomaly detection results saved successfully!")