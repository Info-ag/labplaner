from flask import Blueprint, request, jsonify, g, redirect, render_template, abort
from models.user import User, Session
from app import db

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET"])
def login_get():
    if g.session.authenticated:
        return redirect("/")

    return render_template('login.html', warning='')


@bp.route("/login", methods=["POST"])
def login():
    if g.session.authenticated:
        return redirect("/")
    user = User.query.filter_by(email=request.values["email"]).one()
    if user and user.check_password(request.values["password"]):
        g.session.revoked = True
        db.session.merge(g.session)
        db.session.commit()

        _session = Session(user)
        db.session.add(_session)
        db.session.commit()
        g.session = _session
        return redirect("/")

    return jsonify({"Status": "Failed"})


@bp.route("/logout")
def logout():
    if g.session.authenticated:
        g.session.revoked = True
        db.session.merge(g.session)
        db.session.commit()

        _session = Session()
        db.session.add(_session)
        db.session.commit()
        g.session = _session

    return redirect("/")
