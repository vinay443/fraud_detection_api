import httpx, json
from joblib import load

bundle = load("models/xgb_fraud.joblib")
features = bundle["features"]
payload = {k: 0.0 for k in features}

r = httpx.post("https://127.0.0.1:8000/predict", json = payload, timeout = 10)
print("Status: ", r.status_code)
print("Body: ", r.json())