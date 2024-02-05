#!/usr/bin/python3
"""Defines api indices"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns a JSON response with status OK."""
    response = {
                 "status": "OK"
               }
    return jsonify(response)


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Returns JSON response of the number objects in the database
    """
    nb_of_objs = {
                  "amenities": storage.count('Amenity'),
                  "cities": storage.count('City'),
                  "places": storage.count('Place'),
                  "reviews": storage.count('Review'),
                  "states": storage.count('State'),
                  "users": storage.count('User')
                  }
    return jsonify(nb_of_objs)
