#!/usr/bin/python3
"""The places_reviews module for the API"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


# GET,POST places/<place_id>/reviews
# GET,DELETE,PUT reviews/<review_id>


@app_views.route('/places/<review_id>', methods=['DELETE', 'GET', 'PUT'])
def reviews_id_rt(review_id):
    """Delete, update, or get a review object by id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if request.method == 'GET':  # Retrieve a city object by id
        return (jsonify(review.to_dict()), 200)

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return (jsonify({}), 200)

    # Handle PUT request - typically an update request
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    for ky, value in data.items():
        if ky not in ['id', 'created_at', 'updated_at', 'user_id', 'place_id']:
            setattr(review, ky, value)
    storage.save()
    return (jsonify(review.to_dict()), 200)


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def places_id_reviews_rt(place_id):
    """Retreive all reviews of a place or create a new review object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':  # Retrieve all reviews belonging to a place
        reviews = [review.to_dict() for review in place.reviews]
        return (jsonify(reviews), 200)

    # Handle POST request - typically a create request
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if not data.get('user_id'):
        abort(400, description="Missing user_id")
    if not storage.get(User, data.get('user_id')):
        abort(404)
    if not data.get('text'):
        abort(400, description="Missing text")

    # user_id is already in data
    data['place_id'] = place_id
    review = Review(**data)
    storage.new(review)
    storage.save()
    return (jsonify(review.to_dict()), 201)
