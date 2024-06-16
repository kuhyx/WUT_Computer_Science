import pandas as pd
import numpy as np
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from flask import Flask, request, jsonify
from flask_caching import Cache
import hashlib
import json


config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)

app.config.from_mapping(config)
cache = Cache(app)


def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan


def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        if len(names) > 3:
            names = names[:3]
        return names
    return []


def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''


def create_soup(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])


class MovieRecommender:
    def __init__(self):
        self.df = None
        self.cosine_sim = None

    def fit(self, credits_file, movies_file):
        """
        Fittuje AI do przekazanych danych
        :param credits_file: csv z creditsami
        :param movies_file: csv z filmami
        :return: Nic
        """
        df1 = pd.read_csv(credits_file)
        df2 = pd.read_csv(movies_file)
        df1.columns = ['id', 'tittle', 'cast', 'crew']
        df2 = df2.merge(df1, on='id')
        df2['overview'] = df2['overview'].fillna('')
        self.df = df2

        features = ['cast', 'crew', 'keywords', 'genres']
        for feature in features:
            df2[feature] = df2[feature].apply(literal_eval)

        df2['director'] = df2['crew'].apply(get_director)

        features = ['cast', 'keywords', 'genres']
        for feature in features:
            df2[feature] = df2[feature].apply(get_list)

        features = ['cast', 'keywords', 'director', 'genres']
        for feature in features:
            df2[feature] = df2[feature].apply(clean_data)

        df2['soup'] = df2.apply(create_soup, axis=1)

        count = CountVectorizer(stop_words='english')
        count_matrix = count.fit_transform(df2['soup'])
        self.cosine_sim = cosine_similarity(count_matrix, count_matrix)

        self.df = df2.reset_index()

    def _get_recommendations_one_input(self, movie_id):
        """
        Tworzy rekomendacje, bazując na jednym filmie
        :param movie_id: id filmu, dla którego ma zrobić rekomendację
        :return: Zwraca listę [movie_ids, similarity_scores] gdzie oba argumenty są np.array
        """
        indices = pd.Series(self.df.index, index=self.df['id']).drop_duplicates()
        idx = indices[movie_id]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:101]
        movie_indices = [i[0] for i in sim_scores]
        sim_scores = np.array([t[1] for t in sim_scores])
        return [self.df['id'].iloc[movie_indices].values, sim_scores]

    def get_recommendations(self, movie_ids: list) -> {}:
        """
        Tworzy listę rekomendacji bazującą na id podanych filmów
        :param movie_ids: id filmów, na podstawie których ma wybrać rekomendowane filmy
        :return: Zwraca dicta {movie_id: similarity_scores}
        """
        recommended_movies = {}
        for movie_id in movie_ids:
            recommended_ids, sim_scores = self._get_recommendations_one_input(movie_id)
            for recommended_id, sim_score in zip(recommended_ids, sim_scores):
                if recommended_id in movie_ids:
                    continue

                if recommended_movies.get(int(recommended_id)) is None:
                    recommended_movies[int(recommended_id)] = float(round((sim_score / len(movie_ids)), 4))
                else:
                    recommended_movies[int(recommended_id)] += float(round((sim_score / len(movie_ids)), 4))
        return recommended_movies


recommender = MovieRecommender()
recommender.fit('movie_recommendations/datasets/tmdb_5000_credits.csv',
                'movie_recommendations/datasets/tmdb_5000_movies.csv')


def make_cache_key():
    data = request.get_json()
    if isinstance(data, list):
        data = sorted(data)
    key = hashlib.md5(json.dumps(data).encode('utf-8')).hexdigest()
    return key


@app.route("/api/v3/AI_recommendations", methods=["POST"])
@cache.cached(timeout=300, key_prefix=make_cache_key)
def AI_recommendations():
    ids = request.get_json()
    recommendations = recommender.get_recommendations(ids)
    return jsonify(recommendations)


# Przykładowe użycie:
# if __name__ == "__main__":
#     recommender = MovieRecommender()
#     recommender.fit('datasets/tmdb_5000_credits.csv', 'datasets/tmdb_5000_movies.csv')
#     recommendations = recommender.get_recommendations([49026, 155, 312113])
#     print(recommendations)
