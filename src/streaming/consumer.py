# Consume messages and score each using the trained model
import json
from kafka import KafkaConsumer
from src.serve.model_io import score_one, feature_names

TOPIC = "transactions"
BOOT = "127.0.0.1:9092"
THRESH = 0.9

def main():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOT,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="fraud-consumers",
    )
    for msg in consumer:
        d = msg.value
        if not all(k in d for k in feature_names):
            continue
        p = score_one(d)
        print({"p": round(p, 6), "flag": p >= THRESH})

if __name__ == "__main__":
    main()
