from flask import Flask, request, jsonify
from flask_caching import Cache
import psycopg2
import pandas
import json
from configparser import ConfigParser
from datetime import datetime


app = Flask(__name__)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
db_connector = None
conn = None


@app.route("/api/get_number_of_ratings", methods=["GET"])
@cache.cached(timeout=500)
def get_number_of_ratings():
    cursor = conn.cursor()
    cursor.execute("select count(*) as num_of_ratings from ratings")
    res = cursor.fetchall()

    cursor.close()

    return jsonify(res[0]), 200


@app.route("/api/get_movie_ratings/<string:movie_id>", methods=["GET"])
@cache.cached(timeout=50)
def get_movie_ratings(movie_id):
    cursor = conn.cursor()
    ratings = {}
    rating_values = [5, 4, 3, 2, 1]

    for rating in rating_values:
        cursor.execute("""
                SELECT COUNT(*) as count 
                FROM ratings 
                WHERE rating = %s AND movie_ID = %s;
            """, (rating, movie_id))
        result = cursor.fetchone()
        ratings[f'{rating}_star'] = result[0]

    cursor.close()

    return jsonify(ratings), 200


@app.route("/api/get_users_number", methods=["GET"])
@cache.cached(timeout=50)
def get_number_of_users():
    cursor = conn.cursor()
    cursor.execute("select count(*) as num_of_users from users")
    res = cursor.fetchall()

    cursor.close()

    return jsonify(res[0]), 200


@app.route("/api/get_movie_rating_avg/<string:movie_id>", methods=["GET"])
@cache.cached(timeout=50)
def get_movie_rating_avg(movie_id):
    cursor = conn.cursor()
    cursor.execute("""
            SELECT AVG(rating) as avg_rating 
            FROM ratings 
            WHERE movie_ID = %s;
        """, (movie_id,))
    res = cursor.fetchall()

    cursor.close()

    return jsonify(res[0]), 200


@app.route("/api/get_user_ratings/<string:user_id>", methods=["GET"])
@cache.cached(timeout=50)
def get_user_ratings(user_id):
    cursor = conn.cursor()
    cursor.execute("""
            SELECT movie_ID, rating 
            FROM ratings 
            WHERE oauth_ID = %s;
        """, (user_id,))
    res = cursor.fetchall()

    cursor.close()

    return jsonify(res), 200


if __name__ == "__main__":
    config = ConfigParser()
    config.read("init_scripts/constants.ini")

    while True:
        try:
            conn = psycopg2.connect(
                host=config["postgres"]["host"],
                database=config["postgres"]["database"],
                user=config["postgres"]["user"],
                password=config["postgres"]["password"],
                port=int(config["postgres"]["port"])
            )

        except Exception:
            print("Trying to connect with database")
            continue
        else:
            break

    cache.init_app(app)
    app.run(host="localhost", port=8082, debug=True)

    conn.close()
