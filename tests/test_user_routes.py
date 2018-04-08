import json
from test_base import TestBase
from flask import url_for, request


class TestUserRoutes(TestBase):
    def test_register_user(self):
        response = self.client.post(
            url_for('api.register_new_user'),
            data=json.dumps(self.create_demo_user))
        self.assertTrue(response.status_code == 201)

    def test_missing_values_register_user(self):
        response = self.client.post(
            url_for('api.register_new_user'),
            data=json.dumps(self.wrong_create_demo_user))
        self.assertTrue(response.status_code == 400)

    def test_empty_credentials_create_uer(self):
        response = self.client.post(
            url_for('api.register_new_user'),
            data=json.dumps(self.empty_create_demo_user))
        self.assertTrue(response.status_code == 400)

    def test_login(self):
        response = self.client.post(
            url_for('api.login'), data=json.dumps(self.login_user))
        self.assertTrue(response.status_code == 200)

    def test_empty_login_credentials(self):
        response = self.client.post(
            url_for('api.login'), data=json.dumps(self.empty_login_user))
        self.assertTrue(response.status_code == 404)

    def test_wrong_email_at_login(self):
        response = self.client.post(
            url_for('api.login'),
            data=json.dumps(self.wrong_email_credentials))
        self.assertTrue(response.status_code == 401)
    
    def test_wrong_password_at_login(self):
        response = self.client.post(
            url_for('api.login'),
            data=json.dumps(self.wrong_password_credentials))
        self.assertTrue(response.status_code == 401)

    def test_reset_password(self):
        response = self.client.post(
            url_for('api.reset_password'),
            data=json.dumps(self.set_new_password),
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 200)

    def test_logout_user(self):
        response = self.client.post(
            url_for('api.logout_user'), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 200)
