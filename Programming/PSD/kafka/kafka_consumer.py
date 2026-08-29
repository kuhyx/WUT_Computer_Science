#!/usr/bin/env python3
"""Print everything on the `transactions` topic until the partition ends."""

from __future__ import annotations

import logging

from confluent_kafka import Consumer

logger = logging.getLogger(__name__)

# confluent-kafka names this error _PARTITION_EOF, leading underscore and all.
# `KafkaError.name()` is the public way to ask for it without reaching into a
# private attribute; it returns exactly this string.
PARTITION_EOF = "_PARTITION_EOF"


def main() -> None:
    """Consume until a broker error other than end-of-partition arrives."""
    conf = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "test_group",
        "auto.offset.reset": "earliest",
    }

    consumer = Consumer(**conf)
    consumer.subscribe(["transactions"])

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            error = msg.error()
            if error is not None:
                if error.name() == PARTITION_EOF:
                    continue
                logger.error("%s", error)
                break
            value = msg.value()
            if value is not None:
                logger.info("Received message: %s", value.decode("utf-8"))
    finally:
        consumer.close()


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    main()
