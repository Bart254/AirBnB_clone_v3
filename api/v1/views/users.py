#!/usr/bin/python3
"""Creates a user view
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_users():
    """Returns JSON represenation of users
    """
    all_users = storage.all(User)
    list_users = []
    for user in all_users.values():
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """Retrieves a user specified by the id
    """
    for user in storage.all(User).values():
        if user.id == user_id:
            return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User specified by the id
    """
    for user in storage.all(User).values():
        if user.id == user_id:
            user.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates a new user with email and password
    """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates the user specified by the id
    """
    for user in storage.all(User).values():
        if user.id == user_id:
            data = request.get_json()
            if not data:
                abort(400, description="Not a JSON")
            for key, value in data.items():
                if key not in ["id", "updated_at", "email", "created_at"]:
                    user.__dict__[key] = value
            return jsonify(user.to_dict()), 200
    abort(404)
