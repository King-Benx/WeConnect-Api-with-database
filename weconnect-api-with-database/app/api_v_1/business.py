from flask import request, url_for, session, jsonify
from . import api
from .. import db
from ..models import Business, User
from .authentication import token_required
from ..functions import make_json_reply


@api.route('/api/v1/businesses', methods=['POST'])
@token_required
def register_business(current_user):
    # register new business into the system
    data = request.get_json()
    if data:
        if (len(data.keys()) == 4):
            user_id = current_user.id
            name = data['name']
            location = data['location']
            category = data['category']
            description = data['description']
            business = Business(
                user_id=user_id,
                name=name,
                location=location,
                category=category,
                description=description)
            db.session.add(business)
            if business:
                return make_json_reply('message', 'business ' + str(
                    business.name) + ' successfully created'), 201
            else:
                return make_json_reply(
                    'message',
                    'cannot create business due to missing fields'), 400
    else:
        return make_json_reply(
            'message', 'cannot create business due to missing fields'), 400


@api.route('/api/v1/businesses/<businessId>', methods=['PUT'])
@token_required
def update_business(current_user, businessId):
    # update business
    check_business_by_id = Business.query.get(int(businessId))
    if check_business_by_id:
        data = request.get_json()
        name = data['name']
        location = data['location']
        category = data['category']
        description = data['description']
        user_information = User.query.filter_by(username=current_user.username)
        user_id = user_information.id
        if check_business_by_id.user_id == user_id:
            if name != '' and name != check_business_by_id.name:
                check_business_by_id.name = name
            if location != '' and location != check_business_by_id.location:
                check_business_by_id.location = location
            if category != '' and category != check_business_by_id.category:
                check_business_by_id.category = category
            if description != '' and description != check_business_by_id.description:
                check_business_by_id.description = description
            db.session.add(check_business_by_id)
            if check_business_by_id:
                return make_json_reply(
                    'message',
                    'successfully updated business ' + str(name)), 201
            else:
                return make_json_reply('message',
                                       'Failure updating ' + str(name)), 400
    else:
        return make_json_reply('message', 'Business id does not exist'), 400


@api.route('/api/v1/businesses/<businessId>', methods=['DELETE'])
@token_required
def delete_business(current_user, businessId):
    # delete business by id
    check_business_by_id = Business.query.get(int(businessId))
    if check_business_by_id and check_business_by_id.user_id == current_user.id:
        business_name = check_business_by_id.name
        db.session.delete(check_business_by_id)
        return make_json_reply(
            'message',
            'successfully deleted business ' + str(business_name)), 200
    else:
        return make_json_reply(
            'message',
            'Business id might not exist or you have no right to delete business'
        ), 404


@api.route('/api/v1/businesses', methods=['GET'])
@token_required
def retrieve_all_businesses(current_user):
    # retrieve all businesses
    if Business.query.count() > 0:
        businesses = Business.query.all()
        return jsonify('Businesses ',
                       [business.to_json() for business in businesses]), 200
    else:
        return make_json_reply(
            'message', 'No businesses registered currently, register one at ' +
            str(url_for('api.register_business', _external=True))), 404


@api.route('/api/v1/businesses/<businessId>', methods=['GET'])
@token_required
def retrieve_a_business(current_user, businessId):
    # retrieve a single businesses
    if Business.query.get(int(businessId)):
        specific_business = Business.query.get_or_404(int(businessId))
        if specific_business:
            return jsonify('Business', specific_business.to_json()), 200
        else:
            return make_json_reply(
                'message',
                'No businesses registered with that id currently, view all businesses at '
                + str(url_for('api.retrieve_all_businesses',
                              _external=True))), 400
    else:
        return make_json_reply(
            'message',
            'No businesses registered with that id currently, view all businesses at '
            + str(url_for('api.retrieve_all_businesses', _external=True))), 400
