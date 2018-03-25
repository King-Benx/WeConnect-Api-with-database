from flask import request, jsonify, session, url_for
from . import api
from ..models import Review, User, Business
from ..functions import make_json_reply
from .authentication import token_required
from .. import db


@api.route('/api/v1/businesses/<businessId>/reviews', methods=['POST'])
@token_required
def post_review(current_user, businessId):
    # create a review for a business
    data = request.get_json()
    if len(data.keys()) == 1:
        user_id = current_user.id
        business_id = int(businessId)
        if Business.query.get(business_id):
            user_review = data['review']
            review = Review(
                user_id=user_id, business_id=business_id, review=user_review)
            db.session.add(review)
            if review:
                return make_json_reply('message',
                                       'review successfully created'), 201
        else:
            return make_json_reply(
                'message',
                'cannot create review for none existant business'), 400
    else:
        return make_json_reply(
            'message', 'cannot create review due to missing fields'), 400


@api.route('/api/v1/businesses/<businessId>/reviews', methods=['GET'])
@token_required
def get_reviews(current_user, businessId):
    # get reviews for business
    if Business.query.get(int(businessId)):
        reviews = Review.query.filter_by(business_id=int(businessId))
        if Review.query.filter_by(business_id=int(businessId)).count() > 0:
            return jsonify('Reviews',
                           [review.to_json() for review in reviews]), 200
        else:
            return make_json_reply('message', 'No reviews for business'), 200
    else:
        return make_json_reply('message', 'None existant business id'), 400
