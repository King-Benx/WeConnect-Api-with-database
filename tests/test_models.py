import unittest
from app.models import User, Business, Review, BlackListedTokens


class TestModels(unittest.TestCase):
    """Tests the model representations in the models"""

    def test_user_repr(self):
        user = User(
            username='janedoe', password='pass', email='janedoe@mail.com')
        self.assertTrue(user.__repr__() == "User 'janedoe'")
        with self.assertRaises(AttributeError): user.password


    def test_business_repr(self):
        business = Business(
            user_id=1,
            name='business 1',
            location='location 1',
            description='business description')
        self.assertTrue(business.__repr__() == "Business name 'business 1'")

    def test_review_repr_(self):
        review = Review(user_id=1, business_id=1, review='business 1 review')
        self.assertTrue(review.__repr__() == "Review 'business 1 review'")

    def test_blacklistedtokens_repr(self):
        blacklistedtokens = BlackListedTokens(token='abcdefghijklmnopqrs')
        self.assertTrue(blacklistedtokens.__repr__() ==
                        "Blacklisted Token : 'abcdefghijklmnopqrs'")
