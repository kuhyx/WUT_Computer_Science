import pandas as pd
import numpy as np
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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

    def get_recommendations(self, title):
        indices = pd.Series(self.df.index, index=self.df['title']).drop_duplicates()
        idx = indices[title]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        movie_indices = [i[0] for i in sim_scores]
        return self.df['title'].iloc[movie_indices]

    def fit(self, credits_file, movies_file):
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


# Example usage:
if __name__ == "__main__":
    recommender = MovieRecommender()
    recommender.fit('datasets/tmdb_5000_credits.csv', 'datasets/tmdb_5000_movies.csv')
    recommendations = recommender.get_recommendations('The Dark Knight Rises')
    print(recommendations)
