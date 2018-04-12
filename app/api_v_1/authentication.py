import jwt
import datetime
from flask import request, url_for, make_response
from flasgger import swag_from
from ..models import User, BlackListedTokens
from config import Config
from . import api
from functools import wraps
from ..functions import make_json_reply, check_validity_of_mail


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
@swag_from('swagger/users/login_user.yml')
def login():
    """Login registered users into systems and assign a token"""
    data = request.get_json(force=True)
    if len(data.keys()) == 2:
        email = data['email']
        password = data['password']
        if check_validity_of_mail(email) != None:
            if User.query.filter_by(email=email).count() == 0:
                return make_response(
                    "Could not verify! wrong email, Try again " +
                    str(url_for('api.login', _external=True))), 401
            else:
                user = User.query.filter_by(email=email).first()
                password_validity = user.check_password(password)
                if not password_validity:
                    return make_response(
                        "Could not verify! password incorrect, Try again " +
                        str(url_for('api.login', _external=True))), 401
                else:
                    token = jwt.encode(
                        {
                            'id':
                            user.id,
                            'exp':
                            datetime.datetime.utcnow() +
                            datetime.timedelta(minutes=20)
                        },
                        Config.SECRET_KEY)
                    return make_json_reply('Use Token',
                                           token.decode('UTF-8')), 200
        else:
            return make_json_reply('Error', 'Invalid Email, Try again'), 400
    else:
        return make_response("Unknown user, register now or try to Login again"
                             + str(url_for('api.login', _external=True))), 404
