from flask import request, jsonify, session, url_for
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
    """ create a review for a business"""
    data = request.get_json(force=True)
    if len(data.keys()) == 1:
        user_id = current_user.id
        business_id = int(businessId)
        if Business.query.get(business_id):
            user_review = data['review']
            review = Review(
                user_id=user_id, business_id=business_id, review=user_review)
            db.session.add(review)
            return make_json_reply('message',
                                   'review successfully created'), 201
        else:
            return make_json_reply(
                'message',
                'cannot create review for none existant business'), 404
    else:
        return make_json_reply(
            'message', 'cannot create review due to missing fields'), 400


@api.route('/api/v1/businesses/<int:businessId>/reviews', methods=['GET'])
@swag_from('swagger/reviews/get_reviews.yml')
@token_required
def get_reviews(current_user, businessId):
    """get reviews for business"""
    if Business.query.get(int(businessId)):
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
        if business_reviews:
            return jsonify({
                'Reviews': [review.to_json() for review in business_reviews],
                'prev':
                prev,
                'next':
                next,
                'count':
                pagination.total
            }), 200
        else:
            return make_json_reply('message', 'No reviews for business'), 404
    else:
        return make_json_reply('message', 'None existant business id'), 404
