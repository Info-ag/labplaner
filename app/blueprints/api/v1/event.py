import datetime

from flask import Blueprint, request, jsonify, g
from sqlalchemy.sql import exists
from werkzeug.exceptions import NotFound, Unauthorized

from app.utils import requires_auth

from app.models.event import Event, EventSchema
from app.models.ag import AG
from app.models.date import Date
from app.models.associations import UserAG

from app.models import db

bp = Blueprint('event_api', __name__)

event_schema = EventSchema()
events_schema = EventSchema(many=True)


@bp.route('/', methods=['POST'])
@requires_auth()
def add_event():
    ag_id = request.values.get('ag')

    if db.session.query(exists().where(AG.id == ag_id)).scalar():
        if db.session.query(exists().where(UserAG.user_id == g.session.user_id and UserAG.ag_id == ag_id)).scalar():
            user_ag = UserAG.query.filter_by(user_id=g.session.user_id, ag_id=ag_id).scalar()
            if user_ag.role == 'MENTOR':
                display_name = request.values.get('display_name')
                description = request.values.get('description')
                if len(display_name) == 0 or len(display_name) > 48:
                    return jsonify({'reason': 'display_name'}), 400
                if len(description) > 280:
                    return jsonify({'reason': 'description'}), 400

                event = Event()
                event.display_name = display_name
                event.description = description
                event.ag_id = ag_id
                event.date = None

                db.session.add(event)

                dates = request.values.getlist('dates[]')
                for _date in dates:
                    d = datetime.datetime.strptime(_date, '%a %b %d %Y').date()
                    if db.session.query(exists().where(Date.day == d)).scalar():
                        u_date = Date.query.filter_by(day=d).scalar()
                        u_date.users.append(g.user)
                        u_date.events.append(event)
                        continue
                    else:
                        date_obj: Date = Date()
                        date_obj.users.append(g.user)
                        date_obj.events.append(event)
                        date_obj.day = d
                        db.session.add(date_obj)

                db.session.commit()
                return jsonify({'status': 'success', 'redirect': '/'}), 200

        return Unauthorized()
    return NotFound()


@bp.route('/id/<evid>', methods=['GET'])
def get_event_by_id(evid):
    event = Event.query.get(evid)
    return event_schema.jsonify(event)


@bp.route('/name/<name>', methods=['GET'])
def get_event_by_name(name):
    event = Event.query.filter_by(name=name).scalar()
    return event_schema.jsonify(event)


@bp.route('/month/<month>', methods=['GET'])
def get_events_by_month(month):
    events = Date.query.filter((Date.events != None) | (Date.events != 0)).filter(Date.day.month == int(month))
    return event_schema.jsonify(events)


@bp.route('/', methods=['GET'])
def get_all_events():
    all_events = Event.query.all()
    result = events_schema.dump(all_events)
    return jsonify(result)
