#!/usr/bin/env python3
"""Flink job: read the Temperatura topic and republish below-zero readings.

Run it against a local Kafka on 9092. The connector JARs are not bundled with
pyflink, so `add_kafka_dependencies` points the environment at a Kafka and a
Flink install and reports precisely which JAR is missing when one is.
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.datastream.functions import KeyedProcessFunction, MapFunction

if TYPE_CHECKING:
    from collections.abc import Iterator

# Add parent directory to path to import model
sys.path.append(str(Path(__file__).resolve().parent.parent))

logger = logging.getLogger(__name__)

# A reading at or below this temperature is what the job is looking for.
ALARM_TEMPERATURE = 0.0

# Where the Kafka and Flink installs live on the lab machine.
KAFKA_LIB_PATH = Path("/home/psd/Downloads/kafka_2.13-3.4.0/libs")
FLINK_LIB_PATH = Path("/home/psd/Downloads/flink-1.17.0/lib")
KAFKA_CLIENTS_JAR = "kafka-clients-3.4.0.jar"


class ReadingMapFunction(MapFunction):
    """Turn a JSON reading into the (id, timestamp, temperature) tuple."""

    def map(self, value: str) -> tuple[str, int, float]:
        """Parse one message off the Temperatura topic."""
        data = json.loads(value)
        return (data["thermometerId"], data["timestamp"], data["temperature"])


class AnomalyDetectionFunction(KeyedProcessFunction):
    """Emit an alarm for every reading below zero."""

    def __init__(self) -> None:
        """Set the window the job was written around."""
        self.window_size = 10 * 1000  # 10 seconds in milliseconds

    def process_element(
        self, value: tuple[str, int, float], ctx: object
    ) -> Iterator[str]:
        """Yield a JSON alarm when `value` is below zero, otherwise nothing."""
        del ctx
        thermometer_id, timestamp, temperature = value

        # Check if temperature is below zero (anomaly)
        if temperature < ALARM_TEMPERATURE:
            # Create alarm
            alarm = {
                "thermometerId": thermometer_id,
                "timestamp": timestamp,
                "temperature": temperature,
            }
            yield json.dumps(alarm)


def add_kafka_dependencies(env: StreamExecutionEnvironment) -> None:
    """Add Kafka connector dependencies to the environment."""
    jar_paths = []

    # Add kafka-clients JAR
    clients_jar = KAFKA_LIB_PATH / KAFKA_CLIENTS_JAR
    if clients_jar.exists():
        jar_paths.append(f"file://{clients_jar}")
    else:
        logger.warning("Could not find Kafka clients JAR at %s", clients_jar)

    # Try to find Flink Kafka connector JAR
    connector = next(
        (p for p in sorted(FLINK_LIB_PATH.glob("flink-connector-kafka*"))), None
    )
    if connector is not None:
        jar_paths.append(f"file://{connector}")
    else:
        logger.warning(
            "No Flink Kafka connector JAR found. Download one named like "
            "'flink-connector-kafka-1.17.0.jar' from Maven Central or the "
            "Apache Flink website and place it in %s",
            FLINK_LIB_PATH,
        )

    if jar_paths:
        env.get_config().get_configuration().set_string(
            "pipeline.jars", ";".join(jar_paths)
        )
        logger.info("Added JAR files: %s", jar_paths)


def main() -> None:
    """Wire the Kafka source to the detector to the Kafka sink, and run it."""
    # Create execution environment
    env = StreamExecutionEnvironment.get_execution_environment()

    # Add Kafka connector dependencies
    add_kafka_dependencies(env)

    # Configure Kafka consumer
    consumer_props = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "temperature-anomaly-detector",
    }

    # Create Kafka consumer
    consumer = FlinkKafkaConsumer(
        topics=["Temperatura"],
        deserialization_schema=SimpleStringSchema(),
        properties=consumer_props,
    )

    # Configure Kafka producer
    producer_props = {"bootstrap.servers": "localhost:9092"}

    # Create Kafka producer
    producer = FlinkKafkaProducer(
        topic="Alarm",
        serialization_schema=SimpleStringSchema(),
        producer_config=producer_props,
    )

    # Add source and transformations
    env.add_source(consumer).map(
        ReadingMapFunction(),
        output_type=Types.TUPLE([Types.STRING(), Types.LONG(), Types.DOUBLE()]),
    ).assign_timestamps_and_watermarks(
        WatermarkStrategy.for_monotonous_timestamps().with_timestamp_assigner(
            lambda event, _timestamp: event[1]
        )
    ).key_by(lambda x: x[0]).process(AnomalyDetectionFunction()).add_sink(producer)

    # Print the execution plan
    logger.info("%s", env.get_execution_plan())

    # Execute
    env.execute("Temperature Anomaly Detector with Time Windows")


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    main()
