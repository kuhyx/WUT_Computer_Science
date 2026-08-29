#!/usr/bin/env python3
"""Send a simulated reading to the temperature_readings topic, now and then."""

from __future__ import annotations

import json
import logging
import time
from secrets import SystemRandom
from typing import Any

from kafka import KafkaProducer
from simulate_temperature_sensor import generate_temperature_reading

logger = logging.getLogger(__name__)

MIN_INTERVAL_SECONDS = 1
MAX_INTERVAL_SECONDS = 5

_random = SystemRandom()


def serializer(message: dict[str, Any]) -> bytes:
    """Encode one message as UTF-8 JSON for Kafka."""
    return json.dumps(message).encode("utf-8")


def main() -> None:
    """Produce readings until interrupted."""
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"], value_serializer=serializer
    )
    while True:
        reading = generate_temperature_reading()
        logger.info("Sending reading: %s", reading)
        producer.send("temperature_readings", reading)
        # Simulate readings sent at random intervals
        time.sleep(_random.randint(MIN_INTERVAL_SECONDS, MAX_INTERVAL_SECONDS))


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    main()
