from flask import Flask, request, jsonify
import tinydb
import psycopg2

files = []

DB_PATH = "ai_front_connector/mock_db/db.json"

app = Flask(__name__)
db_connector = None
conn = None

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
    # res = db_connector.search(tinydb.where('username') == username)

    cursor = conn.cursor()
    cursor.execute("select * from users where username='{}';".format(username))
    res = cursor.fetchall()

    if len(res):
        return jsonify({"status": "User already exists"}), 500

    # db_connector.insert({"ID": oauth_ID, "username": username})
    cursor.execute("INSERT INTO users (username, oauth_ID) VALUES ('{}','{}');".format(
        oauth_ID, username
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

if __name__ == "__main__":
    db_connector = tinydb.TinyDB(DB_PATH)
    conn = psycopg2.connect(
        host="localhost",
        database="test_db",
        user="root",
        password="root",
        port=5432
    )

    app.run(port=8080, debug=True)
    conn.close()

