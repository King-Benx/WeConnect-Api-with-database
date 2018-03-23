from flask import request, url_for, session
from . import api
from ..models import User
from .. import known_usernames, known_business_ids, businesses, users, reviews, known_review_ids, known_user_ids, users
from .authentication import token_required
from ..functions import make_json_reply


@api.route('/api/v1/auth/register', methods=['POST'])
def register_new_user():
    # register new user into the system
    data = request.get_json(force=True)
    if len(data.keys()) == 3:
        username = data['username']
        email = data['email']
        password = data['password']
        if (username is not None and email is not None and password is not None
            ) and (username != '' and email != ''
                   and password != '') and (email is not set
                                            and password is not set
                                            and username is not set):
            user = User(username, email, password)
            if user:
                return make_json_reply(
                    'message', 'Successfully created user ' + str(username) +
                    ' you can login using ' + str(
                        url_for('api.login', _external=True))), 201
            else:
                make_json_reply('message', 'Failure creating user'), 400
        else:
            return make_json_reply('message',
                                   'Values cannot be empty or not set'), 400
    else:
        return make_json_reply(
            'message', 'Couldn\'t create user, some fields missing'), 400


# More work to be done on signing out
@api.route('/api/v1/auth/logout', methods=['POST'])
@token_required
def logout_user(current_user):
    # This logs out user from the application
    request.authorization = None
    current_user = None
    global users
    global known_user_ids
    global reviews
    global known_review_ids
    global businesses
    global known_business_ids
    global known_usernames
    del users[:]
    del known_business_ids[:]
    del reviews[:]
    del known_review_ids[:]
    del businesses[:]
    del known_usernames[:]
    del known_user_ids[:]
    if not request.authorization:
        return make_json_reply('message',
                               'You have been successfully logout'), 200
    else:
        return make_json_reply(
            'message', 'Something went wrong, please try again ' +
            str(url_for('api.logout_user', _external=True))), 400


@api.route('/api/v1/auth/reset-password', methods=['POST'])
@token_required
def reset_password(current_user):
    # This resets the password of a user back to password if an email has been given
    data = request.get_json()
    if (len(data.keys()) == 2):
        username = data['username']
        password = data['new_password']
        status = User.reset_password(username, password)
        if status:
            return make_json_reply(
                'message', 'password has been reset to ' + str(password)), 200
        else:
            return make_json_reply(
                'message', 'failure resetting password, username invalid'), 400
    else:
        return make_json_reply('message',
                               'couldn\'t reset password missing fields'), 400
