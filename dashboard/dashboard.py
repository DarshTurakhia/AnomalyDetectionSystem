import streamlit as st
import requests

st.title("🔍 Insider Threat Detection Dashboard")

# Fetch Alerts
alerts = requests.get("http://127.0.0.1:5000/alerts").json()

# Display Alerts
if alerts:
    for alert in alerts:
        st.error(f"⚠️ User {alert['User_ID']} detected as anomalous!")
else:
    st.success("✅ No Threats Detected")
