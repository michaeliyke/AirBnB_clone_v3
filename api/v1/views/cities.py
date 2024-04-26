#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def cities_rt():
    """The home route for now - gets some json data"""
    cities = [city.to_dict() for city in storage.all(City).values()]
    return jsonify(cities)
