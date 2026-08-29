#!/usr/bin/env python3
"""A Tk window listing the alarms as they arrive on the Alarm topic.

The Kafka consumer runs on a daemon thread and hands each alarm back to the Tk
main loop with `root.after`, because Tk widgets may only be touched from the
thread that created them.
"""

from __future__ import annotations

import json
import logging
import sys
import threading
import tkinter as tk
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from tkinter import ttk

from confluent_kafka import Consumer

# Add parent directory to path to import model
sys.path.append(str(Path(__file__).resolve().parent.parent))
from model.temperature_alarm import TemperatureAlarm

logger = logging.getLogger(__name__)

# Milliseconds per second, for turning the wire timestamp into a datetime.
MILLISECONDS = 1000


class AlarmVisualizer:
    """The window: a scrolling list of alarms and a per-thermometer tally."""

    def __init__(self, root: tk.Tk) -> None:
        """Build the widgets and start consuming."""
        self.root = root
        self.root.title("Temperature Alarm Visualizer")
        self.root.geometry("600x400")

        # Create the list model for alarms
        self.alarm_list = tk.Listbox(root, font=("Courier", 12))
        self.alarm_list.pack(fill=tk.BOTH, expand=True)

        # Create scrollbar
        scrollbar = ttk.Scrollbar(
            self.alarm_list, orient="vertical", command=self.alarm_list.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.alarm_list.config(yscrollcommand=scrollbar.set)

        # Create stats panel
        self.stats_frame = tk.Frame(root)
        self.stats_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.stats_label = tk.Label(self.stats_frame, text="No alarms yet")
        self.stats_label.pack(pady=5)

        # Stats tracking
        self.thermometer_alarm_count: Counter[str] = Counter()
        self.max_alarms = 100

        # Start Kafka consumer in a separate thread
        self.consumer_thread = threading.Thread(target=self.consume_alarms, daemon=True)
        self.consumer_thread.start()

    def consume_alarms(self) -> None:
        """Poll the Alarm topic forever, handing each alarm to the Tk thread."""
        # Set up Kafka consumer with confluent-kafka
        consumer_config = {
            "bootstrap.servers": "localhost:9092",
            "group.id": "alarm-visualizer",
            "auto.offset.reset": "latest",
        }
        consumer = Consumer(consumer_config)
        consumer.subscribe(["Alarm"])

        try:
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    logger.error("Consumer error: %s", msg.error())
                    continue

                # Parse the alarm message
                value = msg.value()
                if value is None:
                    continue
                alarm_data = json.loads(value.decode("utf-8"))
                alarm = TemperatureAlarm.from_dict(alarm_data)
                if alarm.timestamp is None or alarm.thermometer_id is None:
                    logger.warning("Skipping malformed alarm: %s", alarm_data)
                    continue

                # Format the timestamp
                timestamp_dt = datetime.fromtimestamp(
                    alarm.timestamp / MILLISECONDS, tz=timezone.utc
                ).astimezone()
                formatted_date = timestamp_dt.strftime("%Y-%m-%d %H:%M:%S")

                # Create alarm message
                alarm_message = (
                    f"⚠️ ALARM: Thermometer {alarm.thermometer_id} "
                    f"reported {alarm.temperature:.2f}°C at {formatted_date}"
                )

                # Update the UI
                self.root.after(0, self.update_ui, alarm_message, alarm.thermometer_id)

        finally:
            consumer.close()

    def update_ui(self, alarm_message: str, thermometer_id: str) -> None:
        """Insert one alarm at the top of the list and refresh the tally."""
        # Add new alarm to the top of the list
        self.alarm_list.insert(0, alarm_message)

        # Keep list at a reasonable size
        if self.alarm_list.size() > self.max_alarms:
            self.alarm_list.delete(self.max_alarms)

        # Update statistics
        self.thermometer_alarm_count[thermometer_id] += 1

        # Format stats string
        if self.thermometer_alarm_count:
            stats_parts = [
                f"{name}={count}"
                for name, count in self.thermometer_alarm_count.items()
            ]
            stats_text = "Alarm Counts: " + ", ".join(stats_parts)
            self.stats_label.config(text=stats_text)


def main() -> None:
    """Open the window and run the Tk main loop."""
    root = tk.Tk()
    AlarmVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    main()
