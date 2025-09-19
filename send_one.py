import json
from kafka import KafkaProducer
from joblib import load

b = load("models/xgb_fraud.joblib")
payload = {k: 0.0 for k in b["features"]}

p = KafkaProducer(bootstrap_servers="127.0.0.1:9092",
                  value_serializer=lambda v: json.dumps(v).encode())
p.send("transactions", payload)
p.flush()
print("sent")
