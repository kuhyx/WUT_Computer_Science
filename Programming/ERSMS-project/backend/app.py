#!/usr/bin/env python3
"""The Firebase-authenticated API: log in, rate a movie, look films up on TMDB.

Every route takes a Firebase ID token in the request body, verifies it, and
uses the uid inside it as the identity. Ratings live in a local SQLite file;
film metadata is proxied from TMDB.
"""

from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

import firebase_admin
import requests
from dotenv import load_dotenv
from firebase_admin import auth, credentials, exceptions
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import Base, Rating, User
from sqlalchemy.exc import SQLAlchemyError

if TYPE_CHECKING:
    from flask.typing import ResponseReturnValue

logger = logging.getLogger(__name__)

load_dotenv()
TMDB_BEARER_TOKEN = os.getenv("TMDB_BEARER_TOKEN")

# TMDB is a third party over the internet; never wait on it indefinitely.
TMDB_TIMEOUT_SECONDS = 10

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_UNAUTHORIZED = 401
HTTP_INTERNAL_SERVER_ERROR = 500

# A token that will not verify, and a request the token owner may not make.
AUTH_ERRORS = (exceptions.FirebaseError, ValueError, KeyError)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.sqlite3"
app.config["SQLALCHEY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app, model_class=Base)

CORS(app)

cred = credentials.Certificate("movie-recommendation-firebase-adminsdk.json")
firebase_admin.initialize_app(cred)


with app.app_context():
    db.create_all()


@app.route("/login", methods=["POST"])
def login() -> ResponseReturnValue:
    """Verify the token and create the user row if this is their first visit."""
    token = request.json.get("token")
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token["uid"]
        logger.info("login: %s", uid)
        email = decoded_token.get("email")

        user = db.session.scalars(db.select(User).filter_by(uid=uid)).first()
        if user is None:
            user = User(uid=uid, email=email)

            db.session.add(user)
            db.session.commit()
    except (*AUTH_ERRORS, SQLAlchemyError):
        logger.exception("Login failed")
        return jsonify({"message": "Login failed"}), HTTP_UNAUTHORIZED
    return jsonify(
        {"message": "Login successful!", "email": email, "is_admin": user.is_admin}
    ), HTTP_OK


@app.route("/count_user_ratings", methods=["POST"])
def count_user_ratings() -> ResponseReturnValue:
    """Return how many films this user has rated."""
    token = request.json.get("token")
    try:
        decoded_token = auth.verify_id_token(token)
        user_id = decoded_token["uid"]

        user = db.session.scalars(db.select(User).filter_by(uid=user_id)).first()
        if user is None:
            return jsonify({"message": "Error"}), HTTP_INTERNAL_SERVER_ERROR

        rating_count = db.session.scalar(
            db.select(db.func.count()).select_from(Rating).filter_by(user_id=user_id)
        )
    except (*AUTH_ERRORS, SQLAlchemyError) as exc:
        logger.exception("Could not count ratings")
        return jsonify({"message": str(exc)}), HTTP_INTERNAL_SERVER_ERROR
    return jsonify(
        {"message": "Ratings counted!", "rating_count": rating_count}
    ), HTTP_OK


@app.route("/movie/<int:movie_id>", methods=["GET"])
def get_tmdb_data_movie_id(movie_id: int) -> ResponseReturnValue:
    """Proxy one film's TMDB record."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    headers = {"Authorization": f"Bearer {TMDB_BEARER_TOKEN}"}

    try:
        response = requests.get(url, headers=headers, timeout=TMDB_TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.exception("TMDB lookup failed for %s", movie_id)
        return jsonify({"message": str(exc)}), HTTP_INTERNAL_SERVER_ERROR
    return jsonify(response.json()), HTTP_OK


@app.route("/movie", methods=["GET"])
def get_tmdb_data_query() -> ResponseReturnValue:
    """Search TMDB, or return what is trending today when there is no query."""
    query = request.args.get("query")

    if query:
        url = f"https://api.themoviedb.org/3/search/movie?query={query}"
    else:
        url = "https://api.themoviedb.org/3/trending/movie/day"

    headers = {"Authorization": f"Bearer {TMDB_BEARER_TOKEN}"}

    try:
        response = requests.get(url, headers=headers, timeout=TMDB_TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.exception("TMDB search failed")
        return jsonify({"message": str(exc)}), HTTP_INTERNAL_SERVER_ERROR
    return jsonify(response.json()), HTTP_OK


@app.route("/rating", methods=["POST"])
def add_rating() -> ResponseReturnValue:
    """Record this user's score for a film, or update it if they had one."""
    token = request.json.get("token")
    movie = request.json.get("movie")
    value = request.json.get("value")
    try:
        decoded_token = auth.verify_id_token(token)
        user_id = decoded_token["uid"]

        rating = db.session.scalars(
            db.select(Rating).filter_by(user_id=user_id, movie_id=movie)
        ).first()
        if rating is None:
            rating = Rating(user_id=user_id, movie_id=movie, value=value)

            db.session.add(rating)
            db.session.commit()

            return jsonify({"message": "Rating added successfully!"}), HTTP_CREATED
        rating.value = value

        db.session.commit()
    except (*AUTH_ERRORS, SQLAlchemyError) as exc:
        logger.exception("Could not add rating")
        return jsonify({"message": str(exc)}), HTTP_INTERNAL_SERVER_ERROR
    return jsonify({"message": "Rating updated successfully!"}), HTTP_OK


@app.route("/rating", methods=["DELETE"])
def remove_rating() -> ResponseReturnValue:
    """Delete this user's score for a film."""
    token = request.json.get("token")
    movie = request.json.get("movie")
    try:
        decoded_token = auth.verify_id_token(token)
        user_id = decoded_token["uid"]

        rating = db.session.scalars(
            db.select(Rating).filter_by(user_id=user_id, movie_id=movie)
        ).first()
        if rating is None:
            return jsonify({"message": "Error"}), HTTP_INTERNAL_SERVER_ERROR

        db.session.delete(rating)
        db.session.commit()
    except (*AUTH_ERRORS, SQLAlchemyError) as exc:
        logger.exception("Could not remove rating")
        return jsonify({"message": str(exc)}), HTTP_INTERNAL_SERVER_ERROR
    return jsonify({"message": "Rating removed successfully!"}), HTTP_OK


@app.route("/get_rating", methods=["POST"])
def get_rating() -> ResponseReturnValue:
    """Return this user's score for a film, if they have given one."""
    token = request.json.get("token")
    movie = request.json.get("movie")
    try:
        decoded_token = auth.verify_id_token(token)
        user_id = decoded_token["uid"]

        rating = db.session.scalars(
            db.select(Rating).filter_by(user_id=user_id, movie_id=movie)
        ).first()
        if rating is None:
            return jsonify({"message": "Rating not found!"}), HTTP_OK
    except (*AUTH_ERRORS, SQLAlchemyError) as exc:
        logger.exception("Could not read rating")
        return jsonify({"message": str(exc)}), HTTP_INTERNAL_SERVER_ERROR
    return jsonify(
        {
            "message": "Rating found!",
            "movie": rating.movie_id,
            "value": rating.value,
        }
    ), HTTP_OK


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    # Inside a container the service must bind every interface or the
    # published port is unreachable, so docker-compose sets ERSMS_HOST. The
    # default is loopback, which is the safe thing to do outside Docker.
    app.run(host=os.environ.get("ERSMS_HOST", "127.0.0.1"), port=8084)
