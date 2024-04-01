import random
import time

def generate_temperature_reading():
    location_id = random.randint(1, 10)  # Simulate 10 different locations
    temperature = random.uniform(-20, 40)  # Temperature range from -20 to 40 degrees Celsius
    timestamp = time.time()  # Current Unix timestamp
    return {
        'location_id': location_id,
        'temperature': round(temperature, 2),
        'timestamp': timestamp
    }
