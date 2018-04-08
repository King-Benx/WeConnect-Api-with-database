from flask import jsonify
"""These are custom messages for handling json replies """


def make_json_reply(title, message):
    json_message = {title: message}
    return jsonify(json_message)
