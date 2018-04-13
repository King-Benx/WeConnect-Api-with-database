import re
from flask import jsonify
"""These are custom messages for handling json replies """


def make_json_reply(message):
    json_message = {'message': message}
    return jsonify(json_message)


def check_validity_of_mail(email):
    return re.match(
        '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
        email)


def check_validity_of_username(username):
    return re.match('^[^.]*[a-zA-Z]$', username)
