from __future__ import annotations
from datasets import load_dataset
from .utils import RAW_DIR
OUTPUT_PATH = RAW_DIR / "phishing_email_raw.csv"
def main() -> None:
    dataset = load_dataset("zefang-liu/phishing-email-dataset", split="train")
    df = dataset.to_pandas()
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved raw data to {OUTPUT_PATH}")
if __name__ == "__main__":
    main()
