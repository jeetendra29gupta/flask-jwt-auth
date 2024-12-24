from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

from models import db, User
from utils import hash_password, check_password

auth_bp = Blueprint("auth", __name__)

blacklisted_tokens = set()


@auth_bp.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username:
        return jsonify(message="Username is required"), 400
    if not password:
        return jsonify(message="Password is required"), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify(message="Username already exists"), 400

    hashed_password = hash_password(password)

    new_user = User(username=username, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(message="User created successfully"), 201


@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username:
        return jsonify(message="Username is required"), 400
    if not password:
        return jsonify(message="Password is required"), 400

    existing_user = User.query.filter_by(username=username).first()
    if not existing_user:
        return jsonify(message="Invalid Username"), 401

    is_valid = check_password(existing_user.password, password)
    if not is_valid:
        return jsonify(message="Invalid credentials"), 401

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    return (
        jsonify(
            message="Login successful",
            access_token=access_token,
            refresh_token=refresh_token,
        ),
        200,
    )


@auth_bp.route("/api/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token)


@auth_bp.route("/api/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    blacklisted_tokens.add(jti)
    return jsonify(message="Successfully logged out")


@auth_bp.route("/api/protected", methods=["GET"])
@jwt_required()
def protected():
    jti = get_jwt()["jti"]
    if jti in blacklisted_tokens:
        return jsonify(message="Token has been revoked. Please login again."), 401

    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
