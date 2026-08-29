#!/usr/bin/env python3
"""Stand-in for the sensors: one reading from one of ten made-up locations."""

from __future__ import annotations

import time
from secrets import SystemRandom
from typing import Any

LOCATION_COUNT = 10
MIN_TEMPERATURE = -20
MAX_TEMPERATURE = 40

_random = SystemRandom()


def generate_temperature_reading() -> dict[str, Any]:
    """Return one reading: a location, a temperature and a Unix timestamp."""
    location_id = _random.randint(1, LOCATION_COUNT)  # Simulate 10 different locations
    temperature = _random.uniform(
        MIN_TEMPERATURE, MAX_TEMPERATURE
    )  # Temperature range from -20 to 40 degrees Celsius
    timestamp = time.time()  # Current Unix timestamp
    return {
        "location_id": location_id,
        "temperature": round(temperature, 2),
        "timestamp": timestamp,
    }
