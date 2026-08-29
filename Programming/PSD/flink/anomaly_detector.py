#!/usr/bin/env python3
"""Flink job skeleton: read `transactions` and print each one back out.

The detection itself was never written; the job exists to prove the Kafka
source and the pyflink environment are wired up.
"""

from __future__ import annotations

import json
from typing import Any, cast

from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer


def detect_anomalies(transaction: str) -> dict[str, Any]:
    """Parse one transaction. Anomaly detection would go here."""
    return cast("dict[str, Any]", json.loads(transaction))


def main() -> None:
    """Wire the Kafka source to the parser and run the job."""
    env = StreamExecutionEnvironment.get_execution_environment()
    kafka_consumer = FlinkKafkaConsumer(
        topics="transactions",
        deserialization_schema=SimpleStringSchema(),
        properties={
            "bootstrap.servers": "localhost:9092",
            "group.id": "anomaly_detection",
        },
    )

    data_stream = env.add_source(kafka_consumer).map(detect_anomalies)
    data_stream.print()
    env.execute("Anomaly Detection")


if __name__ == "__main__":
    main()
