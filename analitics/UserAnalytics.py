from User import User
from Rating import Rating
from MockUps import users, ratings


def get_number_of_users():
    return len(users)


def get_user_ratings(user_id):
    results = []
    for rating in ratings:
        if rating.user_id == user_id:
            results.append(rating)
    return results


def get_user_ratings_number(user_id):
    return len(get_user_ratings(user_id))


def get_user_ratings_in_time(user_id, begin, end):
    pass


