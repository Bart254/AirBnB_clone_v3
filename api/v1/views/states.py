#!/usr/bin/python3
""" Creates a new state view
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def all_states():
    """Returns a list of all states
    """
    all_states = storage.all("State")
    states_list = []
    for state in all_states.values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Returns a state object based on the id
    """
    for state_obj in storage.all(State).values():
        if state_id == state_obj.id:
            return jsonify(state_obj.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object."""
    all_states = storage.all("State")
    for state in all_states.values():
        if state.id == state_id:
            state.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State."""
    data = request.get_json()

    if not data:
        abort(400, description="Not a JSON")

    if 'name' not in data:
        abort(400, description="Missing name")

    new_state = State(**data)
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates an available state object
    """
    all_states = storage.all(State)
    my_state_obj = None
    for state in all_states.values():
        if state.id == state_id:
            my_state_obj = state
            break
    if not my_state_obj:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            my_state_obj.__dict__[key] = value
    my_state_obj.save()
    return jsonify(my_state_obj.to_dict()), 201
