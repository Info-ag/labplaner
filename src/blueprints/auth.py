from flask import Blueprint, request, jsonify, g, redirect, render_template, abort, Response
from models.user import User, Session
from app import db

bp = Blueprint("auth", __name__)


@bp.route("/signup", methods=["GET"])
def signup_get():
    if g.session.authenticated:
        return redirect("/")

    return render_template('signup.html', warning='')


@bp.route("/login", methods=["GET"])
def login_get():
    if g.session.authenticated:
        return redirect("/")

    return render_template('login.html', warning='')


@bp.route("/login", methods=["POST"])
def login():
    if g.session.authenticated:
        return jsonify({"redirect": "/"}), 200

    try:
        email = request.values["email"]
        if "@" in email:
            user = User.query.filter_by(email=email).one()
        else:
            user = User.query.filter_by(username=email).one()

        if user and user.check_password(request.values.get("password")):
            g.session.revoked = True
            db.session.merge(g.session)
            db.session.commit()

            _session = Session(user)
            db.session.add(_session)
            db.session.commit()
            g.session = _session
            return jsonify({"redirect": "/"}), 200
        return jsonify({"Status": "Failed", "reason": "password"}), 406
    except:
        return jsonify({"Status": "Failed", "reason": "email"}), 406


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
