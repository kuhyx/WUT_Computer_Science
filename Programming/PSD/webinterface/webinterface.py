#!/usr/bin/env python3
"""A one-route Flask app that drains the `alarms` topic and returns it as JSON."""

from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING

from confluent_kafka import Consumer
from flask import Flask, jsonify

if TYPE_CHECKING:
    from flask.typing import ResponseReturnValue

app = Flask(__name__)

# confluent-kafka names this error _PARTITION_EOF, leading underscore and all.
# `KafkaError.name()` is the public way to ask for it without reaching into a
# private attribute; it returns exactly this string.
PARTITION_EOF = "_PARTITION_EOF"

HTTP_INTERNAL_SERVER_ERROR = 500


@app.route("/alarms", methods=["GET"])
def get_alarms() -> ResponseReturnValue:
    """Return every alarm currently on the topic, oldest first."""
    alarms = []
    conf = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "alarm_group",
        "auto.offset.reset": "earliest",
    }

    consumer = Consumer(**conf)
    consumer.subscribe(["alarms"])

    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            break
        error = msg.error()
        if error is not None:
            if error.name() == PARTITION_EOF:
                continue
            return str(error), HTTP_INTERNAL_SERVER_ERROR
        value = msg.value()
        if value is not None:
            alarms.append(json.loads(value.decode("utf-8")))

    consumer.close()
    return jsonify(alarms)


if __name__ == "__main__":
    # Debug mode serves a console that executes arbitrary code, so it is opt-in
    # rather than the default it used to be here.
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
