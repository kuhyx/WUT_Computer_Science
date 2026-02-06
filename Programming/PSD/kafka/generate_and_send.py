from confluent_kafka import Producer
import json
import random
import time

# Configuration for Kafka Producer
conf = {'bootstrap.servers': "localhost:9092"}
producer = Producer(**conf)

def generate_transaction():
    return {
        "card_id": random.randint(1000, 9999),
        "user_id": random.randint(100, 999),
        "location": {
            "latitude": round(random.uniform(-90, 90), 6),
            "longitude": round(random.uniform(-180, 180), 6)
        },
        "transaction_value": round(random.uniform(1, 1000), 2),
        "spending_limit": round(random.uniform(1000, 5000), 2)
    }

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

while True:
    transaction = generate_transaction()
    producer.produce('transactions', key=str(transaction["card_id"]), value=json.dumps(transaction), callback=delivery_report)
    producer.poll(1)
    time.sleep(1)  # Adjust the sleep time to control the frequency of transactions
