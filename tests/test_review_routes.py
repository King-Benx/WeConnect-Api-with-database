import json
from test_base import TestBase
from flask import url_for, request


class TestReviewRoutes(TestBase):
    """Tests all routes concerning reviews"""

    # Tests all routes concerning posting reviews
    def test_post_review(self):
        response = self.client.post(
            url_for('api.post_review', businessId=self.default_business.id),
            data=json.dumps(self.create_review),
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 201)

    def test_unknown_business_id_at_post_review(self):
        response = self.client.post(
            url_for('api.post_review', businessId=2),
            data=json.dumps(self.create_review),
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 404)

    def test_unauthorized_user_at_post_review(self):
        response = self.client.post(
            url_for('api.post_review', businessId=1),
            data=json.dumps(self.create_review))
        self.assertTrue(response.status_code == 401)

    # Tests all routes concerning getting reviews
    def test_get_reviews(self):
        response = self.client.get(
            url_for('api.get_reviews', businessId=self.default_business.id),
            data=json.dumps(self.create_review),
            headers={'x-access-token': self.token})
        self.assertTrue(response.status_code == 200)

    def test_unauthorized_user_at_get_reviews(self):
        response = self.client.get(
            url_for('api.get_reviews', businessId=self.default_business.id),
            data=json.dumps(self.create_review))
        self.assertTrue(response.status_code == 401)

    def test_unknown_business_at_get_reviews(self):
        response = self.client.get(
            url_for('api.get_reviews', businessId=2),
            headers={'x-access-token': self.token},
            data=json.dumps(self.create_review))
        self.assertTrue(response.status_code == 404)
