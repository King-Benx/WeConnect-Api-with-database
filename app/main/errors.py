from . import main
from flask import request
from app.functions import make_json_reply


@main.app_errorhandler(404)
def page_not_known(e):
    """Error handler for unknown routes"""
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = make_json_reply({'Not found'})
        response.status_code = 404
        return response
    return 'Page Not found', 404


@main.app_errorhandler(500)
def internal_server_error(e):
    """Error handler for server errors"""
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = make_json_reply({'Internal server error'})
        response.status_code = 500
        return response
    return 'Internal Server Error', 500
