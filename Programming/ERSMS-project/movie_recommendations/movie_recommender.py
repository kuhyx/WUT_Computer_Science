#!/usr/bin/env python3
"""Content-based film recommendations from the TMDB 5000 dataset.

Each film is reduced to a "soup" of its keywords, top three cast members,
director and genres; the recommender then scores films by the cosine
similarity of those soups.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
from ast import literal_eval
from configparser import ConfigParser
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, cast

import numpy as np
import pandas as pd
import psycopg2
from flask import Flask, jsonify, request
from flask_caching import Cache
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

if TYPE_CHECKING:
    from flask.typing import ResponseReturnValue

logger = logging.getLogger(__name__)

# Only the top few cast members say anything useful about a film.
MAX_CAST_MEMBERS = 3

# How many similar films one input film contributes to the pool.
RECOMMENDATION_POOL = 100

# The database container may still be starting when this one is ready.
DB_RETRY_SECONDS = 1


def get_director(crew: list[dict[str, Any]]) -> str | float:
    """Return the director's name, or NaN when the crew list has no director."""
    for member in crew:
        if member["job"] == "Director":
            return cast("str", member["name"])
    return np.nan


def get_list(values: object) -> list[str]:
    """Return at most the first three names from a TMDB list column."""
    if isinstance(values, list):
        names = [item["name"] for item in values]
        if len(names) > MAX_CAST_MEMBERS:
            names = names[:MAX_CAST_MEMBERS]
        return names
    return []


def clean_data(value: object) -> list[str] | str:
    """Lowercase and de-space a name so "Tom Hanks" cannot match "Tom Hardy"."""
    if isinstance(value, list):
        return [str.lower(item.replace(" ", "")) for item in value]
    if isinstance(value, str):
        return str.lower(value.replace(" ", ""))
    return ""


def create_soup(row: pd.Series) -> str:
    """Join one film's keywords, cast, director and genres into one string."""
    return cast(
        "str",
        " ".join(row["keywords"])
        + " "
        + " ".join(row["cast"])
        + " "
        + row["director"]
        + " "
        + " ".join(row["genres"]),
    )


class MovieRecommender:
    """Holds the film table and the film-by-film cosine similarity matrix."""

    def __init__(self) -> None:
        """Start empty; `fit` fills both."""
        self.df: pd.DataFrame | None = None
        self.cosine_sim: np.ndarray | None = None

    def fit(self, credits_file: str, movies_file: str) -> None:
        """Fittuje AI do przekazanych danych.

        :param credits_file: csv z creditsami
        :param movies_file: csv z filmami
        :return: Nic.
        """
        df1 = pd.read_csv(credits_file)
        df2 = pd.read_csv(movies_file)
        df1.columns = ["id", "tittle", "cast", "crew"]
        df2 = df2.merge(df1, on="id")
        df2["overview"] = df2["overview"].fillna("")
        self.df = df2

        features = ["cast", "crew", "keywords", "genres"]
        for feature in features:
            df2[feature] = df2[feature].apply(literal_eval)

        df2["director"] = df2["crew"].apply(get_director)

        features = ["cast", "keywords", "genres"]
        for feature in features:
            df2[feature] = df2[feature].apply(get_list)

        features = ["cast", "keywords", "director", "genres"]
        for feature in features:
            df2[feature] = df2[feature].apply(clean_data)

        df2["soup"] = df2.apply(create_soup, axis=1)

        count = CountVectorizer(stop_words="english")
        count_matrix = count.fit_transform(df2["soup"])
        self.cosine_sim = cosine_similarity(count_matrix, count_matrix)

        self.df = df2.reset_index()

    def _get_recommendations_one_input(
        self, movie_id: int
    ) -> tuple[np.ndarray, np.ndarray]:
        """Tworzy rekomendacje, bazując na jednym filmie.

        :param movie_id: id filmu, dla którego ma zrobić rekomendację
        :return: Para (movie_ids, similarity_scores), obie jako np.array.
        """
        if self.df is None or self.cosine_sim is None:
            msg = "call fit() before asking for recommendations"
            raise RuntimeError(msg)
        indices = pd.Series(self.df.index, index=self.df["id"]).drop_duplicates()
        idx = indices[movie_id]
        sim_scores = sorted(
            enumerate(self.cosine_sim[idx]), key=lambda pair: pair[1], reverse=True
        )
        sim_scores = sim_scores[1 : RECOMMENDATION_POOL + 1]
        movie_indices = [pair[0] for pair in sim_scores]
        scores = np.array([pair[1] for pair in sim_scores])
        return (self.df["id"].iloc[movie_indices].to_numpy(), scores)

    def get_recommendations(self, movie_ids: list[int]) -> dict[int, float]:
        """Tworzy listę rekomendacji bazującą na id podanych filmów.

        :param movie_ids: id filmów, na podstawie których wybiera rekomendacje
        :return: Dict {movie_id: similarity_score}.
        """
        recommended_movies: dict[int, float] = {}
        for movie_id in movie_ids:
            recommended_ids, sim_scores = self._get_recommendations_one_input(movie_id)
            for recommended_id, sim_score in zip(
                recommended_ids, sim_scores, strict=True
            ):
                if recommended_id in movie_ids:
                    continue

                share = float(round(sim_score / len(movie_ids), 4))
                key = int(recommended_id)
                recommended_movies[key] = recommended_movies.get(key, 0.0) + share
        return recommended_movies


@dataclass
class Database:
    """The Postgres connection, opened once at start-up."""

    conn: psycopg2.extensions.connection | None = None


app = Flask(__name__)
cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
DB = Database()
recommender = MovieRecommender()


def make_cache_key() -> str:
    """Key the cache on the sorted request body, so order does not matter."""
    data = request.get_json()
    if isinstance(data, list):
        data = sorted(data)
    # Not a security hash: this only has to be short and stable.
    return hashlib.md5(
        json.dumps(data).encode("utf-8"), usedforsecurity=False
    ).hexdigest()


@app.route("/api/v3/AI_recommendations", methods=["POST"])
@cache.cached(timeout=300, key_prefix=make_cache_key)
def ai_recommendations() -> ResponseReturnValue:
    """Return {movie_id: score} for the film ids posted in the body."""
    ids = request.get_json()
    return jsonify(recommender.get_recommendations(ids))


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
    """Fit the recommender, connect to the database, and serve until stopped."""
    recommender.fit("datasets/tmdb_5000_credits.csv", "datasets/tmdb_5000_movies.csv")

    config = ConfigParser()
    config.read("init_scripts/constants.ini")
    DB.conn = connect_with_retry(config)

    cache.init_app(app)
    try:
        # docker-compose sets ERSMS_HOST; see backend/app.py for why.
        app.run(
            host=os.environ.get("ERSMS_HOST", "127.0.0.1"),
            port=8081,
            debug=os.environ.get("FLASK_DEBUG") == "1",
        )
    finally:
        DB.conn.close()


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    main()
