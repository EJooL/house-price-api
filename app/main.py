from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schema import PropertyInput, PredictionOutput, ModelInfo
from app.model import (
    predict_price,
    get_city_list,
    get_district_list,
    get_model_info
)
from app.preprocess import validate_city, validate_district

# ── App Initialization ────────────────────────────────
app = FastAPI(
    title       = "Jabodetabek House Price API",
    description = """
    REST API for predicting property prices across Jabodetabek.
    
    ## Endpoints
    - **GET /**          → API info
    - **GET /health**    → Health check
    - **GET /info**      → Model information
    - **GET /cities**    → List available cities
    - **GET /districts** → List available districts
    - **POST /predict**  → Predict property price
    """,
    version     = "1.0.0",
    contact     = {
        "name" : "Ihza Budi Cendhika",
        "url"  : "https://github.com/EJooL",
    }
)

# ── CORS Middleware ───────────────────────────────────
# Agar API bisa diakses dari browser / frontend manapun
app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["*"],
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

# ══════════════════════════════════════════════════════
# ENDPOINTS
# ══════════════════════════════════════════════════════

# ── GET / ─────────────────────────────────────────────
@app.get("/", tags=["General"])
def root():
    return {
        "name"       : "Jabodetabek House Price API",
        "version"    : "1.0.0",
        "status"     : "running",
        "docs"       : "/docs",
        "github"     : "https://github.com/EJooL"
    }


# ── GET /health ───────────────────────────────────────
@app.get("/health", tags=["General"])
def health_check():
    return {
        "status" : "healthy",
        "version": "1.0.0"
    }


# ── GET /info ─────────────────────────────────────────
@app.get("/info", response_model=ModelInfo, tags=["Model"])
def model_info():
    return get_model_info()


# ── GET /cities ───────────────────────────────────────
@app.get("/cities", tags=["Data"])
def list_cities():
    return {
        "cities": get_city_list(),
        "total" : len(get_city_list())
    }


# ── GET /districts ────────────────────────────────────
@app.get("/districts", tags=["Data"])
def list_districts():
    return {
        "districts": get_district_list(),
        "total"    : len(get_district_list())
    }


# ── POST /predict ─────────────────────────────────────
@app.post("/predict", response_model=PredictionOutput, tags=["Prediction"])
def predict(input: PropertyInput):

    # Convert Pydantic model → dict
    input_dict = input.model_dump()

    # Validate city
    if not validate_city(input_dict["city"], get_city_list()):
        raise HTTPException(
            status_code = 422,
            detail      = f"City '{input_dict['city']}' not found. "
                        f"Use GET /cities to see available options."
        )

    # Validate district
    if not validate_district(input_dict["district"], get_district_list()):
        raise HTTPException(
            status_code = 422,
            detail      = f"District '{input_dict['district']}' not found. "
                        f"Use GET /districts to see available options."
        )

    # Predict
    try:
        result = predict_price(input_dict)
        return result
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail      = f"Prediction failed: {str(e)}"
        )