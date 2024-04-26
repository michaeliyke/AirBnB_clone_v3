#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """The home route for now - gets some json data"""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)
