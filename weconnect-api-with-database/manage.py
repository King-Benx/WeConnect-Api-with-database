import os
from app import create_app
from flask_script import Manager
from flask_script import Shell

app = create_app(os.getenv('APPLICATION_CONFIG') or 'default')
manager = Manager(app)


@manager.command
def run_test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def deploy():
    pass


def make_shell_context():
    return dict(app=app, User=User, Business=Business, Review=Review)


manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()