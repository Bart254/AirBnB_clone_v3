#!/usr/bin/python3
""" Creates a new state view
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
from models.state import State
from models import storage


@app_views.route("/states/<state_id>/cities", methods=['GET'])
def all_cities(state_id):
    """Returns a list of all cities of a state
    """
    all_states = storage.all(State)
    all_cities = storage.all(City)
    city_list = []
    found = False
    for state in all_states.values():
        if state.id == state_id:
            found = True
    if not found:
        abort(404)
    for city in all_cities.values():
        if city.state_id == state_id:
            city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Returns a city object based on the id
    """
    for city_obj in storage.all(City).values():
        if city_obj.id == city_id:
            return jsonify(city_obj.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object."""
    all_cities = storage.all(City)
    for city in all_cities.values():
        if city.id == city_id:
            city.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Creates a new City."""
    all_states = storage.all(State)
    found_state = False
    for state in all_states.values():
        if state.id == state_id:
            found_state = True
    if not found_state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates an available city object
    """
    all_cities = storage.all(City)
    my_city_obj = None
    for city in all_cities.values():
        if city.id == city_id:
            my_city_obj = city
            break
    if not my_city_obj:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            my_city_obj.__dict__[key] = value
    my_city_obj.save()
    return jsonify(my_city_obj.to_dict()), 201
