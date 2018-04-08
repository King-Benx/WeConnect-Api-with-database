import json
from test_base import TestBase
from flask import url_for, request


class TestReviewRoutes(TestBase):
    def test_post_review(self):
        response = self.client.post(
            url_for('api.post_review',businessId=self.default_business.id),
            data=json.dumps(self.create_review), headers={'x-access-token':self.token})
        self.assertTrue(response.status_code == 201)

    def test_get_reviews(self):
        response = self.client.get(
            url_for('api.get_reviews',businessId=self.default_business.id),
            data=json.dumps(self.create_review), headers={'x-access-token':self.token})
        self.assertTrue(response.status_code == 200)
