from flask import request, session, url_for
from flasgger import swag_from
from . import api
from ..models import Review, User, Business
from ..functions import make_json_reply
from .authentication import token_required
from .. import db


@api.route('/api/v1/businesses/<int:businessId>/reviews', methods=['POST'])
@swag_from('swagger/reviews/create_reviews.yml')
@token_required
def post_review(current_user, businessId):
    """
    create a review for a business
    """
    data = request.get_json(force=True)

    if len(data.keys()) != 1:
        return make_json_reply(
            'message', 'Cannot create review due to missing fields'), 400

    user_id = current_user.id

    if not Business.query.get(int(businessId)):
        return make_json_reply(
            'message', 'Cannot create review for none existant business'), 404

    user_review = data['review']

    if len(user_review) < 4:
        return make_json_reply(
            'message', 'Cannot create review due to very short review'), 400

    review = Review(
        user_id=user_id, business_id=int(businessId), review=user_review)
    db.session.add(review)

    return make_json_reply('message', 'Review successfully created'), 201


@api.route('/api/v1/businesses/<int:businessId>/reviews', methods=['GET'])
@swag_from('swagger/reviews/get_reviews.yml')
@token_required
def get_reviews(current_user, businessId):
    """
    get reviews for business
    """

    if not Business.query.get(int(businessId)):
        return make_json_reply('message', 'None existant business id'), 404

    reviews = Review.query.filter_by(business_id=int(businessId))
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', reviews.count(), type=int)
    pagination = reviews.paginate(page, per_page=limit, error_out=False)
    business_reviews = pagination.items
    prev = None

    if pagination.has_prev:
        prev = url_for(
            'api.get_reviews',
            businessId=int(businessId),
            page=page - 1,
            _external=True)
    next = None

    if pagination.has_next:
        next = url_for(
            'api.get_reviews',
            businessId=int(businessId),
            page=page + 1,
            _external=True)

    if not business_reviews:
        return make_json_reply('message', 'No reviews for business'), 404

    return make_json_reply(
        'reviews', {
            'business_reviews':
            [review.to_json() for review in business_reviews],
            'prev': prev,
            'next': next
        }), 200
