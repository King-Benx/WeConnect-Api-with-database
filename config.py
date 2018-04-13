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
        'DEV-DATABASE') or 'sqlite:////' + os.path.join(
            basedir, 'dev-data.sqlite')


class ProductionConfig(Config):
    """Production configurations"""
    POSTGRES = {
        'user': 'yugdidzdtdvtbs',
        'pw':
        '382f60e76260d3ead5021451626b644aaa35753b49e5b0274085cd1f5bf71555',
        'db': 'd763a6843un291',
        'host': 'ec2-54-225-96-191.compute-1.amazonaws.com',
        'port': '5432',
    }
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'WECONNECT-DATABASE'
    ) or 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


class StagingConfig(Config):
    """Staging configurations"""
    POSTGRES = {
        'user': 'postgres',
        'pw': 'pass',
        'db': 'weconnect',
        'host': 'localhost',
        'port': '5432',
    }
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'WECONNECT-DATABASE'
    ) or 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


class TestingConfig(Config):
    """Testing Configurations"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST-DATABASE') or 'sqlite:////' + os.path.join(
            basedir, 'test-data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'staging': StagingConfig,
    'default': ProductionConfig
    # 'default': DevelopmentConfig
}
