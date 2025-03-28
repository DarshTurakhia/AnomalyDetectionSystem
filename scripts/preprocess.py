from sklearn.preprocessing import StandardScaler
import pandas as pd

def preprocess_data():
    df = pd.read_csv("data/myFile0.csv")  # Load your dataset

    # Convert time column to numeric (adjust column name accordingly)
    if "time_column" in df.columns:
        df["time_column"] = pd.to_datetime(df["time_column"], format="%I:%M %p").dt.hour * 3600 + \
                            pd.to_datetime(df["time_column"], format="%I:%M %p").dt.minute * 60

    # Drop non-numeric columns (except target variables)
    non_numeric_columns = df.select_dtypes(include=["object"]).columns
    df = df.drop(columns=non_numeric_columns)

    # Initialize and apply StandardScaler
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df.drop(columns=["User_ID"], errors="ignore"))  # Ignore errors if column missing

    # Create a DataFrame with only the columns that were scaled
    columns_to_use = df.drop(columns=["User_ID"], errors="ignore").columns  # Get columns used for scaling
    df_scaled = pd.DataFrame(df_scaled, columns=columns_to_use)

    return df, df_scaled

df, df_scaled = preprocess_data()

# Print first 5 rows of the scaled DataFrame
print("✅ Preprocessing Complete! First 5 rows of scaled data:")
print(df_scaled.head())
