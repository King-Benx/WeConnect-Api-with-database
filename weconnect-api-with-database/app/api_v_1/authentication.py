import jwt
import datetime
from flask import jsonify, request, url_for, make_response
from ..models import User
from . import api
from functools import wraps
from ..functions import make_json_reply


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # checks token and creates a current_user object with users information
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_json_reply('message ',
                                   'Unauthorized access token is missing'), 401
        try:
            data = jwt.decode(token, SECRET_KEY)
            current_user = User.get_user(user_id=data['id'])
        except:
            return make_json_reply('message', 'Token is invalid'), 401
        return f(current_user, *args, **kwargs)

    return decorated


@api.route('/api/v1/auth/login', methods=['POST'])
def login():
    # This logs a registered user into system and creates a unique token for them
    auth = request.authorization

    if not auth or not auth.username and auth.password:
        return make_response(
            "Could not verify", 401, {
                'WWW-Authenticate':
                'Basic Realm="url_for(\'api.login\',_external=True)"'
            })

    user = User.login(auth.username, auth.password)
    if not user:
        return make_response(
            "Could not verify! if you are not a user register otherwise try again",
            401, {
                'WWW-Authenticate':
                'Basic Realm =' + str(url_for('api.login', _external=True))
            })
    if user:
        token = jwt.encode(
            {
                'id': User.get_user_id_by_username(auth.username),
                'exp':
                datetime.datetime.utcnow() + datetime.timedelta(minutes=20)
            },
            SECRET_KEY)
        return make_json_reply('token', token.decode('UTF-8')), 200
    else:
        return make_response(
            "Could not verify! if you are not a user, register otherwise try again"
            + str(url_for('api.login', _external=True))), 401
