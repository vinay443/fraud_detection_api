import json, threading, time, httpx, uvicorn
from src.serve.app import app

def run_app():
    uvicorn.run(app, host="127.0.0.1", port=8010, log_level="error")

def test_health_and_predict():
    t = threading.Thread(target=run_app, daemon=True); t.start()
    time.sleep(0.8)

    r = httpx.get("http://127.0.0.1:8010/healthz", timeout=5)
    assert r.status_code == 200 and r.json()["ok"] is True

    # zero-vector payload
    from joblib import load
    feats = load("models/xgb_fraud.joblib")["features"]
    payload = {k: 0.0 for k in feats}

    r = httpx.post("http://127.0.0.1:8010/predict", json=payload, timeout=5)
    assert r.status_code == 200
    body = r.json()
    assert "fraud_probability" in body and "latency_ms" in body
