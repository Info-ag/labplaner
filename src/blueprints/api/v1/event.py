from datetime import date
from flask import Blueprint, request, jsonify, g
from sqlalchemy.sql import exists
import datetime
from werkzeug.exceptions import NotFound, Unauthorized, BadRequest, Forbidden, RequestEntityTooLarge
from models.event import Event, EventSchema
from models.ag import AG
from models.date import Date
from models.associations import EventDate, UserAG
from app import db

bp = Blueprint("event_api", __name__)

event_schema = EventSchema()
events_schema = EventSchema(many=True)


@bp.route("/", methods=["POST"])
def add_event():
    if not g.session.authenticated:
        return Unauthorized()

    ag_id = request.values.get("ag")

    if db.session.query(exists().where(AG.id == ag_id)).scalar():
        if db.session.query(exists().where(UserAG.user_id == g.session.uid and UserAG.ag_id == ag_id)).scalar():
            user_ag = UserAG.query.filter_by(uid=g.session.uid, ag_id=ag_id).scalar()
            if user_ag.role == "MENTOR":
                display_name = request.values.get("display_name")
                description = request.values.get("description")
                if len(display_name) == 0 or len(display_name) > 48:
                    return RequestEntityTooLarge('Maximum length of 48 characters')
                if len(description) > 280:
                    return RequestEntityTooLarge('Maximum length of 280 characters')

                event = Event()
                event.display_name = display_name
                event.description = description
                event.ag = ag_id
                event.date = None

                db.session.add(event)
                db.session.flush()

                dates = request.values.getlist("dates")
                for date in dates:
                    d = datetime.datetime.strptime(date, "%a %b %d %Y")
                    date_obj = Date()
                    date_obj.event = event.id
                    date_obj.day = d

                    db.session.add(date_obj)

                db.session.commit()

                return jsonify({"Status": "Success", "redirect": "/"})

        return Unauthorized()
    return NotFound()


@bp.route("/dates", methods=["POST"])
def add_dates():
    try:
        if not g.session.authenticated:
            return Unauthorized()
    except NameError:
        return Unauthorized()

    try:
        name = request.values["name"]
        if db.session.query(Event).filter_by(name=name).scalar() is None:
            return NotFound(description='Eventname not found')
        dates = request.values["dates"]

        event = db.session.query(Event).filter_by(name=name).scalar()

        for d in dates:

            d = d.replace('-', '')
            d = date(int(d[:4]), int(d[4:6]), int(d[6:]))

            if db.session.query(Date).filter_by(day=d) is None:
                date_obj = Date()
                date_obj.day = obj_date

                db.session.merge(date_obj)
                db.session.commit()

            else:
                date_obj = db.session.query(Date).filter_by(day=d)

            date_event = EventDate()
            date_event.date_id = date_obj.id
            date_event.event_id = event.id

            db.session.merge(date_event)
            db.session.commit()

        return jsonify({"redirect": f"/event/{name}/invite"}), 200
    except:
        return BadRequest()


@bp.route("/id/<evid>", methods=["GET"])
def get_event_by_id(evid):
    event = Event.query.get(evid)
    return event_schema.jsonify(event)


@bp.route("/name/<name>", methods=["GET"])
def get_event_by_name(name):
    event = Event.query.filter_by(name=name).scalar()
    return event_schema.jsonify(event)


@bp.route("/month/<month>", methods=["GET"])
def get_events_by_month(month):
    events = Date.query.filter((Date.events != None) | (Date.events != 0)).filter(Date.day.month == int(month))
    return event_schema.jsonify(events)


@bp.route("/", methods=["GET"])
def get_all_events():
    all_events = Event.query.all()
    result = event_schema.dump(all_events)
    return jsonify(result)
