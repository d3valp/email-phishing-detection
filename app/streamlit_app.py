from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st
from src.predict import score_email
ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models"
PROCESSED_DIR = ROOT / "data" / "processed"
st.set_page_config(page_title="Phishing Email Detector", layout="wide")
st.title("Phishing Email Detector")
metrics_path = MODELS_DIR / "metrics.json"
data_path = PROCESSED_DIR / "phishing_emails.csv"
if metrics_path.exists():
    metrics = json.loads(metrics_path.read_text())
    cols = st.columns(5)
    for col, (name, value) in zip(cols, [(k, metrics.get(k)) for k in ["accuracy", "precision", "recall", "f1", "roc_auc"]]):
        col.metric(name.upper(), value)
sample_text = st.text_area("Paste an email message", value="Dear user, your account has been flagged. Click the link below to verify your credentials immediately.", height=180)
if st.button("Score email"):
    try:
        result = score_email(sample_text)
        st.json(result)
    except FileNotFoundError:
        st.error("Train the model first by running python -m src.train")
if data_path.exists():
    df = pd.read_csv(data_path)
    st.subheader("Dataset label distribution")
    chart_df = df["label_binary"].value_counts().rename_axis("label_binary").reset_index(name="count")
    chart_df["label_name"] = chart_df["label_binary"].map({0: "safe", 1: "phishing_or_spam"})
    fig = px.bar(chart_df, x="label_name", y="count", title="Class distribution")
    st.plotly_chart(fig, use_container_width=True)
