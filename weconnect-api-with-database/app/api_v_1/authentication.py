import jwt
import datetime
from flask import jsonify, request, url_for, make_response
from ..models import User, BlackListedTokens
from config import Config
from . import api
from functools import wraps
from ..functions import make_json_reply


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        """checks token and creates a current_user object with users information"""
        token = None
        if 'x-access-token' in request.headers and BlackListedTokens.query.filter_by(
                token=request.headers['x-access-token']).count() == 0:
            token = request.headers['x-access-token']
        else:
            return make_json_reply(
                'Error',
                'Token no longer valid, user signed out! Login again ' + str(
                    url_for('api.login', _external=True))), 401
        if not token:
            return make_json_reply('message ',
                                   'Unauthorized access token is missing'), 401
        try:
            data = jwt.decode(token, Config.SECRET_KEY)
            current_user = User.query.get(int(data['id']))
        except:
            return make_json_reply('message', 'Token is invalid'), 401
        return f(current_user, *args, **kwargs)

    return decorated


@api.route('/api/v1/auth/login', methods=['POST'])
def login():
    """Login registered users into systems and assign a token"""
    auth = request.authorization

    if not auth or not auth.username and auth.password:
        return make_response(
            "Could not verify", 401, {
                'WWW-Authenticate':
                'Basic Realm="url_for(\'api.login\',_external=True)"'
            })
    if User.query.filter_by(username=auth.username).count() == 0:
        return make_response("Could not verify! wrong username, Try again " +
                             str(url_for('api.login', _external=True))), 401

    user = User.query.filter_by(username=auth.username).first()
    if not user.check_password(auth.password):
        return make_response(
            "Could not verify! if you are not a user register otherwise try again",
            401, {
                'WWW-Authenticate':
                'Basic Realm =' + str(url_for('api.login', _external=True))
            })
    if user.check_password(auth.password):
        token = jwt.encode(
            {
                'id': user.id,
                'exp':
                datetime.datetime.utcnow() + datetime.timedelta(minutes=20)
            },
            Config.SECRET_KEY)
        return make_json_reply('Use Token', token.decode('UTF-8')), 200
    else:
        return make_response(
            "Could not verify! if you are not a user, register otherwise try to Login again"
            + str(url_for('api.login', _external=True))), 401
