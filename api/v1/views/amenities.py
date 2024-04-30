#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity

# GET,POST /amenities
# GET,DELETE,PUT amenities/<amenity_id>


@app_views.route('/amenities', methods=['GET', 'POST'])
def amenities_rt():
    """Returns a list of all amenities or creates a new amenity"""
    if request.method == 'GET':  # Retrieve all amenities
        amenities = [amenity.to_dict()
                     for amenity in storage.all(Amenity).values()]
        return (jsonify(amenities), 200)

    # Handle POST request - typically a create request
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if not data.get('name'):
        abort(400, description="Missing name")
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()
    return (jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE', 'GET', 'PUT'])
def amenities_id_rt(amenity_id):
    """Delete, update, or get a amenity object by id"""
    amenity = storage.get(Amenity, amenity_id)
    # TODO: FIX THIS LATER
    print(amenity, amenity_id)
    if not amenity:
        abort(404)

    if request.method == 'GET':  # Retrieve a amenity object by id
        return (jsonify(amenity.to_dict()), 200)

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return (jsonify({}), 200)

    # Handle PUT request - typically an update request
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return (jsonify(amenity.to_dict()), 200)

