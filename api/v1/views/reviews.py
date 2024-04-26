#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.review import Review


@app_views.route('/reviews', methods=['GET'], strict_slashes=False)
def reviews():
    """The home route for now - gets some json data"""
    reviews = [review.to_dict() for review in storage.all(Review).values()]
    return jsonify(reviews)
