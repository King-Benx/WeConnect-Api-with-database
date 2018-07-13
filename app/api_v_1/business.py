import math
from flask import request, url_for
from flasgger import swag_from
from . import api
from .. import db
from ..models import Business
from .authentication import token_required
from ..functions import make_json_reply, check_validity_of_input


@api.route('/api/v1/businesses', methods=['POST'])
@swag_from('swagger/businesses/create_business.yml')
@token_required
def register_business(current_user):
    """
    register new business into the system basing on name,location,
    category and description sent in json
    """
    data = request.get_json(force=True)

    if not data:
        return make_json_reply(
            'message', 'Cannot create business due to missing fields'), 400

    if (len(data.keys()) != 4):
        return make_json_reply(
            'message', 'Cannot create business due to missing fields'), 400

    user_id = current_user.id
    name = data['name']
    location = data['location']
    category = data['category']
    description = data['description']

    if check_validity_of_input(
            name=name,
            location=location,
            category=category,
            description=description) == False:
        return make_json_reply('message', 'Fields cannot be empty'), 400

    business = Business(
        user_id=user_id,
        name=name,
        location=location,
        category=category,
        description=description)

    db.session.add(business)

    return make_json_reply(
        'message',
        'Business ' + str(business.name) + ' successfully created'), 201


@api.route('/api/v1/businesses/<int:businessId>', methods=['PUT'])
@swag_from('swagger/businesses/update_business.yml')
@token_required
def update_business(current_user, businessId):
    """
    update an authenticated user's business
    """
    business = Business.query.get(int(businessId))

    if not business:
        return make_json_reply('message', 'Business id does not exist'), 404

    if business.user_id != current_user.id:
        return make_json_reply('message', 'Cannot update business'), 400

    data = request.get_json(force=True)
    name = location = category = description = None

    if 'name' in data.keys():
        name = data['name']

    if 'location' in data.keys():
        location = data['location']

    if 'category' in data.keys():
        category = data['category']

    if 'description' in data.keys():
        description = data['description']

    if check_validity_of_input(name=name):
        business.name = name

    if check_validity_of_input(location=location):
        business.location = location

    if check_validity_of_input(category=category):
        business.category = category

    if check_validity_of_input(description=description):
        business.description = description

    db.session.add(business)

    return make_json_reply(
        'message', 'Successfully updated business ' + business.name), 200


@api.route('/api/v1/businesses/<int:businessId>', methods=['DELETE'])
@swag_from('swagger/businesses/delete_business_by_id.yml')
@token_required
def delete_business(current_user, businessId):
    """
    authenticated user deletes a business created by them basing on the 
    business's id
    """
    business = Business.query.get(int(businessId))

    if not (business and business.user_id == current_user.id):
        return make_json_reply(
            'message',
            'Business id might not exist or you have no right to delete business'
        ), 404

    business_name = business.name
    db.session.delete(business)

    return make_json_reply(
        'message', 'Successfully deleted business ' + str(business_name)), 200


@api.route('/api/v1/businesses', methods=['GET'])
@swag_from('swagger/businesses/retrieve_all_businesses.yml')
@token_required
def get_all_businesses(current_user):
    """
    retrieve all businesses
    """

    if Business.query.count() == 0:
        return make_json_reply('message',
                               'No businesses registered currently'), 404

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', Business.query.count(), type=int)
    pagination = Business.query.paginate(page, per_page=limit, error_out=False)
    businesses = pagination.items
    prev = None

    if pagination.has_prev:
        prev = url_for('api.get_all_businesses', page=page - 1, _external=True)
    next = None

    if pagination.has_next:
        next = url_for('api.get_all_businesses', page=page + 1, _external=True)

    return make_json_reply(
        'results', {
            'businesses': [business.to_json() for business in businesses],
            'prev': prev,
            'next': next,
            'records': math.ceil(Business.query.count() / 5)
        }), 200


@api.route('/api/v1/owned_businesses', methods=['GET'])
@token_required
def get_owned_businesses(current_user):
    """
    retrieve all businesses
    """

    if Business.query.filter_by(user_id=current_user.id).count() == 0:
        return make_json_reply('message',
                               'No businesses registered currently'), 404

    page = request.args.get('page', 1, type=int)
    limit = request.args.get(
        'limit',
        Business.query.filter_by(user_id=current_user.id).count(),
        type=int)
    pagination = Business.query.filter_by(user_id=current_user.id).paginate(
        page, per_page=limit, error_out=False)
    businesses = pagination.items
    prev = None

    if pagination.has_prev:
        prev = url_for(
            'api.get_owned_businesses', page=page - 1, _external=True)
    next = None

    if pagination.has_next:
        next = url_for(
            'api.get_owned_businesses', page=page + 1, _external=True)

    return make_json_reply(
        'results', {
            'businesses': [business.to_json() for business in businesses],
            'prev': prev,
            'next': next,
            'records': math.ceil(Business.query.filter_by(user_id=current_user.id).count() / 5)

        }), 200


@api.route('/api/v1/businesses/<int:businessId>', methods=['GET'])
@swag_from('swagger/businesses/retrieve_business_by_id.yml')
@token_required
def get_a_business(current_user, businessId):
    """
    retrieve an existant single business
    """
    business = Business.query.get(int(businessId))

    if not business:
        return make_json_reply(
            'message', 'No businesses registered with that id currently'), 404

    return make_json_reply('business_info', business.to_json()), 200


@api.route('/api/v1/businesses/search', methods=['GET'])
@swag_from('swagger/businesses/search_business.yml')
@token_required
def get_a_business_by_name(current_user):
    """
    search for a business by name using the q parameter
    """
    business_name = str(request.args.get('q'))
    filter_type = str(request.args.get('filter_type'))
    filter_value = str(request.args.get('filter_value'))

    results = Business.query.filter(
        Business.name.ilike('%' + business_name + '%'))

    # filter by either category or location
    if filter_type and filter_value:
        if filter_type == 'category':
            results = Business.query.filter(
                Business.category.ilike('%'+filter_value+'%')).filter(
                    Business.name.ilike('%' + business_name + '%'))

        if filter_type == 'location':
            results = Business.query.filter(
                Business.location.ilike('%' + filter_value + '%')).filter(
                Business.name.ilike('%' + business_name + '%'))

    # paginate results
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', results.count(), type=int)

    pagination = results.paginate(page, per_page=limit, error_out=False)
    search_results = pagination.items
    prev = None

    if pagination.has_prev:
        prev = url_for(
            'api.get_a_business_by_name', page=page - 1, _external=True)
    next = None

    if pagination.has_next:
        next = url_for(
            'api.get_a_business_by_name', page=page + 1, _external=True)

    if not search_results:
        return make_json_reply(
            'message', 'No businesses registered called ' + business_name), 404

    return make_json_reply(
        'results', {
            'searched_businesses':
            [business.to_json() for business in search_results],
            'prev':
            prev,
            'next':
            next,
            'records': math.ceil(results.count() / 5)
        }), 200


@api.route('/api/v1/businesses/filter', methods=['GET'])
@swag_from('swagger/businesses/filter_business.yml')
@token_required
def filter_business(current_user):
    """
    filter business by either location or category
    """
    filter_type = str(request.args.get('filter_type'))
    filter_value = str(request.args.get('filter_value'))

    if filter_type == 'category':
        results = Business.query.filter_by(category=filter_value)
    elif filter_type == 'location':
        results = Business.query.filter_by(location=filter_value)
    else:
        return make_json_reply('message', 'Invalid filter type'), 400

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

    if not filter_results:
        return make_json_reply(
            'message', 'No businesses registered with filter type ' +
            str(filter_type) + ' = ' + str(filter_value)), 404

    return make_json_reply(
        'results', {
            'filtered_businesses':
            [business.to_json() for business in filter_results],
            'prev':
            prev,
            'next':
            next
        }), 200
