from flask import request
from flasgger import swag_from
from . import api
from ..models import User, BlackListedTokens
from .. import db
from .authentication import token_required
from ..functions import make_json_reply, check_validity_of_mail, check_validity_of_username, check_validity_of_input


@api.route('/api/v1/auth/register', methods=['POST'])
@swag_from('swagger/users/create_user.yml')
def register_new_user():
    """
    Register new user into system basing on a username, email and 
    password given in the json
    """
    data = request.get_json(force=True)

    if len(data.keys()) != 3:
        return make_json_reply(
            'message', 'Couldn\'t create user, some fields missing'), 400

    username = data['username']
    email = data['email']
    password = data['password']

    if check_validity_of_input(
            username=username, email=email, password=password) != True:
        return make_json_reply('message',
                               'Values cannot be empty or not set'), 400

    if User.query.filter_by(email=email).count() == 1:
        return make_json_reply('message',
                               'Email already exists, try again'), 400

    if check_validity_of_mail(email) == None:
        return make_json_reply('message', 'Invalid email'), 400

    if len(password) < 3:
        return make_json_reply('message', 'Password too short'), 400

    if len(username) < 3 or check_validity_of_username(username) == None:
        return make_json_reply(
            'message',
            'Username either too short or cannot start with a . '), 400

    user = User(username=username, email=email, password=password)
    db.session.add(user)

    return make_json_reply(
        'message',
        'Successfully created user ' + str(username) + ' you can login'), 201


@api.route('/api/v1/auth/logout', methods=['POST'])
@swag_from('swagger/users/logout_user.yml')
@token_required
def logout_user(current_user):
    """
    Logout current user from the system
    """
    request.authorization = None
    current_user = None
    token = request.headers['x-access-token']
    token_to_blacklist = BlackListedTokens(token=token)

    db.session.add(token_to_blacklist)
    db.session.commit()

    return make_json_reply('message', 'You have been successfully logout'), 200


@api.route('/api/v1/auth/reset-password', methods=['POST'])
@swag_from('swagger/users/reset_password.yml')
@token_required
def reset_password(current_user):
    """
    Changes the password of a user to new_password in json set
    """
    data = request.get_json(force=True)

    if (len(data.keys()) != 1):
        return make_json_reply(
            'message', 'Couldn\'t set password due missing fields'), 400

    if 'new_password' not in data.keys():
        return make_json_reply('message',
                               'Couldn\'t set password due invalid key'), 400

    new_password = data['new_password']
    user = User.query.get(current_user.id)
    user.password = new_password
    db.session.add(user)

    return make_json_reply(
        'message', 'Password has been set to ' + str(new_password)), 200
