from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel, Field
from src.predict import score_email
app = FastAPI(title="Phishing Email Detection API", version="1.0.0")
class EmailPayload(BaseModel):
    text: str = Field(..., min_length=5)
@app.get("/")
def healthcheck() -> dict:
    return {"status": "ok", "message": "Phishing email detection API is running."}
@app.post("/predict")
def predict(payload: EmailPayload) -> dict:
    return score_email(payload.text)
