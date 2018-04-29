import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Common configurations"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very hard key'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """Development configurations"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE') or 'sqlite:////' + os.path.join(
            basedir, 'dev-data.sqlite')


class ProductionConfig(Config):
    """Production configurations"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('WECONNECT_DATABASE')


class StagingConfig(Config):
    """Staging configurations"""
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('STAGING_DATABASE')


class TestingConfig(Config):
    """Testing Configurations"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE') or 'sqlite:////' + os.path.join(
            basedir, 'test-data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'staging': StagingConfig,
    'default': DevelopmentConfig
}
