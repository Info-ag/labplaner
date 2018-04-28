from flask import Blueprint, request, jsonify, g, redirect, render_template, url_for
from sqlalchemy.sql import exists
from models.user import User, Session
from models.associations import UserAG
from models.ag import AG
from app import db

bp = Blueprint("ag", __name__)


@bp.route("/add", methods=["GET"])
def create_ag():
    if not g.session.authenticated:
        return redirect(url_for("auth.login"))

    return render_template('ag/add.html')


@bp.route("/<ag>", methods=["GET"])
def ag_dashboard(ag):
    if not g.session.authenticated:
        return redirect(url_for("auth.login"))

    #if db.session.query(exists().where(AG.name == ag)).scalar():


    # userag = UserAG.query.filter(UserAG.uid == g.session.uid).scalar()

    return render_template('ag/dashboard.html')


@bp.route("/<ag>/invite", methods=["GET"])
def invite_ag(ag):
    if not g.session.authenticated:
        return redirect(url_for("auth.login"))

    return render_template('ag/invite.html')
