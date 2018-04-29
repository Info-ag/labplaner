from flask import Blueprint, g, redirect, render_template, url_for, flash
from sqlalchemy.sql import exists
from werkzeug.exceptions import NotFound, Unauthorized
from models.associations import UserAG
from models.ag import AG, AGSchema
from app import db

bp = Blueprint("ag", __name__)

ag_schema = AGSchema()
ags_schema = AGSchema(many=True)



@bp.route("/add", methods=["GET"])
def create_ag():
    if not g.session.authenticated:
        flash(u'You need to be logged in', 'error')
        return redirect(url_for("auth.login"))

    return render_template('ag/add.html', title="Create AG")


@bp.route("/<ag_name>", methods=["GET"])
def ag_dashboard(ag_name):
    if not g.session.authenticated:
        return Unauthorized()

    if db.session.query(exists().where(AG.name == ag_name)).scalar():
        ag: AG = AG.query.filter_by(name=ag_name).scalar()
        if db.session.query(exists().where(UserAG.user_id == g.session.uid and UserAG.ag_id == ag.id)).scalar():
            user_ag = UserAG.query.filter_by(uid=g.session.uid, ag_id=ag.id).scalar()
            if user_ag.role != "NONE":
                schema = AGSchema()
                schema.context = {"ag_id": ag.id}
                return render_template('ag/dashboard.html', my_role="user_ag.role", ag=schema.dump(ag), title=ag.display_name)

        return Unauthorized()

    else:
        return NotFound()


@bp.route("/<ag_name>/invite", methods=["GET"])
def invite_ag(ag_name):
    if not g.session.authenticated:
        return Unauthorized()

    if db.session.query(exists().where(AG.name == ag_name)).scalar():
        ag: AG = AG.query.filter_by(name=ag_name).scalar()
        if db.session.query(exists().where(UserAG.user_id == g.session.uid and UserAG.ag_id == ag.id)).scalar():
            user_ag = UserAG.query.filter_by(uid=g.session.uid, ag_id=ag.id).scalar()
            if user_ag.role == "MENTOR":
                return render_template('ag/invite.html', ag=ag_schema.dump(ag), title=f"Invite {ag.display_name}")

        return Unauthorized()

    else:
        return NotFound()


# Events

@bp.route("/<ag_name>/event/add", methods=["GET"])
def create_event(ag_name):
    if not g.session.authenticated:
        return Unauthorized()

    if db.session.query(exists().where(AG.name == ag_name)).scalar():
        ag: AG = AG.query.filter_by(name=ag_name).scalar()
        if db.session.query(exists().where(UserAG.user_id == g.session.uid and UserAG.ag_id == ag.id)).scalar():
            user_ag = UserAG.query.filter_by(uid=g.session.uid, ag_id=ag.id).scalar()
            if user_ag.role == "MENTOR":
                return render_template('ag/event/add.html', ag=ag_schema.dump(ag), title=f"New Event {ag.display_name}")

        return Unauthorized()

    return NotFound()
