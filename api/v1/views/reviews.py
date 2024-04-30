#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.review import Review


@app_views.route('/reviews', methods=['GET'], strict_slashes=False)
@app_views.route('/reviews/<string:id>', methods=['GET'], strict_slashes=False)
def reviews(id=None):
    """The home route for now - gets some json data"""
    if id:
        rv = storage.get(Review, id)
        return jsonify(rv.to_dict()) if rv else jsonify({"error": "Not found"})
    reviews = [review.to_dict() for review in storage.all(Review).values()]
    return jsonify(reviews)

