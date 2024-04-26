#!/usr/bin/python3
from flask import Flask, jsonify
from models import storage
from models.state import State
from os import getenv as env
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


states = [state.to_dict() for state in storage.all(State).values()]


@app.teardown_appcontext
def close_session(response_or_exc):
    """The function to call after each request"""
    storage.close()


@app.route('/', methods=['GET'], strict_slashes=False)
def hello():
    """The home route for now - gets some json data"""
    return jsonify(states)


options = {
    "host": env("HBNB_API_HOST") or '0.0.0.0',
    "port": env("HBNB_API_PORT") or 5000,
    "threaded": True,
    "debug": True,
}

if __name__ == '__main__':
    app.run(**options)
