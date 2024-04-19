#!/usr/bin/python3
""" Creates a new Review view
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.review import Review
from models.place import Place
from models import storage
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=['GET'])
def all_reviews(place_id):
    """Returns a list of all reviews of a place
    """
    all_places = storage.all(Place)
    all_reviews = storage.all(Review)
    review_list = []
    found = False
    for place in all_places.values():
        if place.id == place_id:
            found = True
    if not found:
        abort(404)
    for review in all_reviews.values():
        if review.place_id == place_id:
            review_list.append(review.to_dict())
    return jsonify(review_list)


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Returns a review object based on the id
    """
    for review in storage.all(Review).values():
        if review.id == review_id:
            return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Review object."""
    all_reviews = storage.all(Review)
    for review in all_reviews.values():
        if review.id == review_id:
            review.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Creates a new Review."""
    all_places = storage.all(Place)
    found_place = False
    found_user = False
    for place in all_places.values():
        if place.id == place_id:
            found_place = True
    if not found_place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    for user in storage.all(User).values():
        if user.id == data["user_id"]:
            found_user = True
            break
    if not found_user:
        abort(404)
    data["place_id"] = place_id
    new_review = Review(**data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Updates an available review object
    """
    all_reviews = storage.all(Review)
    my_review_obj = None
    for review in all_reviews.values():
        if review.id == review_id:
            my_review_obj = review
            break
    if not my_review_obj:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at", "user_id",
                       "place_id"]:
            my_review_obj.__dict__[key] = value
    my_review_obj.save()
    return jsonify(my_review_obj.to_dict()), 201
