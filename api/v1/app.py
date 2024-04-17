#!/usr/bin/python3
""" API Version 1
"""
from api.v1.views import app_views
from flask_cors import CORS
from flask import Flask, jsonify
import os
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(exception):
    """Closes the storage on teardown."""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors and returns a JSON-formatted 404 response."""
    error_response = {
                      "error": "Not found"
                      }
    return jsonify(error_response), 404


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True, debug=True)
