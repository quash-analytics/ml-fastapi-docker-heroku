# ml-fastapi-docker-heroku

A production-ready template for deploying a machine learning model as a REST API using **FastAPI**, **Docker**, and **Heroku**. This repo uses a pre-trained language detection model as the example ML workload.

The Heroku App working
<img width="1725" height="918" alt="Screenshot 2026-06-27 at 8 49 57 AM" src="https://github.com/user-attachments/assets/ce1239d4-40bd-45d3-adbc-ca67ecc4f112" />

---

## Overview

This project demonstrates the full pipeline from a trained scikit-learn model to a live, containerized API endpoint:

1. A scikit-learn `Pipeline` (TF-IDF vectorizer + Multinomial Naive Bayes) is trained to classify text into one of 17 languages.
2. The pipeline is serialized as a `.pkl` file and loaded at startup.
3. FastAPI exposes two HTTP endpoints — a health check and a prediction route.
4. The app is containerized with Docker and deployed to Heroku using the container stack.

---

## Tech Stack

| Layer | Technology |
|---|---|
| API framework | FastAPI |
| ML library | scikit-learn |
| Server | Gunicorn + Uvicorn workers |
| Container | Docker |
| Hosting | Heroku (container stack) |
| Python | 3.11 |

---

## Supported Languages

The model can detect the following 17 languages:

Arabic, Danish, Dutch, English, French, German, Greek, Hindi, Italian, Kannada, Malayalam, Portugeese, Russian, Spanish, Sweedish, Tamil, Turkish

---

## Project Structure

```
├── app/
│   ├── main.py                          # FastAPI app with / and /predict routes
│   └── model/
│       └── language_detection/
│           ├── language_detection_model.py   # Model loading and prediction logic
│           └── trained_pipeline-0.1.0.pkl    # Serialized scikit-learn pipeline
├── Dockerfile                           # Container definition
├── heroku.yml                           # Heroku container stack config
└── requirements.txt                     # Python dependencies
```

---

## API Endpoints

### `GET /`
Health check. Returns the model version.

**Response:**
```json
{
  "health_check": "OK",
  "model_version": "0.1.0"
}
```

### `POST /predict`
Predicts the language of the given text.

**Request body:**
```json
{
  "text": "Bonjour, comment allez-vous?"
}
```

**Response:**
```json
{
  "language": "French"
}
```

---

## Running Locally

### With Docker

```bash
docker build -t language-detection-app .
docker run -d -p 80:80 --name language-detection language-detection-app
```

Then visit `http://localhost/` or use the interactive docs at `http://localhost/docs`.

### Without Docker

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## Deploying to Heroku

### Prerequisites
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed
- Logged in via `heroku login`
- A Heroku app created with the container stack enabled

### Steps

```bash
# Set the container stack
heroku stack:set container -a <your-app-name>

# Add the Heroku git remote
heroku git:remote -a <your-app-name>

# Push to deploy
git push heroku HEAD:main
```

> **Note:** Set `WEB_CONCURRENCY=1` in the Dockerfile to avoid memory quota errors on Basic dynos, since each worker loads the full ML model into memory.

