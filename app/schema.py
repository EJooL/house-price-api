from pydantic import BaseModel, Field, ConfigDict

# ── Input Schema ──────────────────────────────────────
class PropertyInput(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "city"              : "Jakarta Selatan",
                "district"          : "Kebayoran Baru",
                "property_type"     : "rumah",
                "certificate"       : "SHM - Sertifikat Hak Milik",
                "furnishing"        : "furnished",
                "electricity"       : "2200 mah",
                "property_condition": "baru",
                "land_size_m2"      : 150,
                "building_size_m2"  : 120,
                "bedrooms"          : 3,
                "bathrooms"         : 2,
                "floors"            : 2,
                "carports"          : 1,
                "garages"           : 1
            }
        }
    )

    city              : str   = Field(..., description="City name")
    district          : str   = Field(..., description="District name")
    property_type     : str   = Field(..., description="Type of property")
    certificate       : str   = Field(..., description="Certificate type")
    furnishing        : str   = Field(..., description="Furnishing status")
    electricity       : str   = Field(..., description="Electricity capacity")
    property_condition: str   = Field(..., description="Property condition")
    land_size_m2      : float = Field(..., gt=0,       description="Land size in m²")
    building_size_m2  : float = Field(..., gt=0,       description="Building size in m²")
    bedrooms          : int   = Field(..., ge=1, le=20, description="Number of bedrooms")
    bathrooms         : int   = Field(..., ge=1, le=20, description="Number of bathrooms")
    floors            : int   = Field(..., ge=1, le=10, description="Number of floors")
    carports          : int   = Field(..., ge=0, le=10, description="Number of carports")
    garages           : int   = Field(..., ge=0, le=10, description="Number of garages")


# ── Output Schema ─────────────────────────────────────
class PredictionOutput(BaseModel):
    status                   : str
    predicted_price          : float
    predicted_price_formatted: str
    price_range              : dict
    model_version            : str


# ── Info Schema ───────────────────────────────────────
class ModelInfo(BaseModel):
    model     : str
    version   : str
    r2_score  : float
    mae       : int
    features  : int
    cities    : int
    districts : int