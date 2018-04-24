from flask import request, url_for, session
from flasgger import swag_from
from . import api
from ..models import User, BlackListedTokens
from .. import db
from .authentication import token_required
from ..functions import make_json_reply, check_validity_of_mail, check_validity_of_username, check_validity_of_input


@api.route('/api/v1/auth/register', methods=['POST'])
@swag_from('swagger/users/create_user.yml')
def register_new_user():
    """Register new user into system basing on a username, email and password given in the json"""
    data = request.get_json(force=True)
    if len(data.keys()) != 3:
        return make_json_reply(
            'Couldn\'t create user, some fields missing'), 400

    username = data['username']
    email = data['email']
    password = data['password']
    if check_validity_of_input(username=username,email=email,password=password) != True:
        return make_json_reply('Values cannot be empty or not set'), 400
    if User.query.filter_by(email=email).count() == 1:
        return make_json_reply('Email already exists, try again'), 400
    if check_validity_of_mail(email) == None:
        return make_json_reply('Invalid email'), 400
    if len(password) < 3:
        return make_json_reply('Password too short'), 400
    if len(username) < 3 or check_validity_of_username(
                    username) == None:
            return make_json_reply(
                    'Username either too short or cannot start with a . '), 400
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    return make_json_reply('Successfully created user ' + str(
                        username) + ' you can login using ' + str(
                            url_for('api.login', _external=True))), 201
                
# More work to be done on signing out
@api.route('/api/v1/auth/logout', methods=['POST'])
@swag_from('swagger/users/logout_user.yml')
@token_required
def logout_user(current_user):
    """Logout current user from the system"""
    request.authorization = None
    current_user = None
    blacklist_token = request.headers['x-access-token']
    blacklist = BlackListedTokens(token=blacklist_token)
    db.session.add(blacklist)
    db.session.commit()
    if blacklist_token and not request.authorization:
        return make_json_reply('You have been successfully logout'), 200
    else:
        return make_json_reply('Something went wrong, please try again ' + str(
            url_for('api.logout_user', _external=True))), 400


@api.route('/api/v1/auth/reset-password', methods=['POST'])
@swag_from('swagger/users/reset_password.yml')
@token_required
def reset_password(current_user):
    """Changes the password of a user to new_password in json set"""
    data = request.get_json(force=True)
    if (len(data.keys()) != 1):
        return make_json_reply(
            'Couldn\'t set password due missing fields'), 400
    password = data['new_password']
    user_data = User.query.get(current_user.id)
    user_data.password = password
    db.session.add(user_data)
    if  user_data.check_password(password) != True:
        return make_json_reply(
                'Failure resetting password, username invalid'), 400      
    return make_json_reply(
            'Password has been set to ' + str(password)), 200
      
       
