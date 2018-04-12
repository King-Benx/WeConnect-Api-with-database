import json
from test_base import TestBase
from flask import url_for, request


class TestBusinessRoutes(TestBase):
    """Tests all routes concerning businesses """

    # Tests for regsitration

    def test_register_business(self):
        response = self.client.post(
            url_for('api.register_business'),
            data=json.dumps(self.create_new_business),
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 201)

    def test_missing_fields_at_register_business(self):
        response = self.client.post(
            url_for('api.register_business'),
            data=json.dumps(self.empty_record),
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 400)

    def test_no_data_at_register_business(self):
        response = self.client.post(
            url_for('api.register_business'),
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 400)

    def test_unauthorized_user_at_register_business(self):
        response = self.client.post(
            url_for('api.register_business'),
            data=json.dumps(self.create_new_business))
        self.assertTrue(response.status_code == 401)

    # Tests for updating a busines
    def test_update_business(self):
        response = self.client.put(
            url_for('api.update_business', businessId=1),
            data=json.dumps(self.create_business_update),
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 200)

    def test_unauthorized_user_at_update_business(self):
        response = self.client.put(
            url_for('api.update_business', businessId=1),
            data=json.dumps(self.create_business_update))
        self.assertTrue(response.status_code == 401)

    def test_no_data_at_update_business(self):
        response = self.client.put(
            url_for('api.update_business', businessId=1),
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 400)

    def test_wrong_business_id_at_update_business(self):
        response = self.client.put(
            url_for('api.update_business', businessId=2),
            data=json.dumps(self.create_business_update),
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 404)

    # Tests for deleting a business
    def test_delete_business(self):
        response = self.client.delete(
            url_for('api.delete_business', businessId=1),
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 200)

    def test_unauthorized_user_at_delete_business(self):
        response = self.client.delete(
            url_for('api.delete_business', businessId=1))
        self.assertTrue(response.status_code == 401)

    def test_wrong_business_id_at_delete_business(self):
        response = self.client.delete(
            url_for('api.delete_business', businessId=2),
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 404)

    # Tests for retrieving all businesses
    def test_retrieve_all_businesses(self):
        response = self.client.get(
            url_for('api.retrieve_all_businesses'),
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 200)

    def test_unauthorized_user_at_retrieve_all_businesses(self):
        response = self.client.get(url_for('api.retrieve_all_businesses'))
        self.assertTrue(response.status_code == 401)

    # Tests retrieval of a single business
    def test_retrieve_a_businesses(self):
        response = self.client.get(
            url_for('api.retrieve_a_business', businessId=1),
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 200)

    def test_unauthorized_user_at_retrieve_a_business(self):
        response = self.client.get(
            url_for('api.retrieve_a_business', businessId=1))
        self.assertTrue(response.status_code == 401)

    def test_unknown_business_at_retrieve_a_business(self):
        response = self.client.get(
            url_for('api.retrieve_a_business', businessId=2),
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 404)

    # Tests retrieval of a business by name
    def test_retrieve_a_business_by_name(self):
        response = self.client.get(
            url_for('api.retrieve_a_business_by_name') +
            '?q=business 1&page=1&limit=1',
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 200)

    def test_unauthorized_user_at_retrieve_a_business_by_name(self):
        response = self.client.get(
            url_for('api.retrieve_a_business_by_name') +
            '?q=business 1&page=1&limit=1')
        self.assertTrue(response.status_code == 401)

    def test_unknown_business_at_retrieve_a_business_by_name(self):
        response = self.client.get(
            url_for('api.retrieve_a_business_by_name') +
            '?q=business 2&page=1&limit=1',
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 404)

    # Tests for filter business
    def test_filter_business(self):
        response = self.client.get(
            url_for('api.filter_business') +
            '?filter_type=location&filter_value=location 1&page=1&limit=1',
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 200)

    def test_unauthorized_user_at_filter_business(self):
        response = self.client.get(
            url_for('api.filter_business') +
            '?filter_type=location&filter_value=location 1&page=1&limit=1')
        self.assertTrue(response.status_code == 401)

    def test_wrong_filter_at_filter_business(self):
        response = self.client.get(
            url_for('api.filter_business') +
            '?filter_type=wrong filter&filter_value=location 1&page=1&limit=1',
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 400)

    def test_unknown_filter_at_filter_business(self):
        response = self.client.get(
            url_for('api.filter_business') +
            '?filter_type=location&filter_value=location 2&page=1&limit=1',
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 404)
