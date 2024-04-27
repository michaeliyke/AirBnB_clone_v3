#!/usr/bin/python3
from flask import Flask, jsonify
from os import getenv as env
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False  # Globally set strict_slashes to False
app.register_blueprint(app_views)


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
