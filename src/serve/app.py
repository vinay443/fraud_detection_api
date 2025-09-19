from fastapi import FastAPI, HTTPException, Response
from pydantic import RootModel
from .model_io import score_one, feature_names
import time, logging, sys, structlog
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="fraud-rt")

# logging (JSON)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
structlog.configure(processors=[structlog.processors.JSONRenderer()])
log = structlog.get_logger()

# metrics
PRED_COUNT = Counter("pred_total", "Total predictions")
PRED_LAT = Histogram("pred_latency_seconds", "Prediction latency")

class Txn(RootModel[dict]): pass

@app.get("/healthz")
def health():
    return {"ok": True}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/predict")
def predict(t: Txn):
    d = t.root
    missing = [k for k in feature_names if k not in d]
    if missing:
        raise HTTPException(status_code=400, detail={"missing": missing})
    t0 = time.perf_counter()
    p = score_one(d)
    dt = time.perf_counter() - t0
    PRED_COUNT.inc()
    PRED_LAT.observe(dt)
    log.info("scored", prob=p, latency_ms=round(dt*1000,2))
    return {"fraud_probability": p, "latency_ms": round(dt*1000, 2)}
