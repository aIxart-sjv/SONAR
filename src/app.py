import streamlit as st
import pandas as pd
from anomaly_model import train_model, predict_anomalies
from alert_engine import generate_alerts

st.title("SONAR - Smart City Network Radar")

uploaded_file = st.file_uploader("Upload Network Traffic CSV")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.write("Data Preview", df.head())

    model = train_model(df)
    scores, preds = predict_anomalies(model, df)
    alerts = generate_alerts(preds)

    st.subheader("Alerts")
    for alert in alerts:
        st.error(alert)