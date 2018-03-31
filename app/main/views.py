from flask import redirect, url_for
from . import main


@main.route('/')
def index():
    return redirect(str(url_for('main.index', _external=True)) + 'apidocs')
