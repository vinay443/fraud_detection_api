import os, joblib

MODEL_PATH = os.environ.get("MODEL_PATH", "models/xgb_fraud.joblib")

# load once at import
bundle = joblib.load(MODEL_PATH)        # rename to 'bundle'
model = bundle["model"]
feature_names = bundle["features"]

def score_one(d: dict) -> float:
    # make sure features are ordered
    x = [d[k] for k in feature_names]
    p = model.predict_proba([x])[0, 1]
    return float(p)

