# Send rows from CSV into Kafka topic
import time, json, pandas as pd
from kafka import KafkaProducer

TOPIC = "transactions"
BOOT = "127.0.0.1:9092"

def main():
    producer = KafkaProducer(
        bootstrap_servers=BOOT,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        linger_ms=10,
        acks="1",
    )
    df = pd.read_csv("data/creditcard.csv").drop(columns=["Class"]).head(20)
    time.sleep(0.02)
    for _, row in df.iterrows():
        producer.send(TOPIC, row.to_dict())
        time.sleep(0.01)  # ~100 per second
    producer.flush()

if __name__ == "__main__":
    main()
