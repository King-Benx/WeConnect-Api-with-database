from . import main


@main.app_errorhandler(404)
def page_not_known(e):
    return 'unknown page', 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return 'internal server error', 500
