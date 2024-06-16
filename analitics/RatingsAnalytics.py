from User import User
from Rating import Rating
from MockUps import users, ratings


def get_ratings():
    return ratings


def get_number_of_ratings():
    return len(get_ratings())


def get_ratings_in_time(begin_time, end_time):
    pass


def get_ratings_of_movie(movie_id):
    results = []
    for ranting in ratings:
        if ranting.movie_id == movie_id:
            results.append(ranting)
    return results


def get_ratings_of_movie_numbers(movie_id):
    return len(get_ratings_of_movie(movie_id))


def get_ratings_of_movie_in_time(movie_id, begin_time, end_time):
    pass


