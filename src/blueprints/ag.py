from flask import Blueprint, request, jsonify, g, redirect, render_template, url_for
from models.user import User, Session
from app import db

bp = Blueprint("ag", __name__)


@bp.route("/add", methods=["GET"])
def create_ag():
    if not g.session.authenticated:
        return redirect(url_for("auth.login"))

    return render_template('signup.html')
