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


@app.route("/api/get_number_of_ratings")
@cache.cached(timeout=1000)
def get_number_of_ratings():
    cursor = conn.cursor()
    cursor.execute("select count(*) as num_of_ratings from ratings")
    res = cursor.fetchall()

    return len(res['num_of_ratings'])


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
    app.run(host="0.0.0.0", port=8090, debug=True)

    conn.close()
