from user import User
from hmac import compare_digest

users = [User(1, 'bob', 'bob123')]
username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    print("authenticate")
    user = User.find_by_username(username)
    if user and compare_digest(user.password, password):
        return user


def identity(payload):
    print("identity")
    user_id = payload['identity']
    print(user_id)
    return User.find_by_id(100)