#!/usr/bin/env python3
"""Code for preprocessing data and creating model that predicts and.

recomends anime based on another anime entered by user.
"""

import argparse
import datetime
import logging
import math
import shutil
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

logger = logging.getLogger(__name__)


def get_data_cpu(
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
    return rating_data, anime_data


def get_data(
    limit_data: int = -1, data_folder_path: str = "database"
) -> tuple[pd.DataFrame, pd.DataFrame, int]:
    """Load the ratings and anime tables.

    The `gpu` switch this used to take was never read -- the body always went
    through get_data_cpu -- so it is gone rather than kept as a lie.
    """
    rating_data, anime_data = get_data_cpu(limit_data, data_folder_path)

    # used to fetch anime_id(MAL_ID)
    anime_data = anime_data.rename(columns={"MAL_ID": "anime_id"})
    anime_contact_data = anime_data[["anime_id", "Name"]]
    rows_number = rating_data.shape[0]
    return rating_data, anime_contact_data, rows_number


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


@dataclass(frozen=True)
class Thresholds:
    """Minimum vote counts a user and an anime need to stay in the data."""

    user: int = 500
    anime: int = 200


def preprocessing(
    rating_data: pd.DataFrame,
    anime_contact_data: pd.DataFrame,
    thresholds: Thresholds | None = None,
    *,
    debug: bool = False,
    auto: bool = False,
) -> pd.DataFrame:
    """Preprocess the data so the model is faster and more accurate."""
    if thresholds is None:
        thresholds = Thresholds()
    user_threshold, anime_threshold = thresholds.user, thresholds.anime
    rating_data = merge_rating_anime_data(rating_data, anime_contact_data)
    rating_data = split_data_below_thresholds(rating_data, "user_id", user_threshold)
    rating_data = split_data_below_thresholds(rating_data, "anime_id", anime_threshold)
    rating_data = combine_name_and_ratings(rating_data)

    rating_data = rating_data.drop(columns="rating_y")
    rating_data = rating_data.rename(columns={"rating_x": "rating"})
    if debug and not auto:
        logger.info("%s", rating_data)
        get_data_info(rating_data, debug=True)

    pivot_table = rating_data.pivot_table(
        index="Name", columns="user_id", values="rating"
    ).fillna(0)
    if debug and not auto:
        logger.info("%s", pivot_table)
    return pivot_table


def predict(
    prediction_model: object,
    pivot_table: pd.DataFrame,
    request: tuple[int, str, int] = (42, "RANDOM", 6),
    *,
    debug: bool = False,
) -> tuple[str, object]:
    """Pick a random anime and recommend the ones most like it.

    ``request`` is (seed, anime, recommendation_number); the three always
    travel together, and bundling them keeps this under the argument limit.
    """
    seed, anime, recommendation_number = request
    # default_rng(seed) replaces np.random.seed: the legacy global state is
    # what NPY002 flags, and a local generator is reproducible per call.
    rng = np.random.default_rng(seed)
    if anime == "RANDOM":
        chosen_anime = rng.choice(pivot_table.shape[0])
        query = pivot_table.iloc[chosen_anime, :].to_numpy().reshape(1, -1)
        chosen_anime_name = pivot_table.index[chosen_anime]
    else:
        query = pivot_table.loc[anime].to_numpy().reshape(1, -1)
        chosen_anime_name = anime
    distance, suggestions = prediction_model.kneighbors(query)
    if debug:
        logger.info("prediction model, distance:  %s", distance)
    for i in range(2):
        if i == 0:
            logger.info("Recommendations for %s:\n", chosen_anime_name)
        else:
            logger.info(
                "%s: %s,\n                with distance of %s:",
                i,
                pivot_table.index[suggestions.flatten()[i]],
                distance.flatten()[i],
            )
    average_distance = np.mean(distance.flatten())
    _closest_anime_name = pivot_table.index[suggestions.flatten()[1]]
    closest_anime_distance = distance.flatten()[1]
    average_minus_closest_distance = average_distance - closest_anime_distance
    logger.info(
        "Average distance: %s, average_minus_closest_distance: %s",
        average_distance,
        average_minus_closest_distance,
    )

    return (
        chosen_anime,
        suggestions.flatten()[1 : recommendation_number + 1],
        distance.flatten()[1 : recommendation_number + 1],
        f"{closest_anime_distance}_{average_distance}_{average_minus_closest_distance}",
    )


def calculate_neighbors(rows_number: int, neighbors: int = 5) -> int:
    """Resolve the k of k-NN from the named strategies, or pass it through."""
    neighbor_value = {
        "default": 5,
        "sqrt": math.floor(math.sqrt(rows_number)),
        "half": math.floor(rows_number / 2),
        "log": math.floor(math.log(rows_number)),
        "n-1": rows_number - 1,
    }
    if isinstance(neighbors, str):
        return neighbor_value[neighbors]
    return neighbors


def create_model(
    pivot_table: pd.DataFrame,
    metric: str = "cosine",
    algorithm: str = "brute",
    neighbors: int = 5,
) -> object:
    """Create model based on neaarest neighbor for anime prediction."""
    neighbors_number = calculate_neighbors(pivot_table.shape[0], neighbors)
    pivot_table_matrix = csr_matrix(pivot_table.to_numpy())
    if algorithm == "brute":
        model = NearestNeighbors(
            n_neighbors=neighbors_number, metric=metric, algorithm=algorithm
        )
    else:
        model = NearestNeighbors(n_neighbors=neighbors_number, algorithm=algorithm)
    try:
        model.fit(pivot_table_matrix)
    except ValueError:
        # sklearn raises ValueError when a metric does not accept this data.
        logger.info(
            "Error in create_model, probably wrong metric for data\n        "
            "Metric: %s, algorithm: %s",
            metric,
            algorithm,
        )
        return "Error!"
    return model


def handle_arguments() -> tuple[object, ...]:
    """Handle every argument that changes the algorithm's behaviour or display."""
    parser = argparse.ArgumentParser(description="Example script with pyargs")
    parser.add_argument(
        "--data_limit",
        "-dl",
        help="""Specify data limit,
                        Recommended at least 500k, set to -1 for no limit""",
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
    allowed_algorithms = ["auto", "brute"]
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
        help="""Specify minimal number of votes required for user to be
                        included in the data, set to -1 for no threshold""",
        required=False,
        type=int,
        default=500,
    )
    parser.add_argument(
        "--anime_threshold",
        "-at",
        help="""Specify minimal number of votes required for anime
                        to be included in the data, set to -1 for no threshold""",
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
    parser.add_argument(
        "--auto",
        "-au",
        help="""Enable auto mode, no debug, no user parameters,
                        automatic testing and saving results""",
        type=bool,
        required=False,
        default=False,
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
        args.auto,
    )


def auto_mode(data_limit: int = -1, seed: int = 42, anime: str = "RANDOM") -> None:
    """Run one unattended recommendation with fixed settings."""
    logger.info("Started auto mode")
    algorithm_spread = ["auto", "brute"]
    metric_spread = ["manhattan", "euclidean", "cosine"]
    neighbor_spread = [5, "sqrt", "half", "log", "n-1"]
    # No reason to access and waste computational power every time we run the simulation
    starting_rating_data, starting_anime_contact_data, starting_rows_number = get_data(
        limit_data=data_limit
    )
    original_pivot_table = preprocessing(
        starting_rating_data, starting_anime_contact_data
    )
    if Path("test_results").exists():
        shutil.rmtree("test_results")
    for algorithm in algorithm_spread:
        possible_metrics = []
        if algorithm != "auto":
            possible_metrics = metric_spread
        logger.info("testing for algorithm:  %s %s", algorithm, possible_metrics)
        if possible_metrics == []:
            possible_metrics = [""]
        for metric in possible_metrics:
            if metric != "precomputed":
                logger.info("testing for algorithm, metric:  %s %s", algorithm, metric)
                for neighbor_amount in neighbor_spread:
                    logger.info(
                        "testing for algorithm, metric, neighbor_amount:  %s %s %s",
                        algorithm,
                        metric,
                        neighbor_amount,
                    )
                    preprocess_model_predict(
                        starting_rows_number,
                        original_pivot_table,
                        ModelSettings(
                            metric=metric,
                            algorithm=algorithm,
                            neighbors=neighbor_amount,
                            seed=seed,
                            anime=anime,
                        ),
                    )


def write_test_results(title: str, result: object = "") -> None:
    """Append one measured result to the results file."""
    if not Path("test_results").exists():
        Path("test_results").mkdir(parents=True)

    # Generate timestamped filename
    timestamp = datetime.datetime.now(tz=datetime.timezone.utc).strftime(
        "%Y%m%d%H%M%S"
    )  # e.g., 20230611235959
    filename = f"{title}_{timestamp}.txt"

    # Create and write to the file
    with (Path("test_results") / filename).open("a") as file:
        file.write(result)


def calculate_precision(predictions: object, threshold: float = 8) -> float:
    """Precision at the given rating threshold."""
    ratings = [anime[anime > 0].mean() for anime in predictions]
    precision = [1 if r >= threshold else 0 for r in ratings]
    return np.mean(precision)


@dataclass(frozen=True)
class ModelSettings:
    """One point in the k-NN parameter sweep the report tabulates."""

    metric: str = "cosine"
    algorithm: str = "brute"
    neighbors: int = 5
    seed: int = 42
    anime: str = "RANDOM"
    recommendation_amount: int = 5
    user_threshold: int = 500
    anime_threshold: int = 200


def preprocess_model_predict(
    rows_number: int,
    pivot_table: pd.DataFrame,
    settings: ModelSettings | None = None,
) -> None:
    """Build the model for one setting and record what it recommends.

    Five of its fifteen parameters -- rating_data, anime_contact_data,
    data_limit, db and debug -- were never read: the preprocessing they
    belonged to happens in the caller, which passes the finished pivot_table.
    They are gone rather than annotated as unused. The rest travel together as
    one ModelSettings, which is also what keeps this under the argument limit.
    """
    if settings is None:
        settings = ModelSettings()
    metric = settings.metric
    algorithm = settings.algorithm
    neighbors = settings.neighbors
    seed = settings.seed
    anime = settings.anime
    recommendation_amount = settings.recommendation_amount
    user_threshold = settings.user_threshold
    anime_threshold = settings.anime_threshold
    model = create_model(pivot_table, metric, algorithm, neighbors)
    result = ""
    if model != "Error!":
        chosen_anime, suggestions, distance, distance_data = predict(
            model, pivot_table, (seed, anime, recommendation_amount)
        )

        chosen_anime_name = pivot_table.index[chosen_anime]
        precision = calculate_precision([pivot_table.iloc[s] for s in suggestions])

        result = f"{chosen_anime_name}:\n"
        for i in range(len(suggestions)):
            result += f"{pivot_table.index[suggestions[i]]}; Distance: {distance[i]}\n"
        result += f"Precision: {precision * 100}%\n"
        result += (
            "Smallest distance, average distance, Average - Smallest distance: "
            + distance_data
        )
    write_test_results(
        f"dl={rows_number}&s={seed}&m={metric}&a={algorithm}"
        f"&ut={user_threshold}&at={anime_threshold}&n={neighbors}",
        result,
    )


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    (
        SEED,
        DEBUG,
        DATA_LIMIT,
        DB,
        METRIC,
        ALGORITHM,
        ANIME,
        NEIGHBORS,
        USER_THRESHOLD,
        ANIME_THRESHOLD,
        RECOMMENDATION_AMOUNT,
        AUTO,
    ) = handle_arguments()
    if not AUTO:
        logger.info("Entered not auto mode")
        starting_rating_data, starting_anime_contact_data, starting_rows_number = (
            get_data(limit_data=DATA_LIMIT, data_folder_path=DB)
        )
        pivot_table = preprocessing(
            starting_rating_data,
            starting_anime_contact_data,
            Thresholds(USER_THRESHOLD, ANIME_THRESHOLD),
        )
        preprocess_model_predict(
            starting_rows_number,
            pivot_table,
            ModelSettings(
                metric=METRIC,
                algorithm=ALGORITHM,
                neighbors=NEIGHBORS,
                seed=SEED,
                anime=ANIME,
                recommendation_amount=RECOMMENDATION_AMOUNT,
                user_threshold=USER_THRESHOLD,
                anime_threshold=ANIME_THRESHOLD,
            ),
        )
    if AUTO:
        auto_mode(DATA_LIMIT, SEED, ANIME)
