import json
from test_base import TestBase
from flask import url_for, request


class TestBusinessRoutes(TestBase):
    def test_register_business(self):
        response = self.client.post(
            url_for('api.register_business'),
            data=json.dumps(self.create_new_business),
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 201)

    def test_update_business(self):
        response = self.client.put(
            url_for(
                'api.update_business', businessId=self.default_business.id),
            data=json.dumps(self.create_business_update),
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 200)

    def test_delete_business(self):
        response = self.client.delete(
            url_for(
                'api.delete_business', businessId=self.default_business.id),
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 200)

    def test_retrieve_all_businesses(self):
        response = self.client.get(
            url_for('api.retrieve_all_businesses'),
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 200)

    def test_retrieve_a_businesses(self):
        response = self.client.get(
            url_for(
                'api.retrieve_a_business',
                businessId=self.default_business.id),
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 200)

    def test_retrieve_a_business_by_name(self):
        response = self.client.get(
            url_for('api.retrieve_a_business_by_name') +
            '?q=business 1&page=1&limit=1',
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 200)

    def test_filter_business(self):
        response = self.client.get(
            url_for('api.filter_business') +
            '?filter_type=location&filter_value=location 1&page=1&limit=1',
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 200)
