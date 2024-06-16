from User import User
from Ranting import Ranting
from MockUps import users,rantings


def get_rantings():
    return rantings


def get_number_of_ratings():
    return get_rantings().__len__()


def get_rantings_in_time(begin_time, end_time):
    pass


def get_rantings_of_movie(movie_id):
    results = []
    for ranting in rantings:
        if ranting.movie_id == movie_id:
            results.append(ranting)
    return results


def get_rantings_of_movie_numbers(movie_id):
    return get_rantings_of_movie(movie_id).__len__()


def get_rantings_of_movie_in_time(movie_id, begin_time, end_time):
    pass


