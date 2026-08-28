#!/usr/bin/env python3
"""Code for preprocessing data and creating model that predicts and.

recomends anime based on another anime entered by user.
"""

import argparse
import logging

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

logger = logging.getLogger(__name__)


def get_data(
    limit_data: int = -1, data_folder_path: str = "database"
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Read anime from csv database."""
    if limit_data > -1:
        # User can limit number of data taken into consideration,
        # model seems to work with limit_data value as low as 500,000
        rating_data = pd.read_csv(data_folder_path + "/animelist.csv", nrows=limit_data)
    else:
        rating_data = pd.read_csv(data_folder_path + "/animelist.csv")
    anime_data = pd.read_csv(data_folder_path + "/anime.csv")

    # used to fetch anime_id(MAL_ID)
    anime_data = anime_data.rename(columns={"MAL_ID": "anime_id"})
    anime_contact_data = anime_data[["anime_id", "Name"]]
    return rating_data, anime_contact_data


def merge_rating_anime_data(
    rating_data: pd.DataFrame, anime_contact_data: pd.DataFrame, *, debug: bool = False
) -> pd.DataFrame:
    """Preprocesses the data used for rating."""
    rating_data = rating_data.merge(
        anime_contact_data, left_on="anime_id", right_on="anime_id", how="left"
    )
    rating_data = rating_data[
        ["user_id", "Name", "anime_id", "rating", "watching_status", "watched_episodes"]
    ]
    rating_head = rating_data.head()
    if debug:
        logger.info("%s", rating_head)
    rating_shape_complete = rating_data.shape
    if debug:
        logger.info("%s", rating_shape_complete)
    return rating_data


def split_data_below_thresholds(
    rating_data: pd.DataFrame,
    data_name: str,
    threshold: int = -1,
    *,
    debug: bool = False,
) -> pd.DataFrame:
    """Remove data with data_name which is below given threshold."""
    if threshold != -1:
        count = rating_data[data_name].value_counts()
        rating_data = rating_data[
            rating_data[data_name].isin(count[count >= threshold].index)
        ].copy()
        rating_shape_cut = rating_data.shape
        if debug:
            logger.info("%s", rating_shape_cut)
    return rating_data


def combine_name_and_ratings(
    rating_data: pd.DataFrame, *, debug: bool = False
) -> pd.DataFrame:
    """Create table which holds name of the anime and number of its reviews.

    then we merge this with rating_data.
    """
    combine_movie_rating = rating_data.dropna(axis=0, subset=["Name"])
    movie_rating_count = (
        combine_movie_rating.groupby(by=["Name"])["rating"]
        .count()
        .reset_index()[["Name", "rating"]]
    )
    rating_head = movie_rating_count.head()
    if debug:
        logger.info("%s", rating_head)
    return combine_movie_rating.merge(
        movie_rating_count, left_on="Name", right_on="Name", how="left"
    )


def get_length_of_data(rating_data: pd.DataFrame, data_name: str) -> int:
    """We get amount of data in the database with a given column data_name."""
    # Encoding categorical data
    column_ids = rating_data[data_name + "_id"].unique().tolist()
    column_to_column = {x: i for i, x in enumerate(column_ids)}
    rating_data[data_name] = rating_data[data_name + "_id"].map(column_to_column)
    return len(column_to_column)


def get_top_ranked(
    rating_data: pd.DataFrame,
    data_name: str,
    join_table: pd.DataFrame | None = None,
    top_data_taken: float = 20,
) -> pd.DataFrame:
    """Get anime with highest ranking."""
    if join_table is None:
        join_table = rating_data
    group_data_by_rating = rating_data.groupby(data_name + "_id")["rating"].count()
    top_users = group_data_by_rating.dropna().sort_values(ascending=False)[
        :top_data_taken
    ]
    return join_table.join(top_users, rsuffix="_r", how="inner", on=data_name + "_id")


def get_data_info(rating_data: pd.DataFrame, *, debug: bool = False) -> None:
    """Get some informations about data."""
    users_number = get_length_of_data(rating_data, "user")
    animes_number = get_length_of_data(rating_data, "anime")

    top_rated = get_top_ranked(rating_data, "user")
    top_rated = get_top_ranked(rating_data, "anime", top_rated)

    pivot = pd.crosstab(
        top_rated.user_id, top_rated.anime_id, top_rated.rating, aggfunc=np.sum
    )

    pivot = pivot.fillna(0)
    smallest_rating = min(rating_data["rating"])
    highest_rating = max(rating_data["rating"])
    if debug:
        logger.info("%s", pivot)
    if debug:
        logger.info("Num of users: %s, Num of animes: %s", users_number, animes_number)
        logger.info(
            "Min total rating: %s, Max total rating: %s",
            smallest_rating,
            highest_rating,
        )


def preprocessing(
    rating_data: pd.DataFrame,
    anime_contact_data: pd.DataFrame,
    *,
    debug: bool = False,
    user_threshold: int = 500,
    anime_threshold: int = 200,
) -> pd.DataFrame:
    """Preprocesses data for making model more accurate and/or faster."""
    rating_data = merge_rating_anime_data(rating_data, anime_contact_data)
    rating_data = split_data_below_thresholds(rating_data, "user_id", user_threshold)
    rating_data = split_data_below_thresholds(rating_data, "anime_id", anime_threshold)
    rating_data = combine_name_and_ratings(rating_data)

    rating_data = rating_data.drop(columns="rating_x")
    rating_data = rating_data.rename(columns={"rating_y": "rating"})
    if debug:
        logger.info("%s", rating_data)
        get_data_info(rating_data)

    pivot_table = rating_data.pivot_table(
        index="Name", columns="user_id", values="rating"
    ).fillna(0)
    if debug:
        logger.info("%s", pivot_table)
    return pivot_table


def predict(
    prediction_model: object,
    pivot_table: pd.DataFrame,
    seed: int = 42,
    anime: str = "RANDOM",
    recommendation_number: int = 6,
) -> None:
    """Pick a random anime and recommend the ones most like it."""
    # default_rng(seed) replaces np.random.seed: the legacy global state is
    # what NPY002 flags, and a local generator is reproducible per call.
    rng = np.random.default_rng(seed)
    logger.info("%s", pivot_table)
    if anime == "RANDOM":
        chosen_anime = rng.choice(pivot_table.shape[0])
        query = pivot_table.iloc[chosen_anime, :].to_numpy().reshape(1, -1)
        chosen_anime_name = pivot_table.index[chosen_anime]
    else:
        query = pivot_table.loc[anime].to_numpy().reshape(1, -1)
        chosen_anime_name = anime

    distance, suggestions = prediction_model.kneighbors(
        query, n_neighbors=recommendation_number
    )
    for i in range(len(distance.flatten())):
        if i == 0:
            logger.info("Recommendations for %s:\n", chosen_anime_name)
        else:
            logger.info(
                "%s: %s, with distance of %s:",
                i,
                pivot_table.index[suggestions.flatten()[i]],
                distance.flatten()[i],
            )


def create_model(
    pivot_table: pd.DataFrame,
    metric: str = "cosine",
    algorithm: str = "brute",
    neighbors: int = 5,
) -> object:
    """Create model based on neaarest neighbor for anime prediction."""
    pivot_table_matrix = csr_matrix(pivot_table.to_numpy())
    model = NearestNeighbors(n_neighbors=neighbors, metric=metric, algorithm=algorithm)
    model.fit(pivot_table_matrix)
    return model


def handle_arguments() -> tuple[object, ...]:
    """Parse the command line into the recommender's settings."""
    parser = argparse.ArgumentParser(description="Example script with pyargs")
    parser.add_argument(
        "--data_limit",
        "-dl",
        help="Specify data limit, Recommended at least 500k, set to -1 for no limit",
        required=False,
        type=int,
        default=-1,
    )
    parser.add_argument(
        "--seed", "-s", help="Specify seed", type=int, required=False, default=42
    )
    parser.add_argument(
        "--debug",
        "-d",
        help="Use debug (more information) prints",
        type=bool,
        required=False,
        default=False,
    )
    parser.add_argument(
        "--database",
        "-db",
        help="Specify database path",
        required=False,
        default="database",
    )

    allowed_metric = ["cosine", "mahalanobis", "euclidean"]
    parser.add_argument(
        "--metric",
        "-m",
        help="Specify metric for NearestNeighbor learner",
        required=False,
        default="cosine",
        choices=allowed_metric,
    )
    allowed_algorithms = ["auto", "ball_tree", "kd_tree", "brute"]
    parser.add_argument(
        "--algorithm",
        "-a",
        help="Specify algorithm for Nearest Neighbor learner",
        required=False,
        default="brute",
        choices=allowed_algorithms,
    )
    parser.add_argument(
        "--anime",
        "-an",
        help="Specify anime to choose",
        required=False,
        default="RANDOM",
    )
    parser.add_argument(
        "--neighbors",
        "-n",
        help="Specify number of nearest neighbors",
        required=False,
        default=5,
    )
    parser.add_argument(
        "--user_threshold",
        "-ut",
        help=(
            "Specify minimal number of votes required for user to be included "
            "in the data, set to -1 for no threshold"
        ),
        required=False,
        type=int,
        default=500,
    )
    parser.add_argument(
        "--anime_threshold",
        "-at",
        help=(
            "Specify minimal number of votes required for anime to be included "
            "in the data, set to -1 for no threshold"
        ),
        required=False,
        type=int,
        default=200,
    )
    parser.add_argument(
        "--recommendation_amount",
        "-ra",
        help="Specify how much anime should be recommended",
        required=False,
        type=int,
        default=5,
    )

    # Parse the command-line arguments
    args = parser.parse_args()
    args.recommendation_amount = args.recommendation_amount + 1
    # Access the values of the arguments
    return (
        args.seed,
        args.debug,
        args.data_limit,
        args.database,
        args.metric,
        args.algorithm,
        args.anime,
        args.neighbors,
        args.user_threshold,
        args.anime_threshold,
        args.recommendation_amount,
    )


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    (
        seed,
        debug,
        data_limit,
        db,
        metric,
        algorithm,
        anime,
        neighbors,
        user_threshold,
        anime_threshold,
        recommendation_amount,
    ) = handle_arguments()

    RATING_DATA, ANIME_CONTACT_DATA = get_data(data_limit, db)
    PIVOT_TABLE = preprocessing(
        RATING_DATA, ANIME_CONTACT_DATA, debug, user_threshold, anime_threshold
    )
    MODEL = create_model(PIVOT_TABLE, metric, algorithm, neighbors)
    predict(MODEL, PIVOT_TABLE, seed, anime, recommendation_amount)
