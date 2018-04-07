import unittest
import jwt
import datetime
from flask import request
from app import create_app, db
from app.api_v_1 import api
from config import Config
from app.api_v_1.user import User


class TestBase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        default_user = User(
            username="user", password="pass", email="johndoe@mail.com")
        db.session.add(default_user)
        db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    create_demo_user = {
        'username': 'user',
        'password': 'pass',
        'email': 'johndoe@mail.com'
    }
    login_user = {'password': 'pass', 'email': 'johndoe@mail.com'}

    set_new_password = {
        'new_password': 'newpass',
    }

    new_business = {
        'name': 'business 1',
        'location': 'location 1',
        'category': 'category 1',
        'description': 'business description 1'
    }
    token = jwt.encode(
        {
            'id': 1,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=20)
        },
        Config.SECRET_KEY)
