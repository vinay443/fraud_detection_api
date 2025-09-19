# Real-Time Fraud Detection API

Production-style MLOps project: train XGBoost on the Kaggle credit-card dataset, serve a FastAPI `/predict`, stream with Kafka/Redpanda, containerize with Docker, monitor via Prometheus/Grafana, and test with pytest.

## Quick start

### Setup
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
