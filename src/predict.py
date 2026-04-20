from __future__ import annotations
import re
from .utils import MODELS_DIR, load_artifact
def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"http\S+", " URL ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
def score_email(text: str) -> dict:
    model = load_artifact(MODELS_DIR / "model.joblib")
    cleaned = clean_text(text)
    prob = float(model.predict_proba([cleaned])[0, 1])
    pred = int(prob >= 0.5)
    return {"prediction": pred, "label": "phishing_or_spam" if pred == 1 else "safe", "probability_phishing": round(prob, 4)}
