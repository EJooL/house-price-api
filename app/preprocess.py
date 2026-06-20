import pandas as pd

# ── Build Input DataFrame ─────────────────────────────
def build_input_dataframe(input_data: dict, feature_cols: list) -> pd.DataFrame:
    """
    Convert raw input dict into a properly formatted
    DataFrame that matches the model's expected features.
    """

    # Initialize all features as 0
    df = pd.DataFrame([{col: 0 for col in feature_cols}])

    # ── Numerical Features ────────────────────────────
    numerical_map = {
        "land_size_m2"    : input_data["land_size_m2"],
        "building_size_m2": input_data["building_size_m2"],
        "bedrooms"        : input_data["bedrooms"],
        "bathrooms"       : input_data["bathrooms"],
        "floors"          : input_data["floors"],
        "carports"        : input_data["carports"],
        "garages"         : input_data["garages"],
    }

    for col, value in numerical_map.items():
        if col in df.columns:
            df[col] = value

    # ── Categorical Features (One-Hot) ────────────────
    categorical_map = {
        "city_ "             : input_data["city"],
        "district_"          : input_data["district"],
        "property_type_"     : input_data["property_type"],
        "certificate_"       : input_data["certificate"],
        "furnishing_"        : input_data["furnishing"],
        "electricity_"       : input_data["electricity"],
        "property_condition_": input_data["property_condition"],
    }

    for prefix, value in categorical_map.items():
        col = f"{prefix}{value}"
        if col in df.columns:
            df[col] = 1

    return df


# ── Validate Categories ───────────────────────────────
def validate_city(city: str, city_list: list) -> bool:
    """Check if city exists in training data."""
    return city in city_list


def validate_district(district: str, district_list: list) -> bool:
    """Check if district exists in training data."""
    return district in district_list


# ── Format Price ──────────────────────────────────────
def format_price(price: float) -> str:
    """Format price to Indonesian Rupiah string."""
    return f"Rp {price:,.0f}"