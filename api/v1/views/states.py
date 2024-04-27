#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'])
def states_rt():
    """Returns a list of all states or creates a new state"""
    if request.method == 'GET':  # Retrieve all states
        states = [state.to_dict() for state in storage.all(State).values()]
        return (jsonify(states), 200)

    # Handle POST request - typically a create request
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if not data.get('name'):
        abort(400, description="Missing name")
    state = State(**data)
    storage.new(state)
    storage.save()
    return (jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['DELETE', 'GET', 'PUT'])
def states_id_rt(state_id):
    """Delete, update, or get a state object by id"""
    state = storage.get(State, state_id)
    print("HERE")
    if not state:
        abort(404)

    if request.method == 'GET':  # Retrieve a state object by id
        return (jsonify(state.to_dict()), 200)

    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return (jsonify({}), 200)

    # Handle PUT request - typically an update request
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return (jsonify(state.to_dict()), 200)
