#!/usr/bin/env python3
"""Push made-up card transactions to the `transactions` topic once a second."""

from __future__ import annotations

import json
import logging
import time
from secrets import SystemRandom
from typing import Any

from confluent_kafka import Message, Producer

logger = logging.getLogger(__name__)

_random = SystemRandom()


def generate_transaction() -> dict[str, Any]:
    """Return one transaction with a random card, place and amount."""
    return {
        "card_id": _random.randint(1000, 9999),
        "user_id": _random.randint(100, 999),
        "location": {
            "latitude": round(_random.uniform(-90, 90), 6),
            "longitude": round(_random.uniform(-180, 180), 6),
        },
        "transaction_value": round(_random.uniform(1, 1000), 2),
        "spending_limit": round(_random.uniform(1000, 5000), 2),
    }


def delivery_report(err: object, msg: Message) -> None:
    """Log whether one message made it to the broker."""
    if err is not None:
        logger.error("Message delivery failed: %s", err)
    else:
        logger.info("Message delivered to %s [%s]", msg.topic(), msg.partition())


def main() -> None:
    """Produce transactions until interrupted."""
    # Configuration for Kafka Producer
    conf = {"bootstrap.servers": "localhost:9092"}
    producer = Producer(**conf)

    while True:
        transaction = generate_transaction()
        producer.produce(
            "transactions",
            key=str(transaction["card_id"]),
            value=json.dumps(transaction),
            callback=delivery_report,
        )
        producer.poll(1)
        # Adjust the sleep time to control the frequency of transactions
        time.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    main()
