from flask import request, url_for, session, jsonify
from . import api
from ..models import Business, User
from .. import known_business_ids, businesses
from .authentication import token_required
from ..functions import make_json_reply


@api.route('/api/v1/businesses', methods=['POST'])
@token_required
def register_business(current_user):
    # register new business into the system
    data = request.get_json()
    if data:
        if (len(data.keys()) == 4):
            user_id = int(User.get_user_id_by_username(current_user[0]))
            name = data['name']
            location = data['location']
            category = data['category']
            description = data['description']
            business = Business(user_id, name, location, category, description)
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
    if int(businessId) in known_business_ids:
        data = request.get_json()
        business_id = int(businessId)
        name = data['name']
        location = data['location']
        category = data['category']
        description = data['description']
        user_id = int(User.get_user_id_by_username(current_user[0]))
        status = Business.update_business(user_id, business_id, name, location,
                                          category, description)
        if status:
            return make_json_reply(
                'message', 'successfully updated business ' + str(name)), 201
        else:
            return make_json_reply('message',
                                   'Failure updating ' + str(name)), 400
    else:
        return make_json_reply('message', 'Business id does not exist'), 400


@api.route('/api/v1/businesses/<businessId>', methods=['DELETE'])
@token_required
def delete_business(current_user, businessId):
    # delete business by id
    business_id = int(businessId)
    if business_id in known_business_ids:
        business_to_be_deleted = Business.get_business_by_id(business_id)
        business_name = business_to_be_deleted[1]
        user_id = int(User.get_user_id_by_username(current_user[0]))
        status = Business.delete_business(user_id, business_id)
        if status:
            return make_json_reply(
                'message',
                'successfully deleted business' + str(business_name)), 200
        else:
            return make_json_reply(
                'message', 'Failure deleting business' + str(business_name))
    else:
        return make_json_reply('message', 'Business id does not exist'), 404


@api.route('/api/v1/businesses', methods=['GET'])
@token_required
def retrieve_all_businesses(current_user):
    # retrieve all businesses
    if businesses:
        return jsonify(Business.get_all_businesses()), 200
    else:
        return make_json_reply(
            'message', 'No businesses registered currently, register one at ' +
            str(url_for('api.register_business', _external=True))), 404


@api.route('/api/v1/businesses/<businessId>', methods=['GET'])
@token_required
def retrieve_a_business(current_user, businessId):
    # retrieve a single businesses
    if int(businessId) in known_business_ids:
        specific_business = Business.get_business_by_id(int(businessId))
        information = {
            "user_id": specific_business[0],
            "name": specific_business[1],
            "location": specific_business[2],
            "category": specific_business[3],
            "description": specific_business[4]
        }
        if information:
            return jsonify(information), 200
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
