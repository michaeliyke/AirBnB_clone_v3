#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.place import Place


@app_views.route('/places', methods=['GET'], strict_slashes=False)
@app_views.route('/places/<string:id>', methods=['GET'], strict_slashes=False)
def places(id=None):
    """The home route for now - gets some json data"""
    if id:
        pl = storage.get(Place, id)
        return jsonify(pl.to_dict()) if pl else jsonify({"error": "Not found"})
    places = [place.to_dict() for place in storage.all(Place).values()]
    return jsonify(places)
