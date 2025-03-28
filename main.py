import os

print("🔄 Running Preprocessing...")
os.system("python scripts/preprocess.py")

print("🛠 Training Isolation Forest Model...")
os.system("python models/train_isolation_forest.py")

print("🤖 Training Autoencoder Model...")
os.system("python models/train_autoencoder.py")

print("🚀 Starting Flask API...")
os.system("python api/app.py")
