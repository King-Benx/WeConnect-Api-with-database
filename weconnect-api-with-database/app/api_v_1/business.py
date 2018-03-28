from flask import request, url_for, session, jsonify
from . import api
from .. import db
from ..models import Business, User
from .authentication import token_required
from ..functions import make_json_reply


@api.route('/api/v1/businesses', methods=['POST'])
@token_required
def register_business(current_user):
    """register new business into the system basing on name,location,category and description sent in json"""
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
    """update an authenticated user's business"""
    check_business_by_id = Business.query.get(int(businessId))
    if check_business_by_id:
        data = request.get_json()
        if 'name' in data.keys():
            name = data['name']
        else:
            name = None
        if 'location' in data.keys():
            location = data['location']
        else:
            location = None
        if 'category' in data.keys():
            category = data['category']
        else:
            category = None
        if 'description' in data.keys():
            description = data['description']
        else:
            description = None
        if check_business_by_id.user_id == current_user.id:
            if name != '' and name != check_business_by_id.name and name is not None:
                check_business_by_id.name = name
            if location != '' and location != check_business_by_id.location and location is not None:
                check_business_by_id.location = location
            if category != '' and category != check_business_by_id.category and category is not None:
                check_business_by_id.category = category
            if description != '' and description != check_business_by_id.description and description is not None:
                check_business_by_id.description = description
            db.session.add(check_business_by_id)
            if check_business_by_id:
                return make_json_reply('message',
                                       'successfully updated business ' +
                                       check_business_by_id.name), 201
            else:
                return make_json_reply(
                    'message',
                    'Failure updating ' + check_business_by_id.name), 400
    else:
        return make_json_reply('message', 'Business id does not exist'), 400


@api.route('/api/v1/businesses/<businessId>', methods=['DELETE'])
@token_required
def delete_business(current_user, businessId):
    """authenticated user deletes a business created by them basing on the business's id"""
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
    """retrieve all businesses"""
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
    """retrieve an existant single business"""
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


# @api.route('/api/v1/businesses?q=<name>', methods=['GET'])
# @token_required
# def retrieve_a_business_by_name(current_user, q):
#     """search for a business by name using the q parameter"""
    
#     print(q)
#     # if Business.query.filter_by(name=name).count() > 0:
#     #     businesses = Business.query.filter_by(name=name)
#     #     return jsonify('Businesses ',
#     #                    [business.to_json() for business in businesses]), 200
#     # else:
#     #     return make_json_reply(
#     #         'Results',
#     #         'No businesses with that name registered currently!'), 404


# @api.route(
#     '/api/v1/businesses?<filter>=<filter_value>', methods=['GET'])
# @token_required
# def retrieve_all_businesses_by_filter(current_user, filter, filter_value):
#     """Filter businesses basing on category"""
#     if filter == 'category':
#         if Business.query.filter_by(category=filter_value).count() > 0:
#             businesses = Business.query.filter_by(category=filter_value)
#             return jsonify('Businesses ',
#                            [business.to_json()
#                             for business in businesses]), 200
#         else:
#             return make_json_reply(
#                 'Results',
#                 'No businesses registered under category ' + filter_value), 404
#     elif filter == 'location':
#         if Business.query.filter_by(location=filter_value).count() > 0:
#             businesses = Business.query.filter_by(location=filter_value)
#             return jsonify('Businesses ',
#                            [business.to_json()
#                             for business in businesses]), 200
#         else:
#             return make_json_reply(
#                 'Results',
#                 'No businesses registered located in ' + filter_value), 404
#     else:
#         return make_json_reply('Error', 'Unknown filter ' + filter), 400
