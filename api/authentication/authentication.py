from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, set_access_cookies, unset_access_cookies
from werkzeug.security import generate_password_hash, check_password_hash

from api.models.users import User

from api.redis_db import rds

from .utils import *

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return jsonify({"msg": "provided data is not json"}), 400

    data: dict = request.json

    if not all([_key in data.keys() for _key in ["username", "email", "password"]]):
        return jsonify({"msg": "missing data"}), 400

    username = data["username"]
    email = data["email"]
    password = data["password"]

    if not check_password(password):
        return jsonify({"msg": "password is not strong enough"}), 400

    if not check_email(email):
        return jsonify({"msg": "email is not valid"}), 400

    secret_digits = send_validation_email(email, username)

    password = generate_password_hash(password)
    user = User.create(username, email, password)

    rds.setex(name=f"user_validation:{user.id}", time=(5 * 60), value=secret_digits)

    return jsonify({"msg": "user has been created successful", "user_id": str(user.id)}), 200


@auth.route("/register/validate", methods=["POST"])
def register_validate():
    if not request.is_json:
        return jsonify({"msg": "provided data is not json"}), 400

    data = request.json

    if not all([_key in data for _key in ["user_id", "validation_code"]]):
        return jsonify({"msg": "missing data"}), 400

    validation_code_rds = rds.get(name=f"user_validation:{data['user_id']}")

    if validation_code_rds is None or not data["validation_code"] == validation_code_rds:
        return jsonify({"msg": "wrong code"}), 400

    user = User.query.get(int(data["user_id"]))
    user.activated = True

    response = jsonify({"msg": "registration successful"})

    access_token = create_access_token(identity=user)
    set_access_cookies(response=response, encoded_access_token=access_token)

    return response, 201


@auth.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"msg": "provided data is not json"}), 400

    data = request.json

    if not all([_key in data.keys() for _key in ["email", "password"]]):
        return jsonify({"msg": "missing data"}), 400

    user = User.query.filter_by(email=data["email"]).one_or_none()

    if user is None:
        return jsonify({"msg": "user not found"}), 404

    if not check_password_hash(user.password, data["password"]):
        return jsonify({"msg": "wrong credentials"}), 400

    if not user.activated:
        return jsonify({"msg": "user not activated"}), 404

    response = jsonify({"msg": "login successful"})

    access_token = create_access_token(identity=user)
    set_access_cookies(response=response, encoded_access_token=access_token)

    return response, 200


@auth.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_access_cookies(response)
    return response, 200
