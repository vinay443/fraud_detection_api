import json, httpx
from joblib import load

b = load("models/xgb_fraud.joblib")
payload = {k: 0.0 for k in b["features"]}

for _ in range(50):  # send 50 requests
    r = httpx.post("http://127.0.0.1:8000/predict", json=payload, timeout=5)
    r.raise_for_status()
print("done")
