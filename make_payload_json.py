import json
from joblib import load
b = load("models/xgb_fraud.joblib")
features = b["features"]
payload = {k: 0.0 for k in features}   # simple smoke test payload
print(json.dumps(payload))
