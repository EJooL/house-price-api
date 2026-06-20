from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ── Valid payload untuk reuse ─────────────────────────
VALID_PAYLOAD = {
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

# ── General Endpoints ─────────────────────────────────
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "name" in response.json()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_model_info():
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert "model"     in data
    assert "r2_score"  in data
    assert "features"  in data

def test_cities():
    response = client.get("/cities")
    assert response.status_code == 200
    data = response.json()
    assert "cities" in data
    assert len(data["cities"]) > 0

def test_districts():
    response = client.get("/districts")
    assert response.status_code == 200
    data = response.json()
    assert "districts" in data
    assert len(data["districts"]) > 0

# ── Prediction Endpoint ───────────────────────────────
def test_predict_success():
    response = client.post("/predict", json=VALID_PAYLOAD)
    assert response.status_code == 200
    data = response.json()
    assert data["status"]            == "success"
    assert data["predicted_price"]   >  0
    assert "price_range"             in data
    assert "model_version"           in data

def test_predict_invalid_city():
    payload = VALID_PAYLOAD.copy()
    payload["city"] = "Bandung"
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
    assert "not found" in response.json()["detail"]

def test_predict_invalid_district():
    payload = VALID_PAYLOAD.copy()
    payload["district"] = "District Tidak Ada"
    response = client.post("/predict", json=payload)
    assert response.status_code == 422

def test_predict_missing_field():
    response = client.post("/predict", json={"city": "Jakarta Selatan"})
    assert response.status_code == 422

def test_predict_invalid_type():
    payload = VALID_PAYLOAD.copy()
    payload["land_size_m2"] = "seratus"
    response = client.post("/predict", json=payload)
    assert response.status_code == 422

def test_predict_price_range():
    response = client.post("/predict", json=VALID_PAYLOAD)
    data = response.json()
    low  = data["price_range"]["low"]
    high = data["price_range"]["high"]
    assert low < data["predicted_price"] < high