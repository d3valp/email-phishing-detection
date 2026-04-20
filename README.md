# Phishing Email Detection with NLP, SQL, FastAPI, and Streamlit

A learning project that detects suspicious email content using **TF-IDF features** and a **classification pipeline**, then exposes predictions through **FastAPI** and a **Streamlit dashboard**.

## Why this project matters

Email fraud is a classic real-world classification problem with business stakes:
- false negatives can let malicious content through,
- false positives can block or quarantine legitimate communication,
- model evaluation must therefore go beyond headline accuracy.

This project focuses on building a practical, explainable baseline for phishing or spam-style email detection from text.

## Dataset

This project is designed to download the public **Phishing Email Dataset** hosted on Hugging Face, which is described there as a copy of the Kaggle “Phishing Email Detection” dataset.

Expected characteristics:
- labeled email text,
- binary target separating phishing vs safe email,
- roughly **18,650 rows**.

## Project objectives

- download and standardize public email-text data,
- clean and normalize message content,
- build a reproducible NLP classification pipeline,
- compare baseline models,
- evaluate precision, recall, F1, ROC-AUC,
- expose predictions via API,
- provide a lightweight app for analysts or recruiters to test sample messages.

## Tech stack

- **Python**
- **SQL** (SQLite-style persistence for scored records)
- **scikit-learn**
- **FastAPI**
- **Streamlit**
- **Hugging Face datasets**

## How to run

### 1) Create environment and install dependencies
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Download and prepare the dataset
```bash
python -m src.data_download
python -m src.preprocess
```

### 3) Train the classification pipeline
```bash
python -m src.train
```

### 4) Launch the API
```bash
uvicorn api.main:app --reload
```

### 5) Launch the dashboard
```bash
streamlit run app/streamlit_app.py
```
