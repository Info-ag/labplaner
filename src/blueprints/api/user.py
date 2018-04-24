from flask import Blueprint, request, jsonify
from models.user import User, UserSchema
from app import db

bp = Blueprint("user_api", __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@bp.route("/", methods=["POST"])
def add_user():
    try:
        user = User()
        user.username = request.values["username"]
        user.email = request.values["email"]
        user.set_password(request.values["password"])

        db.session.add(user)
        db.session.commit()

        return user_schema.jsonify(user), 200
    except:
        return jsonify({"Status": "Failed"}), 500


@bp.route("/<uid>", methods=["GET"])
def get_user_by_id(uid):
    user = User.query.get(uid)
    return user_schema.jsonify(user)


@bp.route("/", methods=["GET"])
def get_all_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)
