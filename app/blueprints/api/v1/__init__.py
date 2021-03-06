"""
Basic blueprint route for the api v1

This blueprint provides necessary routes for the
API documentation.
"""

from flask import Blueprint, request, jsonify, render_template
from app.models.user import User, UserSchema


bp = Blueprint('api', __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@bp.route('/', methods=['GET'])
def index():
    return render_template('api/v1/index.html', title='API v1')
