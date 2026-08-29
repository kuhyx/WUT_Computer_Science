#!/usr/bin/env python3
"""The API the frontend talks to: users, ratings, and film metadata.

Every query is parameterised. They used to be f-strings holding a username or
an OAuth id straight out of the URL, which meant any caller could end the
statement and append their own.
"""

from __future__ import annotations

import json
import logging
import os
import time
from configparser import ConfigParser
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING

import pandas as pd
import psycopg2
import requests
from flask import Flask, jsonify
from flask_caching import Cache

if TYPE_CHECKING:
    from flask.typing import ResponseReturnValue

logger = logging.getLogger(__name__)

HTTP_OK = 200
HTTP_NOT_FOUND = 404
HTTP_CONFLICT = 409
HTTP_BAD_REQUEST = 400
HTTP_INTERNAL_SERVER_ERROR = 500

MIN_RATING = 1
MAX_RATING = 5

# The recommender is a sibling container; never wait on it indefinitely.
RECOMMENDER_TIMEOUT_SECONDS = 30

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

    def commit(self) -> None:
        """Commit the current transaction."""
        if self.conn is None:
            msg = "the database connection was never opened"
            raise RuntimeError(msg)
        self.conn.commit()


@dataclass
class Movies:
    """The film metadata table, read from CSV once at start-up."""

    frame: pd.DataFrame | None = None

    def rows(self) -> pd.DataFrame:
        """Return the table, or fail loudly if start-up never loaded it."""
        if self.frame is None:
            msg = "the movie list was never loaded"
            raise RuntimeError(msg)
        return self.frame


app = Flask(__name__)
cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
DB = Database()
MOVIES = Movies()


@app.route("/", methods=["GET"])
@cache.cached(timeout=69)
def hello() -> ResponseReturnValue:
    """Liveness check."""
    return jsonify(
        {"response": "Hello there", "time": datetime.now(tz=timezone.utc)}
    ), HTTP_OK


# endpoint do wyciągania danych o userze
@app.route("/api/v3/get/<string:username>", methods=["GET"])
def access_user(username: str) -> ResponseReturnValue:
    """Return the row for one username."""
    cursor = DB.cursor()
    cursor.execute("select * from users where username=%s;", (username,))
    res = cursor.fetchall()

    cursor.close()

    return jsonify(res[0]), HTTP_OK


# endpoint służący do zapisu danych nowo stworzonego użytkownika, podajemy mu
# id z oautha oraz login
@app.route("/api/v3/add/<string:oauth_id>/<string:username>", methods=["POST"])
def add_user(oauth_id: str, username: str) -> ResponseReturnValue:
    """Create a user, unless that username is taken."""
    cursor = DB.cursor()
    cursor.execute("select * from users where username=%s;", (username,))
    res = cursor.fetchall()

    if len(res):
        cursor.close()
        return jsonify({"status": "User already exists"}), HTTP_CONFLICT

    cursor.execute(
        "INSERT INTO users (username, oauth_ID) VALUES (%s, %s);",
        (username, oauth_id),
    )

    DB.commit()
    cursor.close()

    return jsonify({"status": "success"}), HTTP_OK


# roboczy endpoint służący do wyciąganiu rekomendacji
@app.route("/api/v3/ai/<string:oauth_id>", methods=["GET"])
def get_recommendations(oauth_id: str) -> ResponseReturnValue:
    """Ask the recommender for films to suggest to this user."""
    cursor = DB.cursor()
    cursor.execute("select movie_ID from ratings where oauth_ID=%s;", (oauth_id,))
    res = cursor.fetchall()
    cursor.close()

    movies = [int(row[0]) for row in res]
    url = "http://localhost:8081/api/v3/AI_recommendations"
    try:
        response = requests.post(
            url,
            json=movies,
            headers={"Content-Type": "application/json"},
            timeout=RECOMMENDER_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.exception("Recommender call failed")
        return jsonify({"status": str(exc)}), HTTP_INTERNAL_SERVER_ERROR
    return jsonify(response.json()), HTTP_OK


@app.route("/api/v3/get_movie/<int:movie_id>", methods=["GET"])
def get_movie(movie_id: int) -> ResponseReturnValue:
    """Return one film's title, cast and crew."""
    rows = MOVIES.rows()
    movie_info = rows.loc[rows["movie_id"] == movie_id]
    if movie_info.empty:
        return jsonify(
            {"status": f"Movie with ID {movie_id} doesn't exist"}
        ), HTTP_NOT_FOUND

    cast = json.loads(movie_info["cast"][0].replace('\\"', '"'))
    crew = json.loads(movie_info["crew"][0].replace('\\"', '"'))

    output_json = {
        "movie_id": movie_id,
        "title": movie_info["title"][0],
        "cast": cast,
        "crew": crew,
    }

    return jsonify(output_json), HTTP_OK


@app.route(
    "/api/v3/rate_movie/<string:user_id>/<string:movie_id>/<int:rating>",
    methods=["POST"],
)
def rate_movie(user_id: str, movie_id: str, rating: int) -> ResponseReturnValue:
    """Record or update this user's rating for a film."""
    rows = MOVIES.rows()
    movie_info = rows.loc[rows["movie_id"] == int(movie_id)]
    if movie_info.empty:
        return jsonify(
            {"status": f"Movie with ID {movie_id} doesn't exist"}
        ), HTTP_NOT_FOUND

    if rating < MIN_RATING or rating > MAX_RATING:
        return jsonify({"status": "Incorrect rating"}), HTTP_BAD_REQUEST

    cursor = DB.cursor()
    cursor.execute("select * from users where oauth_ID=%s;", (user_id,))
    res = cursor.fetchall()

    if not len(res):
        cursor.close()
        return jsonify({"status": "User doesn't exists"}), HTTP_NOT_FOUND

    cursor.execute(
        "select * from ratings where oauth_ID=%s AND movie_ID=%s;",
        (user_id, movie_id),
    )
    res = cursor.fetchall()

    if len(res):
        cursor.execute(
            """UPDATE ratings
               SET rating = %s,
                   rdate = CURRENT_TIMESTAMP
               WHERE oauth_ID = %s AND
                     movie_ID = %s
            """,
            (rating, user_id, movie_id),
        )
    else:
        cursor.execute(
            "INSERT INTO ratings (movie_ID, oauth_ID, rating) VALUES (%s, %s, %s);",
            (movie_id, user_id, rating),
        )

    DB.commit()
    cursor.close()

    return jsonify({"status": "success"}), HTTP_OK


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
    """Connect, load the film table, and serve until stopped."""
    config = ConfigParser()
    config.read("init_scripts/constants.ini")
    DB.conn = connect_with_retry(config)

    MOVIES.frame = pd.read_csv(config["movie"]["csv_path"])
    cache.init_app(app)
    try:
        # docker-compose sets ERSMS_HOST; see backend/app.py for why.
        app.run(
            host=os.environ.get("ERSMS_HOST", "127.0.0.1"),
            port=8090,
            debug=os.environ.get("FLASK_DEBUG") == "1",
        )
    finally:
        DB.conn.close()


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    main()
