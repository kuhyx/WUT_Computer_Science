import json
from kafka import KafkaConsumer

# Thresholds
TEMP_TOO_COLD = -10
TEMP_TOO_HOT = 35

def process_temperature_reading(reading):
    temperature = reading['temperature']
    if temperature < TEMP_TOO_COLD:
        alert = f"WARNING: Temperature is too cold! ({temperature}°C)"
    elif temperature > TEMP_TOO_HOT:
        alert = f"WARNING: Temperature is too hot! ({temperature}°C)"
    else:
        alert = f"Temperature is normal. ({temperature}°C)"
    return alert

if __name__ == '__main__':
    consumer = KafkaConsumer(
        'temperature_readings',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest'
    )

    for message in consumer:
        reading = json.loads(message.value)
        alert_message = process_temperature_reading(reading)
        print(alert_message)
