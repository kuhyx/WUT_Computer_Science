import json
import random
import time
from kafka import KafkaProducer
from simulate_temperature_sensor import generate_temperature_reading

def serializer(message):
    return json.dumps(message).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer
)

if __name__ == '__main__':
    while True:
        reading = generate_temperature_reading()
        print(f"Sending reading: {reading}")
        producer.send('temperature_readings', reading)
        time.sleep(random.randint(1, 5))  # Simulate readings sent at random intervals
