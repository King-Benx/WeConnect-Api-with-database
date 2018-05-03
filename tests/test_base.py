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
            url_for('api.register_new_user'), data=json.dumps(self.demo_user))
        login_test_user = self.client.post(
            url_for('api.login'), data=json.dumps(self.login_user))
        user_logged_in_data = json.loads(login_test_user.data.decode())
        self.token = user_logged_in_data['message']['token']

        self.client.post(
            url_for('api.register_business'),
            data=json.dumps(self.new_business),
            headers={'x-access-token': self.token})

        self.client.post(
            url_for('api.register_business'),
            data=json.dumps(self.new_business),
            headers={'x-access-token': self.token})

        self.client.post(
            url_for('api.post_review', businessId=1),
            data=json.dumps(self.review),
            headers={'x-access-token': self.token})

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # variables used at creation of user
    demo_user = {
        'username': 'johndoe',
        'password': 'password',
        'email': 'johndoe@mail.com'
    }

    new_user = {
        'username': 'janedoe',
        'password': 'password2',
        'email': 'janedoe@mail.com'
    }

    missing_email_in_new_user = {
        'username': 'wrong user',
        'password': 'wrong pass'
    }

    short_password_in_new_user = {
        'username': 'janedoe',
        'password': 'pa',
        'email': 'janedoe@mail.com'
    }

    invalid_username_in_new_user = {
        'username': '.john',
        'password': 'password',
        'email': 'janedoe@mail.com'
    }

    invalid_email_in_new_user = {
        'username': 'johndoe',
        'password': 'password',
        'email': 'john.mail'
    }

    empty_new_user_info = {'username': '', 'password': '', 'email': ''}

    # variables used at login
    login_user = {'password': 'password', 'email': 'johndoe@mail.com'}

    empty_record = {}

    invalid_email_credentials = {
        'password': 'pass',
        'email': 'janedoe@mail.com'
    }

    invalid_email_format_at_login = {'password': 'pass', 'email': '.'}

    invalid_password_credentials = {
        'password': 'wrongpass',
        'email': 'johndoe@mail.com'
    }

    # variables used at reseting password
    new_password = {'new_password': 'newpass_2'}

    more_data_at_reset = {
        'extra_field': 'blah',
        'password': 'password',
        'new_password': 'password_2'
    }

    # variables used in businesses
    new_business = {
        'name': 'business 1',
        'location': 'location 1',
        'category': 'category 1',
        'description': 'business description 1'
    }

    business_update = {
        'name': ' new business 1',
        'location': 'new location 1',
        'category': 'new category 1',
        'description': 'new business description 1'
    }

    # variables used in reviews
    review = {'review': 'review 1'}

    short_review = {'review': 'rev'}
