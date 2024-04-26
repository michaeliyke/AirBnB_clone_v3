from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns the staus of the api"""
    return jsonify({"status": "OK"})
