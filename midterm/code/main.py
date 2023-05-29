"""
Code for preprocessing data and creating model that predicts and
recomends anime based on another anime entered by user
"""
import pandas as pd
import numpy as np
import argparse

import sklearn
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix


def get_data(limit_data=-1, data_folder_path="database"):
    """
    Reads anime from csv database
    """
    if limit_data > -1:
        # User can limit number of data taken into consideration,
        # model seems to work with limit_data value as low as 500,000
        rating_data = pd.read_csv(
            data_folder_path + "/animelist.csv", nrows=limit_data)
    else:
        rating_data = pd.read_csv(data_folder_path + "/animelist.csv")
    anime_data = pd.read_csv(data_folder_path + "/anime.csv")

    # used to fetch anime_id(MAL_ID)
    anime_data = anime_data.rename(columns={"MAL_ID": "anime_id"})
    anime_contact_data = anime_data[["anime_id", "Name"]]
    return rating_data, anime_contact_data


def merge_rating_anime_data(rating_data, anime_contact_data, debug=False):
    """
    Preprocesses the data used for rating
    """
    rating_data = rating_data.merge(
        anime_contact_data, left_on="anime_id", right_on="anime_id", how="left"
    )
    rating_data = rating_data[
        ["user_id", "Name", "anime_id", "rating",
            "watching_status", "watched_episodes"]
    ]
    rating_head = rating_data.head()
    if debug:
        print(rating_head)
    rating_shape_complete = rating_data.shape
    if debug:
        print(rating_shape_complete)
    return rating_data


def split_data_below_thresholds(rating_data, data_name, threshold, debug=False):
    """
    Removes data with data_name which is below given threshold
    """
    count = rating_data[data_name].value_counts()
    rating_data = rating_data[
        rating_data[data_name].isin(count[count >= threshold].index)
    ].copy()
    rating_shape_cut = rating_data.shape
    if debug:
        print(rating_shape_cut)
    return rating_data


def combine_name_and_ratings(rating_data, debug=False):
    """
    Create table which holds name of the anime and number of its reviews
    then we merge this with rating_data
    """
    combine_movie_rating = rating_data.dropna(axis=0, subset=["Name"])
    movie_rating_count = (
        combine_movie_rating.groupby(by=["Name"])["rating"]
        .count()
        .reset_index()[["Name", "rating"]]
    )
    rating_head = movie_rating_count.head()
    if debug:
        print(rating_head)
    rating_data = combine_movie_rating.merge(
        movie_rating_count, left_on="Name", right_on="Name", how="left"
    )
    return rating_data


def get_length_of_data(rating_data, data_name):
    """
    We get amount of data in the database with a given column data_name
    """
    # Encoding categorical data
    column_ids = rating_data[data_name + "_id"].unique().tolist()
    column_to_column = {x: i for i, x in enumerate(column_ids)}
    rating_data[data_name] = rating_data[data_name +
                                         "_id"].map(column_to_column)
    users_number = len(column_to_column)
    return users_number


def get_top_ranked(rating_data, data_name, join_table=None, top_data_taken=20):
    """
    Get anime with highest ranking
    """
    if join_table is None:
        join_table = rating_data
    group_data_by_rating = rating_data.groupby(
        data_name + "_id")["rating"].count()
    top_users = group_data_by_rating.dropna().sort_values(ascending=False)[
        :top_data_taken]
    top_rated = join_table.join(top_users, rsuffix="_r",
                                how="inner", on=data_name + "_id")
    return top_rated


def get_data_info(rating_data, debug=False):
    """
    Get some informations about data
    """
    users_number = get_length_of_data(rating_data, "user")
    animes_number = get_length_of_data(rating_data, "anime")

    top_rated = get_top_ranked(rating_data, "user")
    top_rated = get_top_ranked(rating_data, "anime", top_rated)

    pivot = pd.crosstab(top_rated.user_id, top_rated.anime_id,
                        top_rated.rating, aggfunc=np.sum)

    pivot.fillna(0, inplace=True)
    smallest_rating = min(rating_data["rating"])
    highest_rating = max(rating_data["rating"])
    if debug:
        print(pivot)
    if debug:
        print(f"Num of users: {users_number}, Num of animes: {animes_number}")
        print(
            f"Min total rating: {smallest_rating}, Max total rating: {highest_rating}")


def preprocessing(rating_data, anime_contact_data, debug=False):
    """
    Preprocesses data for making model more accurate and/or faster
    """
    rating_data = merge_rating_anime_data(rating_data, anime_contact_data)
    rating_data = split_data_below_thresholds(rating_data, "user_id", 500)
    rating_data = split_data_below_thresholds(rating_data, "anime_id", 200)
    rating_data = combine_name_and_ratings(rating_data)

    rating_data = rating_data.drop(columns="rating_x")
    rating_data = rating_data.rename(columns={"rating_y": "rating"})
    if debug:
        print(rating_data)
        get_data_info(rating_data)

    pivot_table = rating_data.pivot_table(
        index="Name", columns="user_id", values="rating"
    ).fillna(0)
    if debug:
        print(pivot_table)
    return pivot_table


def predict(prediction_model, pivot_table, seed=42, anime="RANDOM"):
    """
    This will choose a random anime name and our prediction_model will predict similar anime.
    """
    np.random.seed(seed)
    print(pivot_table)
    if anime == "RANDOM":
        chosen_anime = np.random.choice(pivot_table.shape[0])
        query = pivot_table.iloc[chosen_anime, :].values.reshape(1, -1)
        chosen_anime_name = pivot_table.index[chosen_anime]
    else:
        query = pivot_table.loc[anime].values.reshape(1, -1)
        chosen_anime_name = anime

    distance, suggestions = prediction_model.kneighbors(
        query, n_neighbors=6)
    for i in range(0, len(distance.flatten())):
        if i == 0:
            print(f"Recommendations for {chosen_anime_name}:\n")
        else:
            print(
                f"{i}: {pivot_table.index[suggestions.flatten()[i]]}, with distance of {distance.flatten()[i]}:"
            )


def create_model(pivot_table, metric="cosine", algorithm="brute"):
    """
    Creates model based on neaarest neighbor for anime prediction
    """
    pivot_table_matrix = csr_matrix(pivot_table.values)
    model = NearestNeighbors(metric=metric, algorithm=algorithm)
    model.fit(pivot_table_matrix)
    return model


def handle_arguments():
    parser = argparse.ArgumentParser(description='Example script with pyargs')
    parser.add_argument('--data_limit', '-dl',
                        help='Specify data limit, Recommended at least 50k', required=False, type=int, default=-1)
    parser.add_argument('--seed', '-s', help='Specify seed',
                        type=int, required=False, default=42)
    parser.add_argument('--debug', '-d', help='Use debug (more information) prints',
                        type=bool, required=False, default=False)
    parser.add_argument('--database', '-db', help='Specify database path',
                        required=False, default="database")

    allowed_metric = ["cosine", "mahalanobis", "euclidean"]
    parser.add_argument('--metric', '-m', help='Specify metric for NearestNeighbor learner',
                        required=False, default="cosine", choices=allowed_metric)
    allowed_algorithms = ['auto', 'ball_tree', 'kd_tree', 'brute']
    parser.add_argument('--algorithm', '-a', help='Specify algorithm for Nearest Neighbor learner',
                        required=False, default="brute", choices=allowed_algorithms)
    parser.add_argument('--anime', '-an', help='Specify anime to choose',
                        required=False, default="RANDOM")
    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the values of the arguments
    return args.seed, args.debug, args.data_limit, args.database, args.metric, args.algorithm, args.anime


if __name__ == "__main__":
    seed, debug, data_limit, db, metric, algorithm, anime = handle_arguments()

    RATING_DATA, ANIME_CONTACT_DATA = get_data(data_limit, db)
    PIVOT_TABLE = preprocessing(RATING_DATA, ANIME_CONTACT_DATA, debug)
    MODEL = create_model(PIVOT_TABLE, metric, algorithm)
    predict(MODEL, PIVOT_TABLE, seed, anime)
