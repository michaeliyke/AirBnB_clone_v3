#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<string:id>', methods=['GET'], strict_slashes=False)
def users(id=None):
    """The home route for now - gets some json data"""
    if id:
        us = storage.get(User, id)
        return jsonify(us.to_dict()) if us else jsonify({"error": "Not found"})
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)
