import json
import random
import time
from confluent_kafka import Producer
import sys
import os

# Add parent directory to path to import model
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.temperature_reading import TemperatureReading

def delivery_report(err, msg):
    """Callback for message delivery reports"""
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        pass  # Successfully delivered

def main():
    # Set up Kafka producer with confluent-kafka
    producer_config = {
        'bootstrap.servers': 'localhost:9092'
    }
    producer = Producer(producer_config)
    
    # Generate a fixed number of thermometer IDs
    thermometer_ids = ["Therm-1", "Therm-2", "Therm-3", "Therm-4", "Therm-5"]
    
    try:
        while True:
            for thermometer_id in thermometer_ids:
                # Generate a random temperature between -10 and 30 degrees
                temperature = random.uniform(-10, 30)
                
                # Create reading object
                reading = TemperatureReading(
                    thermometer_id=thermometer_id,
                    timestamp=int(time.time() * 1000),
                    temperature=temperature
                )
                
                # Convert to dictionary for JSON serialization
                reading_dict = reading.to_dict()
                payload = json.dumps(reading_dict).encode('utf-8')
                
                # Send to Kafka topic "Temperatura"
                producer.produce(
                    "Temperatura", 
                    key=thermometer_id.encode('utf-8'), 
                    value=payload,
                    callback=delivery_report
                )
                producer.flush(timeout=1)
                # print(f"Sent: {json.dumps(reading_dict)}")
            
            # Sleep for a second
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("Stopping temperature generator")
    finally:
        # Wait for any outstanding messages to be delivered
        producer.flush()

if __name__ == "__main__":
    main()
