from __future__ import annotations
import re
import sqlite3
import pandas as pd
from .utils import RAW_DIR, PROCESSED_DIR, save_dataframe
RAW_PATH = RAW_DIR / "phishing_email_raw.csv"
OUTPUT_PATH = PROCESSED_DIR / "phishing_emails.csv"
SQLITE_PATH = PROCESSED_DIR / "phishing_emails.db"
def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"http\S+", " URL ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
def infer_columns(df: pd.DataFrame) -> tuple[str, str]:
    cols = {c.lower(): c for c in df.columns}
    text_candidates = ["text", "email_text", "body", "content", "message"]
    label_candidates = ["label", "labels", "target", "class"]
    text_col = next((cols[c] for c in text_candidates if c in cols), None)
    label_col = next((cols[c] for c in label_candidates if c in cols), None)
    if text_col is None or label_col is None:
        raise ValueError(f"Could not infer text/label columns from columns={list(df.columns)}")
    return text_col, label_col
def main() -> None:
    df = pd.read_csv(RAW_PATH)
    text_col, label_col = infer_columns(df)
    out = df[[text_col, label_col]].copy()
    out.columns = ["text", "label"]
    out["text"] = out["text"].astype(str).fillna("").map(clean_text)
    out = out[out["text"].str.len() > 10].copy()
    out["label"] = out["label"].astype(str).str.lower()
    out["label_binary"] = out["label"].map({"safe email": 0, "safe": 0, "ham": 0, "legitimate": 0, "phishing email": 1, "phishing": 1, "spam": 1})
    if out["label_binary"].isna().all():
        out["label_binary"] = pd.to_numeric(out["label"], errors="coerce")
    out = out.dropna(subset=["label_binary"]).copy()
    out["label_binary"] = out["label_binary"].astype(int)
    save_dataframe(out, OUTPUT_PATH)
    with sqlite3.connect(SQLITE_PATH) as conn:
        out.to_sql("phishing_emails", conn, if_exists="replace", index=False)
    print(f"Saved processed data to {OUTPUT_PATH}")
if __name__ == "__main__":
    main()
