#!/usr/bin/env python3
"""Read the temperature_readings topic and shout about the extremes."""

from __future__ import annotations

import json
import logging
from typing import Any

from kafka import KafkaConsumer

logger = logging.getLogger(__name__)

# Thresholds
TEMP_TOO_COLD = -10
TEMP_TOO_HOT = 35


def process_temperature_reading(reading: dict[str, Any]) -> str:
    """Return the line to print for one reading."""
    temperature = reading["temperature"]
    if temperature < TEMP_TOO_COLD:
        alert = f"WARNING: Temperature is too cold! ({temperature}°C)"
    elif temperature > TEMP_TOO_HOT:
        alert = f"WARNING: Temperature is too hot! ({temperature}°C)"
    else:
        alert = f"Temperature is normal. ({temperature}°C)"
    return alert


def main() -> None:
    """Consume readings until interrupted."""
    consumer = KafkaConsumer(
        "temperature_readings",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
    )

    for message in consumer:
        reading = json.loads(message.value)
        logger.info("%s", process_temperature_reading(reading))


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    main()
