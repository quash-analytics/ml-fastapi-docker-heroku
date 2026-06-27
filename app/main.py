from fastapi import FastAPI
from pydantic import BaseModel
from app.model.language_detection.language_detection_model import predict_language
from app.model.language_detection.language_detection_model import __version__ as model_version


app = FastAPI()


class TextIn(BaseModel):
    text: str


class PredictionOut(BaseModel):
    language: str


@app.get("/")
def home():
    return {"health_check": "OK", "model_version": model_version}


@app.post("/predict", response_model=PredictionOut)
def predict(payload: TextIn):
    language = predict_language([payload.text])[0]
    return {"language": language}