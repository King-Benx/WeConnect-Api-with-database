import re
from flask import jsonify
"""These are custom messages for handling json replies """


def make_json_reply(title, result):
    json_message = {title: result}
    return jsonify(json_message)


def check_validity_of_mail(email):
    return re.match(
        '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
        email)


def check_validity_of_username(username):
    return re.match('^[^.]*[a-zA-Z]$', username)


def check_validity_of_input(**kwargs):
    for key, value in kwargs.items():
        if value is not None and value != '' and len(value) != 0:
            return True
        else:
            return False
