#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.place import Place


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def places():
    """The home route for now - gets some json data"""
    places = [place.to_dict() for place in storage.all(Place).values()]
    return jsonify(places)
