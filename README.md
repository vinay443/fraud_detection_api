# Real-Time Fraud Detection API

Production-style MLOps project: train XGBoost on the Kaggle credit-card dataset, serve a FastAPI `/predict`, stream with Kafka/Redpanda, containerize with Docker, monitor via Prometheus/Grafana, and test with pytest.

## Quick start

### Setup
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```


###Train
```python -m src.training.train
# model saved to models/xgb_fraud.joblib
```

###Serve API
python -m uvicorn src.serve.app:app --host 127.0.0.1 --port 8000 --reload
# Health:  http://127.0.0.1:8000/healthz
# Docs:    http://127.0.0.1:8000/docs

###Test
python -m pytest -q


###Example Predict
from joblib import load
import httpx
bundle = load("models/xgb_fraud.joblib")
payload = {k: 0.0 for k in bundle["features"]}
print(httpx.post("http://127.0.0.1:8000/predict", json=payload).json())


##Streaming (local Redpanda)

###Start Broker (Docker):
docker run -d --name redpanda -p 9092:9092 -p 9644:9644 ^
  docker.redpanda.com/redpandadata/redpanda:latest ^
  redpanda start --overprovisioned --smp 1 --memory 1G --reserve-memory 0M ^
  --node-id 0 --check=false --kafka-addr 0.0.0.0:9092 --advertise-kafka-addr 127.0.0.1:9092


###Run Consumer and Producer
python -m src.streaming.consumer
python -m src.streaming.producer


##Docker

###Build
docker build -f docker/Dockerfile.train -t fraud-train:0.1 .
docker build -f docker/Dockerfile.serve -t fraud-serve:0.1 .

###Train inside container
mkdir models
docker run --rm -v "%CD%\models:/app/models" fraud-train:0.1

###Serve inside container
docker run --rm -p 8080:8000 -v "%CD%\models:/app/models:ro" fraud-serve:0.1
# http://127.0.0.1:8080/healthz


##Monitoring

###Prometheus config (prometheus.yml)
global: { scrape_interval: 5s }
scrape_configs:
  - job_name: fraud-api
    static_configs:
      - targets: ["host.docker.internal:8000"]
        labels: { service: fraud-api }

###Run Prometheus
docker run --rm -p 9090:9090 -v "%CD%\prometheus.yml:/etc/prometheus/prometheus.yml" prom/prometheus

###Run Graphana
docker run -d --name grafana -p 3000:3000 grafana/grafana
# Add Prometheus DS: http://host.docker.internal:9090


##Repo Layout
src/
  training/train.py
  serve/app.py, model_io.py
  streaming/producer.py, consumer.py
docker/
tests/
models/   # trained artifact (git-ignored)
data/     # dataset (git-ignored)

##Notes

---

👉 Copy all of that into `README.md`.  
Then run:

```cmd
git add README.md
git commit -m "docs: add complete README"
git push

