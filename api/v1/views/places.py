#!/usr/bin/python3
"""Creates a place view
"""
from api.v1.views import app_views
from models.city import City
from flask import abort, jsonify, request
from models.place import Place
from models import storage
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """Returns JSON represenation of places in a city
    """
    all_places = storage.all(Place)
    list_places = []
    for place in all_places.values():
        if place.city_id == city_id:
            list_places.append(place.to_dict())
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place_by_id(place_id):
    """Retrieves a place specified by the id
    """
    for place in storage.all(Place).values():
        if place.id == place_id:
            return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place specified by the id
    """
    for place in storage.all(Place).values():
        if place.id == place_id:
            place.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a new place with email and password
    """
    found_city = False
    found_user = False
    for city in storage.all(City).values():
        if city.id == city_id:
            found_city = True
    if not found_city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    for user in storage.all(User).values():
        if user.id == data["user_id"]:
            found_user = True
    if not found_user:
        abort(404)
    if 'name' not in data:
        abort(400, description="Missing name")
    data["city_id"] = city_id
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates the place specified by the id
    """
    for place in storage.all(Place).values():
        if place.id == place_id:
            data = request.get_json()
            if not data:
                abort(400, description="Not a JSON")
            for key, value in data.items():
                if key not in ["id", "updated_at", "user_id", "city_id",
                               "created_at"]:
                    place.__dict__[key] = value
            return jsonify(place.to_dict()), 200
    abort(404)
