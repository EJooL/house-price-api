import joblib
import json
import numpy as np
from pathlib import Path
from app.preprocess import build_input_dataframe, format_price

# ── Path Configuration ────────────────────────────────
BASE_DIR  = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "model"

# ── Load Assets ───────────────────────────────────────
def load_assets():
    model = joblib.load(MODEL_DIR / "xgb_property_model.pkl")

    with open(MODEL_DIR / "feature_cols.json")  as f:
        feature_cols = json.load(f)

    with open(MODEL_DIR / "city_list.json")     as f:
        city_list = json.load(f)

    with open(MODEL_DIR / "district_list.json") as f:
        district_list = json.load(f)

    return model, feature_cols, city_list, district_list


# ── Load sekali saat startup ──────────────────────────
model, feature_cols, city_list, district_list = load_assets()


# ── Predict Function ──────────────────────────────────
def predict_price(input_data: dict) -> dict:

    # Build input DataFrame
    df = build_input_dataframe(input_data, feature_cols)

    # Predict
    log_pred = model.predict(df)[0]
    price_rp = float(np.expm1(log_pred))
    low      = price_rp * 0.85
    high     = price_rp * 1.15

    return {
        "status"                   : "success",
        "predicted_price"          : price_rp,
        "predicted_price_formatted": format_price(price_rp),
        "price_range": {
            "low"           : low,
            "low_formatted" : format_price(low),
            "high"          : high,
            "high_formatted": format_price(high)
        },
        "model_version": "1.0.0"
    }


# ── Getter Functions ──────────────────────────────────
def get_city_list()     -> list: return city_list
def get_district_list() -> list: return district_list
def get_model_info()    -> dict:
    return {
        "model"    : "XGBoost (Tuned)",
        "version"  : "1.0.0",
        "r2_score" : 0.9144,
        "mae"      : 789055794,
        "features" : len(feature_cols),
        "cities"   : len(city_list),
        "districts": len(district_list)
    }