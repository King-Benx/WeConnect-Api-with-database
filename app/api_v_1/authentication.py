import jwt
import datetime
from flask import request
from flasgger import swag_from
from ..models import User, BlackListedTokens
from config import Config
from . import api
from functools import wraps
from ..functions import make_json_reply, check_validity_of_mail


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        """
        checks token and creates a current_user object with users information
        """
        token = None

        if 'x-access-token' in request.headers and BlackListedTokens.query.filter_by(
                token=request.headers['x-access-token']).count() == 0:
            token = request.headers['x-access-token']
        else:
            return make_json_reply(
                'message',
                'Token no longer valid, user signed out! Login again '), 401

        if not token:
            return make_json_reply('message',
                                   'Unauthorized access token is missing'), 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY)
            current_user = User.query.get(int(data['id']))
        except:
            return make_json_reply('message', 'Token is invalid'), 401

        return f(current_user, *args, **kwargs)

    return decorated


@api.route('/api/v1/auth/login', methods=['POST'])
@swag_from('swagger/users/login_user.yml')
def login():
    """
    Login registered users into systems and assign a token
    """
    data = request.get_json(force=True)

    if len(data.keys()) != 2:
        return make_json_reply(
            'message', "Unknown user, register now or try to Login again"), 404

    email = data['email']
    password = data['password']

    if check_validity_of_mail(email) == None:
        return make_json_reply('message', 'Invalid Email, Try again'), 400

    if User.query.filter_by(email=email).count() == 0:
        return make_json_reply('message',
                               "Could not verify! wrong email, Try again "), 401

    user = User.query.filter_by(email=email).first()
    password_validity = user.check_password(password)

    if not password_validity:
        return make_json_reply(
            'message', "Could not verify! password incorrect, Try again "), 401

    token = jwt.encode(
        {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=40)
        },
        Config.SECRET_KEY)

    return make_json_reply(
        'message', {
            'user_status': 'Successfully Logged in',
            'username': user.username,
            'email': email,
            'token': token.decode('UTF-8')
        }), 200
