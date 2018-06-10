from flask import Blueprint, request, jsonify, render_template
from src.models.user import User, UserSchema
from src.main import db

bp = Blueprint("api", __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@bp.route("/", methods=["GET"])
def index():
    return render_template("api/v1/index.html", title="API v1")
