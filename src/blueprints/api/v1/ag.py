from flask import Blueprint, request, jsonify, g
from sqlalchemy.sql import exists
from werkzeug.exceptions import NotFound, Unauthorized
from models.ag import AG, AGSchema
from models.user import User
from models.associations import UserAG
from app import db

bp = Blueprint("ag_api", __name__)

ag_schema = AGSchema()
ags_schema = AGSchema(many=True)


@bp.route("/", methods=["POST"])
def add_ag():
    if not g.session.authenticated:
        return Unauthorized()
    try:
        name = request.values["name"]
        if db.session.query(exists().where(AG.name == name)).scalar():
            return jsonify({"Status": "Failed", "reason": "name"}), 406
        if len(request.values["displayname"]) > 48:
            return jsonify({"Status": "Failed", "reason": "displayname"}), 406
        if len(request.values["description"]) > 140:
            return jsonify({"Status": "Failed", "reason": "description"}), 406

        ag = AG()
        ag.name = name
        ag.display_name = request.values["displayname"]
        ag.description = request.values["description"]

        db.session.add(ag)
        db.session.flush()

        user_ag = UserAG()
        user_ag.uid = g.session.uid
        user_ag.ag_id = ag.id
        user_ag.role = "MENTOR"
        print(ag.id)

        db.session.add(user_ag)
        db.session.commit()

        return jsonify({"redirect": f"/ag/{name}/invite"}), 200
    except:
        return jsonify({"Status": "Failed"}), 406


@bp.route("/id/<aid>", methods=["GET"])
def get_ag_by_id(aid):
    ag = AG.query.get(aid)
    return ag_schema.jsonify(ag)


@bp.route("/name/<name>", methods=["GET"])
def get_ag_by_username(name):
    ag = AG.query.filter_by(name=name).scalar()
    return ag_schema.jsonify(ag)


@bp.route("/<ag_id>/invite", methods=["POST"])
def add_user_to_ag(ag_id):
    if not g.session.authenticated:
        return Unauthorized()

    if db.session.query(exists().where(AG.id == ag_id)).scalar():
        if db.session.query(exists().where(UserAG.uid == g.session.uid and UserAG.ag_id == ag_id)).scalar():
            user_ag = UserAG.query.filter_by(uid=g.session.uid, ag_id=ag_id).scalar()
            if user_ag.role == "MENTOR":
                ag: AG = AG.query.filter_by(id=ag_id).scalar()
                for username in request.values.getlist("users[]"):
                    if db.session.query(exists().where(User.username == username)).scalar():
                        user: User = User.query.filter_by(username=username).scalar()

                        if db.session.query(exists().where(UserAG.uid == user.id and UserAG.ag_id == ag.id)).scalar():
                            continue

                        new_user_ag = UserAG()
                        new_user_ag.role = "PARTICIPANT"
                        new_user_ag.uid = user.id
                        new_user_ag.ag_id = ag.id

                        db.session.add(new_user_ag)
                        db.session.commit()

                return jsonify({"redirect": f"/ag/{ag.name}"}), 200

        return Unauthorized()

    else:
        return NotFound()


@bp.route("/<ag_id>", methods=["GET"])
def add_user_to_ag(ag_id):
    if not g.session.authenticated:
        return Unauthorized()
    try:

        if db.session.query(AG).filter_by(id=ag_id).scalar() is None:
            return jsonify({"Status": "Failed", "reason": "name"}), 406

        ag = db.session.query(AG).filter_by(id=ag_id).scalar()

        if request.values.get('displayname') is not None:
            ag.displayname = request.values["displayname"]

        if request.values.get('description') is not None:
            ag.description = request.values["description"]

    except:
        return NotFound()


@bp.route("/", methods=["GET"])
def get_all_ags():
    all_ags = AG.query.all()
    result = ags_schema.dump(all_ags)
    return jsonify(result)
