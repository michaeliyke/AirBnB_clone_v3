#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<id>', methods=['GET'], strict_slashes=False)
def amenities_rt(id=None):
    """The home route for now - gets some json data"""
    if id:
        am = storage.get(Amenity, id)
        return jsonify(am.to_dict()) if am else jsonify({"error": "Not found"})
    amenities = [am.to_dict() for am in storage.all(Amenity).values()]
    return jsonify(amenities)
