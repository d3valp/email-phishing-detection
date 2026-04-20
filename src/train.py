from __future__ import annotations
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, average_precision_score, classification_report, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from .utils import PROCESSED_DIR, MODELS_DIR, dump_artifact
DATA_PATH = PROCESSED_DIR / "phishing_emails.csv"
def main() -> None:
    df = pd.read_csv(DATA_PATH)
    X_train, X_test, y_train, y_test = train_test_split(df["text"], df["label_binary"], test_size=0.2, random_state=42, stratify=df["label_binary"])
    pipeline = Pipeline(steps=[("tfidf", TfidfVectorizer(max_features=25000, ngram_range=(1, 2), min_df=2)), ("model", LogisticRegression(max_iter=2000, class_weight="balanced"))])
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)
    probs = pipeline.predict_proba(X_test)[:, 1]
    metrics = {
        "accuracy": round(float(accuracy_score(y_test, preds)), 4),
        "precision": round(float(precision_score(y_test, preds)), 4),
        "recall": round(float(recall_score(y_test, preds)), 4),
        "f1": round(float(f1_score(y_test, preds)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, probs)), 4),
        "average_precision": round(float(average_precision_score(y_test, probs)), 4),
        "positive_rate": round(float(y_test.mean()), 4),
        "classification_report": classification_report(y_test, preds, output_dict=True),
    }
    dump_artifact(pipeline, MODELS_DIR / "model.joblib")
    (MODELS_DIR / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print(json.dumps({k: v for k, v in metrics.items() if k != "classification_report"}, indent=2))
if __name__ == "__main__":
    main()
