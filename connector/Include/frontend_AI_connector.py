from flask import Flask, request, jsonify
import psycopg2
import pandas
import json
from configparser import ConfigParser


app = Flask(__name__)
db_connector = None
conn = None
movie_list = None

def error_decorator(fun):
    def inner1(*args, **kwargs):
        try:
            fun(*args, **kwargs)
        except psycopg2.DatabaseError:
            return jsonify({"status": "Something... unexpected has occured :sweat_smile:"}), 500
         
    return inner1

@app.route("/", methods=["GET"])
def hello():
    return jsonify({"response": "Hello there"}), 200

#endpoint do wyciągania danych o userze
@app.route("/api/v3/get/<string:username>", methods=["GET"])
def access_user(username):
    return jsonify({"us": "er"}), 200

#endpoint służący do zapisu danych nowostworzonego użytkownika, podajemy mu
#id z oautha oraz login
@app.route("/api/v3/add/<string:oauth_ID>/<string:username>", methods=["POST"])
def add_user(oauth_ID, username):
    cursor = conn.cursor()
    cursor.execute("select * from users where username='{}';".format(username))
    res = cursor.fetchall()

    if len(res):
        cursor.close()
        return jsonify({"status": "User already exists"}), 500

    cursor.execute("INSERT INTO users (username, oauth_ID) VALUES ('{}','{}');".format(
        username, oauth_ID
    ))

    conn.commit()
    cursor.close()
    
    return jsonify({"status": "success"}), 200


#roboczy endpoint służący do wyciąganiu rekomendacji
@app.route("/api/v3/ai/<string:oauth_ID>", methods=["GET"])
def get_recommendations(oauth_ID):
    #request od frontu na rekomendacje
    #wysyłanie requestu do AI API o rekomendacje dla usera
    #przesłanie danych do  
    return jsonify({"movies": ["3", "Wiedźmin 3", "Najlepszy."]}), 200

@app.route("/api/v3/get_movie/<int:movie_ID>", methods=["GET"])
# @error_decorator
def get_movie(movie_ID):
    movie_info = movie_list.loc[movie_list['movie_id'] == movie_ID]
    if movie_info.empty:
        return jsonify({"status": "Movie with ID {} doesn't exist".format(movie_ID)}
                       ), 500

    cast = json.loads(movie_info["cast"][0].replace('\\"','"'))
    crew = json.loads(movie_info["crew"][0].replace('\\"','"'))

    output_json = {"movie_id": movie_ID,
                   "title": movie_info["title"][0],
                   "cast": cast,
                   "crew": crew}

    return jsonify(output_json), 200

@app.route("/api/v3/rate_movie/<string:uID>/<string:movie_ID>/<int:rating>", methods=["POST"])
def rate_movie(uID, movie_ID, rating):
    movie_info = movie_list.loc[movie_list['movie_id'] == int(movie_ID)]
    if movie_info.empty:
        return jsonify({"status": "Movie with ID {} doesn't exist".format(movie_ID)}
                       ), 500

    if rating < 1 or rating > 5:
        return jsonify({"status": "Incorrect rating"}), 500

    cursor = conn.cursor()
    cursor.execute("select * from users where oauth_ID='{}';".format(uID))
    res = cursor.fetchall()

    if not len(res):
        cursor.close()
        return jsonify({"status": "User doesn't exists"}), 500

    cursor.execute("select * from ratings where oauth_ID='{}' AND movie_ID='{}';".format(uID, movie_ID))
    res = cursor.fetchall()

    if len(res):
        sql = """ UPDATE ratings
                SET rating = {},
                rdate = CURRENT_TIMESTAMP
                WHERE oauth_ID = '{}' AND
                movie_ID = '{}'
                """
        cursor.execute(sql.format(rating, uID, movie_ID))
    else:
        cursor.execute("INSERT INTO ratings (movie_ID, oauth_ID, rating) VALUES ('{}','{}',{});".format(
            movie_ID, uID, rating
        ))

    conn.commit()
    cursor.close()
    
    return jsonify({"status": "success"}), 200


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
    
    movie_list = pandas.read_csv(config["movie"]["csv_path"])

    app.run(host="0.0.0.0",port=8090, debug=True)
    conn.close()

