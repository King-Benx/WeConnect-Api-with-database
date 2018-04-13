from flask import request, url_for
from flasgger import swag_from
from . import api
from .. import db
from ..models import Business, User
from .authentication import token_required
from ..functions import make_json_reply


@api.route('/api/v1/businesses', methods=['POST'])
@swag_from('swagger/businesses/create_business.yml')
@token_required
def register_business(current_user):
    """register new business into the system basing on name,location,category and description sent in json"""
    data = request.get_json(force=True)
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
                return make_json_reply('Business ' + str(business.name) +
                                       ' successfully created'), 201
            else:
                return make_json_reply(
                    'Cannot create business due to missing fields'), 400
    else:
        return make_json_reply(
            'Cannot create business due to missing fields'), 400


@api.route('/api/v1/businesses/<int:businessId>', methods=['PUT'])
@swag_from('swagger/businesses/update_business.yml')
@token_required
def update_business(current_user, businessId):
    """update an authenticated user's business"""
    check_business_by_id = Business.query.get(int(businessId))
    if check_business_by_id:
        data = request.get_json(force=True)
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
            return make_json_reply('Successfully updated business ' +
                                   check_business_by_id.name), 200
        else:
            return make_json_reply('Cannot update business'), 400
    else:
        return make_json_reply('Business id does not exist'), 404


@api.route('/api/v1/businesses/<int:businessId>', methods=['DELETE'])
@swag_from('swagger/businesses/delete_business_by_id.yml')
@token_required
def delete_business(current_user, businessId):
    """authenticated user deletes a business created by them basing on the business's id"""
    check_business_by_id = Business.query.get(int(businessId))
    if check_business_by_id and check_business_by_id.user_id == current_user.id:
        business_name = check_business_by_id.name
        db.session.delete(check_business_by_id)
        return make_json_reply(
            'Successfully deleted business ' + str(business_name)), 200
    else:
        return make_json_reply(
            'Business id might not exist or you have no right to delete business'
        ), 404


@api.route('/api/v1/businesses', methods=['GET'])
@swag_from('swagger/businesses/retrieve_all_businesses.yml')
@token_required
def retrieve_all_businesses(current_user):
    """retrieve all businesses"""
    if Business.query.count() > 0:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', Business.query.count(), type=int)
        pagination = Business.query.paginate(
            page, per_page=limit, error_out=False)
        businesses = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for(
                'api.retrieve_all_businesses', page=page - 1, _external=True)
        next = None
        if pagination.has_next:
            next = url_for(
                'api.retrieve_all_businesses', page=page + 1, _external=True)
        return make_json_reply({
            'Businesses ': [business.to_json() for business in businesses],
            'prev':
            prev,
            'next':
            next
        }), 200
    else:
        return make_json_reply(
            'No businesses registered currently, register one at ' +
            str(url_for('api.register_business', _external=True))), 404


@api.route('/api/v1/businesses/<int:businessId>', methods=['GET'])
@swag_from('swagger/businesses/retrieve_business_by_id.yml')
@token_required
def retrieve_a_business(current_user, businessId):
    """retrieve an existant single business"""
    if Business.query.get(int(businessId)):
        specific_business = Business.query.get_or_404(int(businessId))
        if specific_business:
            return make_json_reply(specific_business.to_json()), 200
        else:
            return make_json_reply(
                'No businesses registered with that id currently, view all businesses at '
                + str(url_for('api.retrieve_all_businesses', _external=True))
            ), 400
    else:
        return make_json_reply(
            'No businesses registered with that id currently, view all businesses at '
            + str(url_for('api.retrieve_all_businesses', _external=True))), 404


@api.route('/api/v1/businesses/search', methods=['GET'])
@swag_from('swagger/businesses/search_business.yml')
@token_required
def retrieve_a_business_by_name(current_user):
    """search for a business by name using the q parameter"""
    business_name = str(request.args.get('q'))
    filter_type = str(request.args.get('filter_type'))
    filter_value = str(request.args.get('filter_value'))
    results = Business.query.filter_by(name=business_name)
    if filter_type and filter_value:
        if filter_type == 'category':
            results = Business.query.filter_by(
                name=business_name, category=filter_value)
        if filter_type == 'location':
            results = Business.query.filter_by(
                name=business_name, location=filter_value)

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', results.count(), type=int)
    pagination = results.paginate(page, per_page=limit, error_out=False)
    search_results = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for(
            'api.retrieve_a_business_by_name', page=page - 1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for(
            'api.retrieve_a_business_by_name', page=page + 1, _external=True)
    if search_results:
        return make_json_reply({
            'Searched Business Results ':
            [business.to_json() for business in search_results],
            'prev':
            prev,
            'next':
            next
        }), 200
    else:
        return make_json_reply(
            'No businesses registered called ' + business_name), 404


@api.route('/api/v1/businesses/filter', methods=['GET'])
@swag_from('swagger/businesses/filter_business.yml')
@token_required
def filter_business(current_user):
    """filter business by either location or category"""
    filter_type = str(request.args.get('filter_type'))
    filter_value = str(request.args.get('filter_value'))
    if filter_type == 'category':
        results = Business.query.filter_by(category=filter_value)
    elif filter_type == 'location':
        results = Business.query.filter_by(location=filter_value)
    else:
        return make_json_reply('Invalid filter type'), 400
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', results.count(), type=int)
    pagination = results.paginate(page, per_page=limit, error_out=False)
    filter_results = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.filter_business', page=page - 1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.filter_business', page=page + 1, _external=True)
    if filter_results:
        return make_json_reply({
            'Business Results ':
            [business.to_json() for business in filter_results],
            'prev':
            prev,
            'next':
            next
        }), 200
    else:
        return make_json_reply(
            'No businesses registered with filter type ' + str(filter_type) +
            ' = ' + str(filter_value)), 404
