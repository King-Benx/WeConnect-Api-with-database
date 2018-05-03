import json
from test_base import TestBase
from flask import url_for, request


class TestUserRoutes(TestBase):
    def test_register_user(self):
        response = self.client.post(
            url_for('api.register_new_user'), data=json.dumps(self.new_user))
        self.assertTrue(response.status_code == 201)

    def test_existant_email_at_register(self):
        response = self.client.post(
            url_for('api.register_new_user'), data=json.dumps(self.demo_user))
        self.assertTrue(response.status_code == 400)

    def test_missing_values_register_user(self):
        response = self.client.post(
            url_for('api.register_new_user'),
            data=json.dumps(self.missing_email_in_new_user))
        self.assertTrue(response.status_code == 400)

    def test_empty_credentials_register_user(self):
        response = self.client.post(
            url_for('api.register_new_user'),
            data=json.dumps(self.empty_record))
        self.assertTrue(response.status_code == 400)

    def test_wrong_email_at_register_user(self):
        response = self.client.post(
            url_for('api.register_new_user'),
            data=json.dumps(self.invalid_email_in_new_user))
        self.assertTrue(response.status_code == 400)

    def test_wrong_username_at_register_user(self):
        response = self.client.post(
            url_for('api.register_new_user'),
            data=json.dumps(self.invalid_username_in_new_user))
        self.assertTrue(response.status_code == 400)

    def test_short_password_at_register_user(self):
        response = self.client.post(
            url_for('api.register_new_user'),
            data=json.dumps(self.short_password_in_new_user))
        self.assertTrue(response.status_code == 400)

    def test_login(self):
        response = self.client.post(
            url_for('api.login'), data=json.dumps(self.login_user))
        self.assertTrue(response.status_code == 200)

    def test_empty_login_credentials(self):
        response = self.client.post(
            url_for('api.login'), data=json.dumps(self.empty_record))
        self.assertTrue(response.status_code == 404)

    def test_wrong_email_at_login(self):
        response = self.client.post(
            url_for('api.login'),
            data=json.dumps(self.invalid_email_credentials))
        self.assertTrue(response.status_code == 401)

    def test_wrong_password_at_login(self):
        response = self.client.post(
            url_for('api.login'),
            data=json.dumps(self.invalid_password_credentials))
        self.assertTrue(response.status_code == 401)

    def test_wrong_email_format_at_login(self):
        response = self.client.post(
            url_for('api.login'),
            data=json.dumps(self.invalid_email_format_at_login))
        self.assertTrue(response.status_code == 400)

    def test_reset_password(self):
        response = self.client.post(
            url_for('api.reset_password'),
            data=json.dumps(self.new_password),
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 200)

    def test_unauthorized_user_at_reset_password(self):
        response = self.client.post(
            url_for('api.reset_password'), data=json.dumps(self.new_password))
        self.assertTrue(response.status_code == 401)

    def test_no_data_at_reset_password(self):
        response = self.client.post(
            url_for('api.reset_password'),
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 400)

    def test_more_fields_at_reset_password(self):
        response = self.client.post(
            url_for('api.reset_password'),
            data=json.dumps(self.more_data_at_reset),
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 400)

    def test_logout_user(self):
        response = self.client.post(
            url_for('api.logout_user'), headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 200)

    def test_unauthorized_at_logout_user(self):
        response = self.client.post(url_for('api.logout_user'))
        self.assertTrue(response.status_code == 401)
