import os
import logging
from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
from tensorflow.keras.models import load_model
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import pandas as pd
import io

# Load the datasets globally
df_anomalies = pd.read_csv('data/anomaly_results.csv')
df_users = pd.read_csv('data/myFile6.csv')

# Merge dataframes
df = pd.merge(df_anomalies, df_users, on='User_ID', how='left')


# Initialize Flask App
app = Flask(__name__)

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load Pre-trained Models
MODEL_PATHS = {
    "isolation_forest": "models/isolation_forest.pkl",
    "autoencoder": "models/autoencoder_model.h5"
}

models = {}

# 📊 Analytical Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    chart_type = request.form.get('chart_type')
    
    if chart_type == 'department_pie':
        chart = generate_anomaly_score_by_department_chart(df)
    elif chart_type == 'time_series':
        chart = generate_time_series_plot(df)
    elif chart_type == 'network_histogram':
        chart = generate_network_traffic_histogram(df)
    elif chart_type == 'scatter_anomaly':
        chart = generate_scatter_anomaly_vs_file_access(df)
    else:
        chart = None

    return render_template('dashboard.html', chart=chart)

# Bar Graph for department distribution
def generate_anomaly_score_by_department_chart(df):
    # Load your anomaly results and user details
    anomaly_data = pd.read_csv('data/anomaly_results.csv')  # Replace with actual path
    user_data = pd.read_csv('data/myFile6.csv')  # Replace with actual path

    # Merge the data on 'User_ID' as before
    merged_data = pd.merge(anomaly_data, user_data, on='User_ID')

    # Group by department and calculate the mean anomaly score
    department_anomalies = merged_data.groupby('department')['Anomaly_Score'].mean().reset_index()

    # Set up the figure for plotting with larger size
    plt.figure(figsize=(12, 8))  # Increase the figure size

    # Create a bar plot
    sns.barplot(x='Anomaly_Score', y='department', data=department_anomalies, palette='viridis')

    # Add labels and title
    plt.title('Average Anomaly Score by Department')
    plt.xlabel('Anomaly Score')
    plt.ylabel('Department')

    # Rotate the y-axis labels to prevent them from getting trimmed
    plt.yticks(rotation=45)  # Rotates the labels by 45 degrees

    # Adjust layout to ensure labels fit
    plt.tight_layout()

    # Save the plot to a BytesIO object to display it in the HTML template
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode image to base64 to render in the HTML template
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Return the dashboard HTML page with the chart
    return plot_url

def generate_network_traffic_histogram(df):
    plt.figure(figsize=(12, 6))
    sns.histplot(df['Network_Traffic'], bins=30, kde=True, color='blue')
    plt.xlabel("Network Traffic")
    plt.ylabel("Frequency")
    plt.title("Distribution of Network Traffic")
    
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url

def generate_scatter_anomaly_vs_file_access(df):
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x=df['File_Access'], y=df['Anomaly_Score'], alpha=0.6, color='red')
    plt.xlabel("File Access")
    plt.ylabel("Anomaly Score")
    plt.title("Scatter Plot: Anomaly Score vs. File Access")
    
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    #plt.close()
    return plot_url

# Load models dynamically
def load_models():
    """
    Load all machine learning models from the specified paths.
    """
    for model_name, path in MODEL_PATHS.items():
        if os.path.exists(path):
            if path.endswith(".pkl"):
                models[model_name] = joblib.load(path)
            elif path.endswith(".h5"):
                models[model_name] = load_model(path)
            logging.info(f"✅ Loaded model: {model_name}")
        else:
            logging.error(f"❌ Model file not found: {path}")

load_models()

# 🏠 Home Page Route
@app.route("/", methods=["GET"])
def home():
    """
    Render the home page with navigation links.
    """
    return render_template("home.html")

# 🔔 Alerts Page Route
@app.route('/alerts')
def show_alerts():
    # Load anomaly results
    anomaly_results = pd.read_csv("data/anomaly_results.csv")

    # Load user details
    user_details = pd.read_csv("data/myFile6.csv")

    # Clean column names (strip any spaces)
    anomaly_results.columns = anomaly_results.columns.str.strip()
    user_details.columns = user_details.columns.str.strip()

    # Clean User_ID columns to be consistent (convert to string and remove extra spaces)
    anomaly_results['User_ID'] = anomaly_results['User_ID'].astype(str).str.strip()
    user_details['User_ID'] = user_details['User_ID'].astype(str).str.strip()

    # Log the unique User_ID values from both files for debugging
    logging.info(f"🚨 Anomaly User_IDs: {anomaly_results['User_ID'].unique()}")
    logging.info(f"🚨 User Details User_IDs: {user_details['User_ID'].unique()}")

    # Filter only anomalous users (Anomaly == 1)
    anomaly_results = anomaly_results[anomaly_results["Anomaly"] == 1]

    # Perform the merge to include all relevant details including department
    merged_data = pd.merge(anomaly_results, user_details, on="User_ID", how="left")

    # Log merged data preview for debugging
    logging.info(f"🚨 Merged Data Preview: {merged_data.head()}")

    # Convert DataFrame to a dictionary for rendering
    alerts = merged_data.to_dict(orient="records")

    return render_template("alerts.html", alerts=alerts)

# Run Flask App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)