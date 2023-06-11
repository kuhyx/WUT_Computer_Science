"""
Code for preprocessing data and creating model that predicts and
recomends anime based on another anime entered by user
"""
import math
import argparse
import shutil
import os
import datetime
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import VALID_METRICS_SPARSE
from scipy.sparse import csr_matrix


def get_data_cpu(limit_data=-1, data_folder_path="database"):
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
    return rating_data, anime_data


def get_data(limit_data=-1, data_folder_path="database", gpu=False):
    rating_data, anime_data = get_data_cpu(limit_data, data_folder_path)

    # used to fetch anime_id(MAL_ID)
    anime_data = anime_data.rename(columns={"MAL_ID": "anime_id"})
    anime_contact_data = anime_data[["anime_id", "Name"]]
    rows_number = rating_data.shape[0]
    return rating_data, anime_contact_data, rows_number


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


def split_data_below_thresholds(rating_data, data_name, threshold=-1, debug=False):
    """
    Removes data with data_name which is below given threshold
    """
    if threshold != -1:
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


def get_data_info(rating_data, debug=False, gpu=False):
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


def preprocessing(rating_data, anime_contact_data,
                  debug=False, user_threshold=500, anime_threshold=200, auto=False):
    """
    Preprocesses data for making model more accurate and/or faster
    """
    rating_data = merge_rating_anime_data(rating_data, anime_contact_data)
    rating_data = split_data_below_thresholds(
        rating_data, "user_id", user_threshold)
    rating_data = split_data_below_thresholds(
        rating_data, "anime_id", anime_threshold)
    rating_data = combine_name_and_ratings(rating_data)

    rating_data = rating_data.drop(columns="rating_y")
    rating_data = rating_data.rename(columns={"rating_x": "rating"})
    if debug and not auto:
        print(rating_data)
        get_data_info(rating_data, True)

    pivot_table = rating_data.pivot_table(
        index="Name", columns="user_id", values="rating"
    ).fillna(0)
    if debug and not auto:
        print(pivot_table)
    return pivot_table


def predict(prediction_model, pivot_table, seed=42, anime="RANDOM", recommendation_number=6, auto=False, debug=False):
    """
    This will choose a random anime name and our prediction_model will predict similar anime.
    """
    np.random.seed(seed)
    if anime == "RANDOM":
        chosen_anime = np.random.choice(pivot_table.shape[0])
        query = pivot_table.iloc[chosen_anime, :].values.reshape(1, -1)
        chosen_anime_name = pivot_table.index[chosen_anime]
    else:
        query = pivot_table.loc[anime].values.reshape(1, -1)
        chosen_anime_name = anime
    distance, suggestions = prediction_model.kneighbors(
        query)
    if debug:
        print("prediction model, distance: ", distance)
    for i in range(0, 2):
        if i == 0:
            print(f"Recommendations for {chosen_anime_name}:\n")
        else:
            print(
                f"""{i}: {pivot_table.index[suggestions.flatten()[i]]},
                with distance of {distance.flatten()[i]}:"""
            )
    average_distance = np.mean(distance.flatten())
    closest_anime_name = pivot_table.index[suggestions.flatten()[1]]
    closest_anime_distance = distance.flatten()[1]
    average_minus_closest_distance = average_distance - closest_anime_distance
    print(
        f"Average distance: {average_distance}, average_minus_closest_distance: {average_minus_closest_distance}")

    return chosen_anime, suggestions.flatten()[1:recommendation_number+1], distance.flatten()[1:recommendation_number+1], f"{closest_anime_distance}_{average_distance}_{average_minus_closest_distance}"
    # return f"{chosen_anime_name}_{closest_anime_name}_{closest_anime_distance}_{average_distance}_{average_minus_closest_distance}"


def calculate_neighbors(rows_number, neighbors=5):
    neighbor_value = {
        "default": 5,
        "sqrt": math.floor(math.sqrt(rows_number)),
        "half": math.floor(rows_number / 2),
        "log": math.floor(math.log(rows_number)),
        "n-1": rows_number - 1
    }
    if isinstance(neighbors, str):
        return neighbor_value[neighbors]
    return neighbors


def create_model(pivot_table, rows_number, metric="cosine", algorithm="brute", neighbors=5):
    """
    Creates model based on neaarest neighbor for anime prediction
    """
    neighbors_number = calculate_neighbors(pivot_table.shape[0], neighbors)
    pivot_table_matrix = csr_matrix(pivot_table.values)
    if algorithm == "brute":
        model = NearestNeighbors(n_neighbors=neighbors_number,
                                 metric=metric, algorithm=algorithm)
    else:
        model = NearestNeighbors(
            n_neighbors=neighbors_number, algorithm=algorithm)
    try:
        model.fit(pivot_table_matrix)
    except:
        print(f"""Error in create_model, probably wrong metric for data
        Metric: {metric}, algorithm: {algorithm}""")
        return "Error!"
    return model


def handle_arguments():
    """
    Handles all arguments that can be used to change algorithm behaviour or program display
    """
    parser = argparse.ArgumentParser(description='Example script with pyargs')
    parser.add_argument('--data_limit', '-dl',
                        help="""Specify data limit,
                        Recommended at least 500k, set to -1 for no limit""",
                        required=False, type=int, default=-1)
    parser.add_argument('--seed', '-s',
                        help='Specify seed',
                        type=int, required=False, default=42)
    parser.add_argument('--debug', '-d',
                        help='Use debug (more information) prints',
                        type=bool, required=False, default=False)
    parser.add_argument('--database', '-db',
                        help='Specify database path',
                        required=False, default="database")

    allowed_metric = ["cosine", "mahalanobis", "euclidean"]
    parser.add_argument('--metric', '-m',
                        help='Specify metric for NearestNeighbor learner',
                        required=False, default="cosine", choices=allowed_metric)
    allowed_algorithms = ['auto', 'brute']
    parser.add_argument('--algorithm', '-a',
                        help='Specify algorithm for Nearest Neighbor learner',
                        required=False, default="brute", choices=allowed_algorithms)
    parser.add_argument('--anime', '-an',
                        help='Specify anime to choose',
                        required=False, default="RANDOM")
    parser.add_argument('--neighbors', '-n',
                        help='Specify number of nearest neighbors',
                        required=False, default=5)
    parser.add_argument('--user_threshold', '-ut',
                        help="""Specify minimal number of votes required for user to be
                        included in the data, set to -1 for no threshold""",
                        required=False, type=int,  default=500)
    parser.add_argument('--anime_threshold', '-at',
                        help="""Specify minimal number of votes required for anime
                        to be included in the data, set to -1 for no threshold""",
                        required=False, type=int, default=200)
    parser.add_argument('--recommendation_amount', '-ra',
                        help='Specify how much anime should be recommended',
                        required=False, type=int, default=5)
    parser.add_argument('--auto', '-au',
                        help="""Enable auto mode, no debug, no user parameters,
                        automatic testing and saving results""",
                        type=bool, required=False, default=False)

    # Parse the command-line arguments
    args = parser.parse_args()
    args.recommendation_amount = args.recommendation_amount + 1
    # Access the values of the arguments
    return args.seed, args.debug, args.data_limit, args.database, args.metric, args.algorithm, args.anime, args.neighbors, args.user_threshold, args.anime_threshold, args.recommendation_amount, args.auto


def auto_mode(data_limit=-1, seed=42, anime="RANDOM"):
    print("Started auto mode")
    algorithm_spread = ['auto', 'brute']
    metric_spread = ['manhattan', 'euclidean', 'cosine']
    neighbor_spread = [5, "sqrt", "half", "log", "n-1"]
    # No reason to access and waste computational power every time we run the simulation
    starting_rating_data, starting_anime_contact_data, starting_rows_number = get_data(
        limit_data=data_limit)
    original_pivot_table = preprocessing(
        starting_rating_data, starting_anime_contact_data)
    if os.path.exists('test_results'):
        shutil.rmtree('test_results')
    for algorithm in algorithm_spread:
        possibleMetrics = []
        if algorithm != 'auto':
            possibleMetrics = metric_spread
        print("testing for algorithm: ", algorithm, possibleMetrics)
        if possibleMetrics == []:
            possibleMetrics = [""]
        for metric in possibleMetrics:
            if metric != 'precomputed':
                print("testing for algorithm, metric: ", algorithm, metric)
                for neighbor_amount in neighbor_spread:
                    print("testing for algorithm, metric, neighbor_amount: ",
                          algorithm, metric, neighbor_amount)
                    preprocess_model_predict(starting_rating_data, starting_anime_contact_data,
                                             starting_rows_number, original_pivot_table, seed=seed, anime=anime,  neighbors=neighbor_amount, algorithm=algorithm, metric=metric)


def write_test_results(title, result=""):
    # Create directory if it doesn't already exist

    if not os.path.exists('test_results'):
        os.makedirs('test_results')

    # Generate timestamped filename
    timestamp = datetime.datetime.now().strftime(
        '%Y%m%d%H%M%S')  # e.g., 20230611235959
    filename = f"{title}_{timestamp}.txt"

    # Create and write to the file
    with open(os.path.join('test_results', filename), 'a') as file:
        file.write(result)


def calculate_precision(predictions, threshold=8):
    ratings = [anime[anime > 0].mean() for anime in predictions]
    precision = [1 if r >= threshold else 0 for r in ratings]
    return np.mean(precision)


def preprocess_model_predict(rating_data, anime_contact_data, rows_number, pivot_table, data_limit=-1, db="database", debug=False, user_threshold=500, anime_threshold=200, metric="cosine", algorithm="brute", neighbors=5, seed=42, anime="RANDOM", recommendation_amount=5):
    MODEL = create_model(pivot_table, rows_number,
                         metric, algorithm, neighbors)
    result = ""
    if MODEL != "Error!":
        chosen_anime, suggestions, distance, distance_data = predict(MODEL, pivot_table, seed,
                                                                     anime, recommendation_amount)

        chosen_anime_name = pivot_table.index[chosen_anime]
        # average_distance = np.mean(distance)
        # closest_anime_name = pivot_table.index[suggestions[1]]
        # closest_anime_distance = distance[1]
        # average_minus_closest_distance = closest_anime_distance - average_distance
        precision = calculate_precision(
            [pivot_table.iloc[s] for s in suggestions])

        result = f"{chosen_anime_name}:\n"
        for i in range(len(suggestions)):
            result += f"{pivot_table.index[suggestions[i]]}; Distance: {distance[i]}\n"
        result += f"Precision: {precision*100}%\n"
        result += "Smallest distance, average distance, Average - Smallest distance: " + distance_data
        # result = f"{chosen_anime_name}_{closest_anime_name}_{closest_anime_distance}_{average_distance}_{average_minus_closest_distance}"
    write_test_results(
        f"dl={rows_number}&s={seed}&m={metric}&a={algorithm}&ut={user_threshold}&at={anime_threshold}&n={neighbors}", result)


if __name__ == "__main__":
    SEED, DEBUG, DATA_LIMIT, DB, METRIC, ALGORITHM, ANIME, NEIGHBORS, USER_THRESHOLD, ANIME_THRESHOLD, RECOMMENDATION_AMOUNT, AUTO = handle_arguments()
    if not AUTO:
        print("Entered not auto mode")
        starting_rating_data, starting_anime_contact_data, starting_rows_number = get_data(
            limit_data=DATA_LIMIT, data_folder_path=DB)
        pivot_table = preprocessing(
            starting_rating_data, starting_anime_contact_data, USER_THRESHOLD, ANIME_THRESHOLD)
        preprocess_model_predict(starting_rating_data, starting_anime_contact_data, starting_rows_number,
                                 pivot_table, data_limit=DATA_LIMIT, db=DB, debug=DEBUG, user_threshold=USER_THRESHOLD, anime_threshold=ANIME_THRESHOLD,
                                 metric=METRIC, algorithm=ALGORITHM, neighbors=NEIGHBORS, seed=SEED, anime=ANIME, recommendation_amount=RECOMMENDATION_AMOUNT)
    if AUTO:
        auto_mode(DATA_LIMIT, SEED, ANIME)
