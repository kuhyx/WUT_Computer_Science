#!/usr/bin/env python3
"""Publish a simulated reading from each of five thermometers, once a second.

The readings go to the Temperatura topic, where the Flink job in
`../processor/` picks them up and republishes the below-zero ones as alarms.
"""

import json
import logging
import sys
import time
from pathlib import Path
from secrets import SystemRandom

from confluent_kafka import Message, Producer

# Add parent directory to path to import model
sys.path.append(str(Path(__file__).resolve().parent.parent))
from model.temperature_reading import TemperatureReading

logger = logging.getLogger(__name__)

# Readings are drawn from this range, so roughly a quarter of them alarm.
MIN_TEMPERATURE = -10
MAX_TEMPERATURE = 30

THERMOMETER_IDS = ["Therm-1", "Therm-2", "Therm-3", "Therm-4", "Therm-5"]

_random = SystemRandom()


def delivery_report(err: object, _msg: Message) -> None:
    """Report a failed delivery; successful ones are not worth a line each."""
    if err is not None:
        logger.error("Message delivery failed: %s", err)
    else:
        pass  # Successfully delivered


def main() -> None:
    """Produce readings until interrupted."""
    # Set up Kafka producer with confluent-kafka
    producer_config = {"bootstrap.servers": "localhost:9092"}
    producer = Producer(producer_config)

    try:
        while True:
            for thermometer_id in THERMOMETER_IDS:
                # Generate a random temperature between -10 and 30 degrees
                temperature = _random.uniform(MIN_TEMPERATURE, MAX_TEMPERATURE)

                # Create reading object
                reading = TemperatureReading(
                    thermometer_id=thermometer_id,
                    timestamp=int(time.time() * 1000),
                    temperature=temperature,
                )

                # Convert to dictionary for JSON serialization
                reading_dict = reading.to_dict()
                payload = json.dumps(reading_dict).encode("utf-8")

                # Send to Kafka topic "Temperatura"
                producer.produce(
                    "Temperatura",
                    key=thermometer_id.encode("utf-8"),
                    value=payload,
                    callback=delivery_report,
                )
                producer.flush(timeout=1)
                logger.debug("Sent: %s", json.dumps(reading_dict))

            # Sleep for a second
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Stopping temperature generator")
    finally:
        # Wait for any outstanding messages to be delivered
        producer.flush()


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    main()
