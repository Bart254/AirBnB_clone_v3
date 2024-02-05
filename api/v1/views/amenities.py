#!/usr/bin/python3
""" Creates a new amenities view
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def all_amenities():
    """Returns a list of all amenities
    """
    all_amenities = storage.all("Amenity")
    amenities_list = []
    for amenity in all_amenities.values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>", methods=['GET'])
def get_amenity(amenity_id):
    """Returns a amenity object based on the id
    """
    for amenity_obj in storage.all(Amenity).values():
        if amenity_obj.id == amenity_id:
            return jsonify(amenity_obj.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes an Amenity object."""
    all_amenities = storage.all("Amenity")
    for amenity in all_amenities.values():
        if amenity.id == amenity_id:
            amenity.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a new Amenity."""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates an available amenity object
    """
    all_amenities = storage.all(Amenity)
    my_amenity_obj = None
    for amenity in all_amenities.values():
        if amenity.id == amenity_id:
            my_amenity_obj = amenity
            break
    if not my_amenity_obj:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            my_amenity_obj.__dict__[key] = value
    my_amenity_obj.save()
    return jsonify(my_amenity_obj.to_dict()), 201
