from . import main
from flask import request, jsonify


@main.app_errorhandler(404)
def page_not_known(e):
    """Error handler for unknown routes"""
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return 'Page Not found', 404


@main.app_errorhandler(500)
def internal_server_error(e):
    """Error handler for server errors"""
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    return 'Internal Server Error', 500
