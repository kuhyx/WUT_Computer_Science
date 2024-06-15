from User import User
from Ranting import Ranting
from MockUps import users,rantings


def get_number_of_users():
    return users.__len__()


def get_user_rantings(user_id):
    results=[]
    for ranting in rantings:
        if ranting.user_id==user_id:
            results.append(ranting)
    return results


def get_user_rantings_number(user_id):
    return get_user_rantings(user_id).__len__()


def get_user_rantings_in_time(user_id, begin, end):
    pass


