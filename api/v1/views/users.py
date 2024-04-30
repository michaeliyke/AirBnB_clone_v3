#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User

# GET,POST /users
# DELETE,GET,PUT /users/<user_id>


@app_views.route('/users', methods=['GET', 'POST'])
def users_rt():
    """Returns a list of all users or creates a new user"""
    if request.method == 'GET':  # Retrieve all users
        users = [user.to_dict() for user in storage.all(User).values()]
        return (jsonify(users), 200)

    # Handle POST request - typically a create request
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if not data.get('email'):
        abort(400, description="Missing email")
    if not data.get('password'):
        abort(400, description="Missing password")

    user = User(**data)
    storage.new(user)
    storage.save()
    return (jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['DELETE', 'GET', 'PUT'])
def users_id_rt(user_id):
    """Delete, update, or get a user object by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if request.method == 'GET':  # Retrieve a user object by id
        return (jsonify(user.to_dict()), 200)

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return (jsonify({}), 200)

    # Handle PUT request - typically an update request
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, key, value)
    storage.save()
    return (jsonify(user.to_dict()), 200)

