from datetime import date
from flask import Blueprint, request, jsonify
from models.event import Event, EventSchema
from models.ag import AG
from models.date import Date
from models.associations import DateEvent
from app import db

bp = Blueprint("event_api", __name__)

event_schema = EventSchema()
events_schema = EventSchema(many=True)


@bp.route("/events/", methods=["POST"])
def add_event():
    if not g.session.authenticated:
        return jsonify({"Status": "Failed"}), 406

    try:
        name = request.values["name"]
        if db.session.query(Event).filter_by(name=name).scalar() is not None:
            return jsonify({"Status": "Failed", "reason": "name"}), 406
        ag = request.values["ag"]
        if db.session.query(AG).filter_by(name=ag).scalar() is None:
            return jsonify({"Status": "Failed", "reason": "ag"}), 406
        if len(request.values["displayname"]) > 48:
            return jsonify({"Status": "Failed", "reason": "displayname"}), 406
        if len(request.values["description"]) > 280:
            return jsonify({"Status": "Failed", "reason": "description"}), 406
        raw_date = request.values["date"]
        if len(raw_date) != 8 or int(raw_date[0]) > 3 or int(raw_date[2]) > 1 or int(raw_date[4]) != 2 or int(raw_date[5]) != 0:
            return jsonify({"Status": "Failed", "reason": "date (DDMMYYYY)"}), 406

        obj_date = date(int(raw_date[:2]), int(raw_date[2:4]), int(raw_date[4:]))

        event = Event()
        event.name = name
        event.display_name = request.values["displayname"]
        event.description = request.values["description"]
        event.ag = ag

        db.session.add(event)
        db.session.commit()

        if db.session.query(Date).filter_by(day=obj_date) is None:
            d = Date()
            d.day = obj_date

            db.session.add(d)
            db.session.commit()

        else:
            d = db.session.query(Date).filter_by(day=obj_date)

        dateevent = DateEvent()
        dateevent.dtid = d.id
        dateevent.evid = event.id

        db.session.add(dateevent)
        db.session.commit()

        dateevent = DateEvent()
        dateevent.dtid = d.id
        dateevent.evid = event.id

        db.session.add(dateevent)
        db.session.commit()

        return jsonify({"redirect": f"/event/{name}/invite"}), 200
    except:
        return jsonify({"Status": "Failed"}), 406


@bp.route("/events/id/<evid>", methods=["GET"])
def get_event_by_id(evid):
    event = Event.query.get(evid)
    return event_schema.jsonify(event)


@bp.route("/events/name/<name>", methods=["GET"])
def get_event_by_name(name):
    event = Event.query.filter_by(name=name).scalar()
    return event_schema.jsonify(event)


@bp.route("/events/", methods=["GET"])
def get_all_events():
    all_events = Event.query.all()
    result = event_schema.dump(all_events)
    return jsonify(result)
