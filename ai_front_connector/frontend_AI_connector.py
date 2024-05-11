from flask import Flask, request, jsonify
import tinydb

files = []

DB_PATH = "ai_front_connector/mock_db/db.json"

app = Flask(__name__)
db_connector = None

@app.route("/", methods=["GET"])
def hello():
    return jsonify({"response": "Hello there"}), 200

@app.route("/api/v3/get/<string:oauth_ID>/<string:username>", methods=["POST"])
def access_user(oauth_ID, username):
    print(oauth_ID, username)
    return jsonify({"status": "success"}), 200

@app.route("/api/v3/add/<string:oauth_ID>/<string:username>", methods=["POST"])
def add_user(oauth_ID, username):
    res = db_connector.search(tinydb.where('username') == username)

    if len(res):
        return jsonify({"status": "User already exists"}), 500

    db_connector.insert({"ID": oauth_ID, "username": username})
    return jsonify({"status": "success"}), 200


#idk, czy zrobimy to w ten sposób, ale na wszelki w, route może pozostać, IG
@app.route("/api/v3/ai/<string:oauth_ID>", methods=["GET"])
def get_recommendations(oauth_ID):
    #request od frontu na rekomendacje
    #wysyłanie requestu do AI API o rekomendacje dla usera
    #przesłanie danych do  
    return jsonify({"movies": ["3", "Wiedźmin 3", "Najlepszy."]}), 200

if __name__ == "__main__":
    db_connector = tinydb.TinyDB(DB_PATH)

    app.run(port=8080, debug=True)


