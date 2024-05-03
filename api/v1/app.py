#!/usr/bin/python3
"""The app module for the API"""

from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv as env
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)
# app.url_map.strict_slashes = False  # Globally set strict_slashes to False
# CORS(app)  # Enable CORS for all routes on the app


@app.errorhandler(404)
def page_not_found(e):
    """Returns a 404 error"""
    return (jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def close_session(response_or_exc):
    """The function to call after each request"""
    storage.close()


@app.route('/', methods=['GET'])
def hello():
    """The home route for now"""
    return (jsonify({'status': 'OK'}), 200)


options = {
    "host": env("HBNB_API_HOST") or '0.0.0.0',
    "port": env("HBNB_API_PORT") or 5000,
    "threaded": True,
    "debug": True,
}

if __name__ == '__main__':
    app.run(**options)
