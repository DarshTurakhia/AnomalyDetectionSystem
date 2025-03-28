import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.preprocess import preprocess_data

# Load Data
df, df_scaled = preprocess_data()

# Drop User_ID if exists
if "User_ID" in df_scaled.columns:
    df_scaled = df_scaled.drop(columns=["User_ID"])

# Define Autoencoder Model
model = Sequential([
    Dense(4, activation='relu', input_shape=(df_scaled.shape[1],)),
    Dense(2, activation='relu'),
    Dense(4, activation='relu'),
    Dense(df_scaled.shape[1], activation='sigmoid')
])

# Compile Model
model.compile(optimizer='adam', loss=tf.keras.losses.MeanSquaredError())

# Train Model
model.fit(df_scaled, df_scaled, epochs=50, batch_size=2, verbose=1)

# Save Model
model.save("models/autoencoder_model.h5")
print("✅ Autoencoder model saved successfully!")
