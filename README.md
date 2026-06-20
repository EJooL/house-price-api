# Jabodetabek House Price API

A production-ready REST API for predicting property prices across Jabodetabek, built with FastAPI, containerized with Docker, and powered by an XGBoost machine learning model.

Live API: [Add your Railway URL here after deployment]
Interactive Docs: `{your-url}/docs`

---

## Overview

This API serves the machine learning model from the [Jabodetabek House Price Predictor](https://github.com/EJooL/jabodetabek-house-price-predictor) project as a REST API, allowing integration with any platform — web apps, mobile apps, or other backend services.

---

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API info |
| GET | `/health` | Health check |
| GET | `/info` | Model performance metrics |
| GET | `/cities` | List of available cities |
| GET | `/districts` | List of available districts |
| POST | `/predict` | Predict property price |

---

## Example Request

```json
POST /predict
Content-Type: application/json

{
    "city": "Jakarta Selatan",
    "district": "Kebayoran Baru",
    "property_type": "rumah",
    "certificate": "SHM - Sertifikat Hak Milik",
    "furnishing": "furnished",
    "electricity": "2200 mah",
    "property_condition": "baru",
    "land_size_m2": 150,
    "building_size_m2": 120,
    "bedrooms": 3,
    "bathrooms": 2,
    "floors": 2,
    "carports": 1,
    "garages": 1
}
```

## Example Response

```json
{
    "status": "success",
    "predicted_price": 2314068480.0,
    "predicted_price_formatted": "Rp 2,314,068,480",
    "price_range": {
        "low": 1966958208.0,
        "low_formatted": "Rp 1,966,958,208",
        "high": 2661178752.0,
        "high_formatted": "Rp 2,661,178,752"
    },
    "model_version": "1.0.0"
}
```

---

## Tech Stack

| Category | Tools |
|---|---|
| Framework | FastAPI |
| Server | Uvicorn |
| Validation | Pydantic |
| Machine Learning | XGBoost, Scikit-learn |
| Containerization | Docker |
| Deployment | Railway |
| Testing | Pytest |

---

## Project Structure

house-price-api/

│

├── app/

│   ├── init.py

│   ├── main.py          # FastAPI app & endpoints

│   ├── model.py          # Model loading & prediction logic

│   ├── schema.py          # Pydantic request/response schemas

│   └── preprocess.py      # Feature preprocessing pipeline

│

├── model/

│   ├── xgb_property_model.pkl

│   ├── feature_cols.json

│   ├── city_list.json

│   └── district_list.json

│

├── tests/

│   ├── init.py

│   └── test_api.py        # Unit tests (11 test cases)

│

├── conftest.py

├── Dockerfile

├── requirements.txt

└── .gitignore

---

## Running Locally

### Without Docker

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### With Docker

```bash
docker build -t house-price-api .
docker run -p 8000:8000 house-price-api
```

Access the API at `http://localhost:8000/docs`

---

## Testing

```bash
pytest tests/ -v
```

11 test cases covering general endpoints, successful predictions, and error handling (invalid city, missing fields, invalid data types).

---

## Model Performance

| Metric | Value |
|---|---|
| Model | XGBoost (Tuned) |
| R² Score | 0.9144 |
| RMSE | Rp 2,178,687,463 |
| MAE | Rp 789,055,794 |

---

## Related Projects

- [Jabodetabek House Price Predictor](https://github.com/EJooL/jabodetabek-house-price-predictor) — Full ML notebook with EDA, preprocessing, and model training
- [Streamlit Web App](https://jabodetabek-house-price-predictor.streamlit.app) — User-facing prediction interface

---

## Author

**Ihza Budi Cendhika**
- GitHub: [@EJooL](https://github.com/EJooL)
- LinkedIn: [linkedin.com/in/ihzabc](https://linkedin.com/in/ihzabc)