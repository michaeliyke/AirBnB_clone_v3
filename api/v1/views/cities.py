#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
@app_views.route('/cities/<string:id>', methods=['GET'], strict_slashes=False)
def cities_rt(id=None):
    """The home route for now - gets some json data"""
    if id:
        ct = storage.get(City, id)
        return jsonify(ct.to_dict()) if ct else jsonify({"error": "Not found"})
    cities = [city.to_dict() for city in storage.all(City).values()]
    return jsonify(cities)
