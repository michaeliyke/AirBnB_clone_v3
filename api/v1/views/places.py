#!/usr/bin/python3
"""The places module for the API"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User
# GET,DELETE,PUT /places/<place_id>
# POST,GET /cities/<city_id>/places


@app_views.route('/places/<place_id>', methods=['DELETE', 'GET', 'PUT'])
def places_id_rt(place_id):
    """Delete, update, or get a place object by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':  # Retrieve a city object by id
        return (jsonify(place.to_dict()), 200)

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return (jsonify({}), 200)

    # Handle PUT request - typically an update request
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            setattr(place, key, value)
    storage.save()
    return (jsonify(place.to_dict()), 200)


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def cities_id_places_rt(city_id):
    """Retreieve or create a place object in a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':  # Retrieve all the places belonging to a city
        places = [place.to_dict() for place in city.places]
        return (jsonify(places), 200)

    # Handle POST request - typically a create request
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if not data.get('name'):
        abort(400, description="Missing name")
    if not data.get('user_id'):
        abort(400, description="Missing user_id")
    if not storage.get(User, data.get('user_id')):
        abort(404)

    data['city_id'] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return (jsonify(place.to_dict()), 201)
