#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State


@app_views.route('/cities/<city_id>', methods=['DELETE', 'GET', 'PUT'])
def cities_id_rt(city_id):
    """Delete, update, or get a city object by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':  # Retrieve a state object by id
        return (jsonify(city.to_dict()), 200)

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return (jsonify({}), 200)

    # Handle PUT request - typically an update request
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return (jsonify(city.to_dict()), 200)


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def states_id_cities_rt(state_id):
    """Retreieve or create a city object in a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if request.method == 'GET':  # Retrieve all the cities belonging to a state
        cities = [city.to_dict() for city in state.cities]
        return (jsonify(cities), 200)

    # Handle POST request - typically a create request
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if not data.get('name'):
        abort(400, description="Missing name")
    data['state_id'] = state_id
    city = City(**data)
    storage.new(city)
    storage.save()
    return (jsonify(city.to_dict()), 201)

