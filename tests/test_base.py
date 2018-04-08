import unittest
import jwt
import datetime
from flask import request
from app import create_app, db
from app.api_v_1 import api
from config import Config
from app.api_v_1.user import User
from app.api_v_1.business import Business
from app.api_v_1.reviews import Review


class TestBase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.default_user = User(
            username="user", password="pass", email="johndoe@mail.com")
        self.default_business = Business(
            user_id=1,
            name='business 1',
            location='location 1',
            description='business 1 description',
            category='category 1')
        self.default_review = Review(
            user_id=1, business_id=1, review='review 1')
        db.session.add_all(
            [self.default_user, self.default_business, self.default_review])
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
    wrong_create_demo_user = {
        'username': 'wrong user',
        'password': 'wrong pass'
    }
    empty_create_demo_user = {'username': '', 'password': '', 'email': ''}
    login_user = {'password': 'pass', 'email': 'johndoe@mail.com'}

    empty_login_user = {}

    empty_business = {}

    wrong_email_credentials = {'password': 'pass', 'email': 'janedoe@mail.com'}
    set_new_password = {'new_password': 'newpass'}

    wrong_password_credentials = {
        'password': 'wrongpass',
        'email': 'johndoe@mail.com'
    }

    create_new_business = {
        'name': 'business 1',
        'location': 'location 1',
        'category': 'category 1',
        'description': 'business description 1'
    }

    create_business_update = {
        'name': ' new business 1',
        'location': 'new location 1',
        'category': 'new category 1',
        'description': 'new business description 1'
    }

    create_review = {'review': 'review 1'}

    token = jwt.encode(
        {
            'id': 1,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=20)
        },
        Config.SECRET_KEY)
