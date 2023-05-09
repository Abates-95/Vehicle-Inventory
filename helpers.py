from functools import wraps
import secrets
from flask import request, jsonify, json
import decimal

from models import User

def token_required(flask_function):
    @wraps(flask_function)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access_token"].split(" ")[1]
        if not token:
            return jsonify({ "message: Token is missing" }), 401


        try:
            current_car_token = User.query.filter_by(token = token).first()
            print(token)
            print(current_car_token)
        except:
            owner = User.query.filter_by(token = token).first

            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify("Message: Token is invalid")
        return flask_function(current_car_token, *args, **kwargs)
    return decorated

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(JSONEncoder, self).default(obj)
