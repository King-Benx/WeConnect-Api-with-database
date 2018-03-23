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
        user_information = User.query.filter_by(username=current_user[0])
        user_id = user_information.id
        business_id = int(businessId)
        if Business.query.get_or_404(business_id):
            review = data['review']
            review = Review(user_id, business_id, review)
            db.session.add(review)
            if review:
                return make_json_reply('message',
                                       'review successfully created'), 201
            else:
                return make_json_reply(
                    'message',
                    'cannot create review due to missing fields'), 400
        else:
            return make_json_reply(
                'message',
                'cannot create review fro none existant business'), 400


@api.route('/api/v1/businesses/<businessId>/reviews', methods=['GET'])
@token_required
def get_reviews(current_user, businessId):
    # get reviews for business
    if Business.query.get_404(int(businessId)):
        reviews = Review.query.filter_by(business_id=int(businessId))
        if reviews:
            return jsonify(reviews), 200
        else:
            return make_json_reply('message', 'No reviews for business'), 200
    else:
        return make_json_reply('message', 'None existant business id'), 400
