from flask import Blueprint, request, jsonify, g
from models.ag import AG, AGSchema
from models.associations import UserAG
from app import db

bp = Blueprint("ag_api", __name__)

ag_schema = AGSchema()
ags_schema = AGSchema(many=True)


@bp.route("/", methods=["POST"])
def add_ag():
    if not g.session.authenticated:
        return jsonify({"Status": "Failed"}), 406
    try:
        name = request.values["name"]
        if db.session.query(AG).filter_by(name=name).scalar() is not None:
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
        db.session.commit()

        userag = UserAG()
        userag.uid = g.session.uid
        userag.agid = ag.id
        userag.role = "MENTOR"
        print(ag.id)

        db.session.add(userag)
        db.session.commit()

        return ag_schema.jsonify(ag), 200
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


@bp.route("/", methods=["GET"])
def get_all_ags():
    all_ags = AG.query.all()
    result = ags_schema.dump(all_ags)
    return jsonify(result)
