#!/usr/bin/env python3
"""The alarm the detector publishes to the Alarm topic."""

from __future__ import annotations

from typing import Any


class TemperatureAlarm:
    """One below-zero reading: who reported it, when, and how cold."""

    def __init__(
        self,
        thermometer_id: str | None = None,
        timestamp: int | None = None,
        temperature: float | None = None,
    ) -> None:
        """Store the three fields, all optional so a partial message still parses."""
        self.thermometer_id = thermometer_id
        self.timestamp = timestamp
        self.temperature = temperature

    def to_dict(self) -> dict[str, Any]:
        """Return the camelCase form that goes on the wire."""
        return {
            "thermometerId": self.thermometer_id,
            "timestamp": self.timestamp,
            "temperature": self.temperature,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TemperatureAlarm:
        """Build an alarm from the camelCase form that came off the wire."""
        return cls(
            thermometer_id=data.get("thermometerId"),
            timestamp=data.get("timestamp"),
            temperature=data.get("temperature"),
        )
