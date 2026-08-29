#!/usr/bin/env python3
"""Read-only rating statistics over the shared Postgres database.

Every route is cached, because these are dashboard numbers that nobody needs
to the second and each one is a full table scan.
"""

from __future__ import annotations

import logging
import os
import time
from configparser import ConfigParser
from dataclasses import dataclass
from typing import TYPE_CHECKING

import psycopg2
from flask import Flask, jsonify
from flask_caching import Cache

if TYPE_CHECKING:
    from flask.typing import ResponseReturnValue

logger = logging.getLogger(__name__)

HTTP_OK = 200

# The database container may still be starting when this one is ready.
DB_RETRY_SECONDS = 1


@dataclass
class Database:
    """The Postgres connection the routes share, opened once at start-up."""

    conn: psycopg2.extensions.connection | None = None

    def cursor(self) -> psycopg2.extensions.cursor:
        """Return a cursor, or fail loudly if start-up never connected."""
        if self.conn is None:
            msg = "the database connection was never opened"
            raise RuntimeError(msg)
        return self.conn.cursor()


app = Flask(__name__)
cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
DB = Database()


@app.route("/api/get_number_of_ratings", methods=["GET"])
@cache.cached(timeout=500)
def get_number_of_ratings() -> ResponseReturnValue:
    """Return how many ratings exist in total."""
    cursor = DB.cursor()
    cursor.execute("select count(*) as num_of_ratings from ratings")
    res = cursor.fetchall()

    cursor.close()

    return jsonify(res[0]), HTTP_OK


@app.route("/api/get_movie_ratings/<string:movie_id>", methods=["GET"])
@cache.cached(timeout=50)
def get_movie_ratings(movie_id: str) -> ResponseReturnValue:
    """Return how many one- to five-star ratings one film has."""
    cursor = DB.cursor()
    ratings = {}
    rating_values = [5, 4, 3, 2, 1]

    for rating in rating_values:
        cursor.execute(
            """
                SELECT COUNT(*) as count
                FROM ratings
                WHERE rating = %s AND movie_ID = %s;
            """,
            (rating, movie_id),
        )
        result = cursor.fetchone()
        ratings[f"{rating}_star"] = result[0]

    cursor.close()

    return jsonify(ratings), HTTP_OK


@app.route("/api/get_users_number", methods=["GET"])
@cache.cached(timeout=50)
def get_number_of_users() -> ResponseReturnValue:
    """Return how many users are registered."""
    cursor = DB.cursor()
    cursor.execute("select count(*) as num_of_users from users")
    res = cursor.fetchall()

    cursor.close()

    return jsonify(res[0]), HTTP_OK


@app.route("/api/get_movie_rating_avg/<string:movie_id>", methods=["GET"])
@cache.cached(timeout=50)
def get_movie_rating_avg(movie_id: str) -> ResponseReturnValue:
    """Return one film's mean rating."""
    cursor = DB.cursor()
    cursor.execute(
        """
            SELECT AVG(rating) as avg_rating
            FROM ratings
            WHERE movie_ID = %s;
        """,
        (movie_id,),
    )
    res = cursor.fetchall()

    cursor.close()

    return jsonify(res[0]), HTTP_OK


@app.route("/api/get_user_ratings/<string:user_id>", methods=["GET"])
@cache.cached(timeout=50)
def get_user_ratings(user_id: str) -> ResponseReturnValue:
    """Return every rating one user has given."""
    cursor = DB.cursor()
    cursor.execute(
        """
            SELECT movie_ID, rating
            FROM ratings
            WHERE oauth_ID = %s;
        """,
        (user_id,),
    )
    res = cursor.fetchall()

    cursor.close()

    return jsonify(res), HTTP_OK


def try_connect(config: ConfigParser) -> psycopg2.extensions.connection | None:
    """Return a connection, or None if the database is not accepting them yet."""
    try:
        return psycopg2.connect(
            host=config["postgres"]["host"],
            database=config["postgres"]["database"],
            user=config["postgres"]["user"],
            password=config["postgres"]["password"],
            port=int(config["postgres"]["port"]),
        )
    except psycopg2.OperationalError:
        return None


def connect_with_retry(config: ConfigParser) -> psycopg2.extensions.connection:
    """Block until Postgres accepts a connection, then return it."""
    connection = try_connect(config)
    while connection is None:
        logger.info("Trying to connect with database")
        time.sleep(DB_RETRY_SECONDS)
        connection = try_connect(config)
    return connection


def main() -> None:
    """Connect to the database and serve until stopped."""
    config = ConfigParser()
    config.read("init_scripts/constants.ini")
    DB.conn = connect_with_retry(config)

    cache.init_app(app)
    try:
        # docker-compose sets ERSMS_HOST; see backend/app.py for why.
        app.run(
            host=os.environ.get("ERSMS_HOST", "127.0.0.1"),
            port=8082,
            debug=os.environ.get("FLASK_DEBUG") == "1",
        )
    finally:
        DB.conn.close()


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    main()
