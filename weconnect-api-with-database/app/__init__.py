from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from config import config

db = SQLAlchemy()
swagger = Swagger()

def create_app(config_name):
    # instantiate the application and packages required
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    swagger.init_app(app)
    # create blueprint of the api
    from .api_v_1 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_ref='/api/v1/')
    # create blueprint for the main application
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
