import unittest
import json
import jwt
import datetime
from flask import request, url_for
from app import create_app, db
from app.api_v_1 import api
from config import Config


class TestBase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()
        self.client.post(
            url_for('api.register_new_user'),
            data=json.dumps(self.create_demo_user))
        login_test_user = self.client.post(
            url_for('api.login'), data=json.dumps(self.login_user))
        user_logged_in_data = json.loads(login_test_user.data.decode())
        self.token = user_logged_in_data['message']['token']

        self.client.post(
            url_for('api.register_business'),
            data=json.dumps(self.create_new_business),
            headers={'x-access-token': self.token})
        self.client.post(
            url_for('api.post_review', businessId=1),
            data=json.dumps(self.create_review),
            headers={'x-access-token': self.token})

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    create_demo_user = {
        'username': 'johndoe',
        'password': 'password',
        'email': 'johndoe@mail.com'
    }
    create_new_user = {
        'username': 'janedoe',
        'password': 'password2',
        'email': 'janedoe@mail.com'
    }
    wrong_create_demo_user = {
        'username': 'wrong user',
        'password': 'wrong pass'
    }
    short_password_at_create_demo_user = {
        'username': 'janedoe',
        'password': 'pa',
        'email': 'janedoe@mail.com'
    }
    wrong_username_at_create_demo_user = {
        'username': '.john',
        'password': 'password',
        'email': 'janedoe@mail.com'
    }
    wrong_email_at_create_demo_user = {
        'username': 'johndoe',
        'password': 'password',
        'email': 'john.mail'
    }
    empty_create_demo_user = {'username': '', 'password': '', 'email': ''}
    login_user = {'password': 'password', 'email': 'johndoe@mail.com'}

    empty_record = {}

    wrong_email_credentials = {'password': 'pass', 'email': 'janedoe@mail.com'}
    wrong_email_at_format_at_login = {'password': 'pass', 'email': '.'}
    set_new_password = {'new_password': 'newpass_2'}
    set_same_password = {'new_password': 'password'}
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
