#!/usr/bin/python3
"""The index module for the API"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

objs = {
    "amenities": storage.count(Amenity),
    "cities": storage.count(City),
    "places": storage.count(Place),
    "reviews": storage.count(Review),
    "states": storage.count(State),
    "users": storage.count(User),
}


@app_views.route('/status', methods=['GET'])
def status():
    """Returns the staus of the api"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """Returns the staus of the api"""
    return jsonify(objs)
