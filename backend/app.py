from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import firebase_admin
from firebase_admin import credentials, auth
from dotenv import load_dotenv
import os
import requests

load_dotenv()
TMDB_BEARER_TOKEN = os.getenv('TMDB_BEARER_TOKEN')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite3'
app.config['SQLALCHEY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

cred = credentials.Certificate('movie-recommendation-firebase-adminsdk.json')
firebase_admin.initialize_app(cred)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Integer, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/login', methods=['POST'])
def login():
    token = request.json.get('token')
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        print(uid)
        email = decoded_token.get('email')

        user = User.query.filter_by(uid=uid).first()
        if user is None:
            user = User(uid=uid, email=email)

            db.session.add(user)
            db.session.commit()

        return jsonify({'message': 'Login successful!', 'email': email, 'is_admin': user.is_admin}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Login failed'}), 401


@app.route('/count_user_ratings', methods=['POST'])
def count_user_ratings():
    token = request.json.get('token')
    try:
        decoded_token = auth.verify_id_token(token)
        user_id = decoded_token['uid']

        user = User.query.filter_by(uid=user_id).first()
        if user is None:
            return jsonify({'message': 'Error'}), 500

        rating_count = Rating.query.filter_by(user_id=user_id).count()
        return jsonify({'message': 'Ratings counted!', 'rating_count': rating_count}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': str(e)}), 500


@app.route('/movie/<int:movie_id>', methods=['GET'])
def get_tmdb_data_movie_id(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}'

    headers = {
        'Authorization': f'Bearer {TMDB_BEARER_TOKEN}'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return jsonify(response.json()), 200
    except Exception as e:
        print(e)
        return jsonify({'message': str(e)}), 500


@app.route('/movie', methods=['GET'])
def get_tmdb_data_query():
    query = request.args.get('query')

    if query:
        url = f'https://api.themoviedb.org/3/search/movie?query={query}'
    else:
        url = 'https://api.themoviedb.org/3/trending/movie/day'

    headers = {
        'Authorization': f'Bearer {TMDB_BEARER_TOKEN}'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return jsonify(response.json()), 200
    except Exception as e:
        print(e)
        return jsonify({'message': str(e)}), 500


@app.route('/rating', methods=['POST'])
def add_rating():
    token = request.json.get('token')
    movie = request.json.get('movie')
    value = request.json.get('value')
    try:
        decoded_token = auth.verify_id_token(token)
        user_id = decoded_token['uid']

        # user = User.query.filter_by(uid=user_id).first()
        # if user is None:
        #     return jsonify({'message': 'Error'}), 500

        rating = Rating.query.filter_by(
            user_id=user_id, movie_id=movie).first()
        if rating is None:
            rating = Rating(user_id=user_id, movie_id=movie, value=value)

            db.session.add(rating)
            db.session.commit()

            return jsonify({'message': 'Rating added successfully!'}), 201
        else:
            rating.value = value

            db.session.commit()

            return jsonify({'message': 'Rating updated successfully!'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': str(e)}), 500


@app.route('/rating', methods=['DELETE'])
def remove_rating():
    token = request.json.get('token')
    movie = request.json.get('movie')
    try:
        decoded_token = auth.verify_id_token(token)
        user_id = decoded_token['uid']

        # user = User.query.filter_by(uid=user_id).first()
        # if user is None:
        #     return jsonify({'message': 'Error'}), 500

        rating = Rating.query.filter_by(
            user_id=user_id, movie_id=movie).first()
        if rating is None:
            return jsonify({'message': 'Error'}), 500

        db.session.delete(rating)
        db.session.commit()

        return jsonify({'message': 'Rating removed successfully!'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': str(e)}), 500


@app.route('/get_rating', methods=['POST'])
def get_rating():
    token = request.json.get('token')
    movie = request.json.get('movie')
    try:
        decoded_token = auth.verify_id_token(token)
        user_id = decoded_token['uid']

        # user = User.query.filter_by(uid=user_id).first()
        # if user is None:
        #     return jsonify({'message': 'Error'}), 500

        rating = Rating.query.filter_by(
            user_id=user_id, movie_id=movie).first()
        if rating is None:
            return jsonify({'message': 'Rating not found!'}), 200
        else:
            return jsonify({'message': 'Rating found!', 'movie': rating.movie_id, 'value': rating.value}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': str(e)}), 500
