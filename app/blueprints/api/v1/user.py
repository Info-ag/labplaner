import datetime
import json

from flask import Blueprint, request, jsonify, g
from werkzeug.exceptions import NotFound, Unauthorized, BadRequest, Forbidden
from sqlalchemy import exists, and_

from app import db
from app.utils import requires_auth
import app.algorithm

from app.models.user import User, UserSchema, UserSchemaDates
from app.models.associations import UserDate, UserAG
from app.models.date import Date
from app.models.event import Event, EventSchema

bp = Blueprint('user_api', __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_dates_schema = UserSchemaDates()
event_schema = EventSchema()
events_schema = EventSchema(many=True)


@bp.route('/', methods=['POST'])
def add_user():
    try:
        username = request.values['username']
        if db.session.query(User).filter_by(username=username).scalar() is not None:
            return BadRequest(description='Username already exists')
        email = request.values.get('email')
        if db.session.query(User).filter_by(email=email).scalar() is not None:
            return BadRequest(description='Email already exists')
        password = request.values.get('password')
        if len(password) < 8:
            return BadRequest(description='Keylength too short')
        user = User()
        user.username = request.values['username']
        user.email = request.values['email']
        user.set_password(request.values['password'])

        db.session.add(user)
        db.session.commit()

        return user_schema.jsonify(user), 200
    except:
        return BadRequest()


@bp.route('/id/<uid>', methods=['GET'])
def get_user_by_id(uid):
    user = User.query.get(uid)
    return user_schema.jsonify(user)


@bp.route('/username/<username>', methods=['GET'])
def get_user_by_username(username):
    user = User.query.filter_by(username=username).scalar()
    return user_schema.jsonify(user)


def query_by_username(query: str, count=5):
    if count > 20:
        count = 20

    users: list = User.query.filter(
        User.username.ilike('%' + '%'.join(query[i:i + 1] for i in range(0, len(query), 1)) + '%')).all()
    return users_schema.jsonify(users[:len(users) if len(users) < count else count])


@bp.route('/', methods=['GET'])
def get_all_users():
    if request.args.get('query', default=None, type=str) is not None:
        return query_by_username(
            request.args.get('query', default=None, type=str),
            count=request.args.get('count', default=5, type=int)
        )
    count = request.args.get('count', default=5, type=int)
    all_users = User.query.all()
    return users_schema.jsonify(all_users[:len(all_users) if len(all_users) < count else count])


@bp.route('/self/dates', methods=['POST'])
@requires_auth()
def set_dates():
    user = g.user

    UserDate.query.filter_by(user_id=g.session.user_id).delete()
    db.session.commit()

    dates = request.values.getlist('dates[]')
    for _date in dates:
        d = datetime.datetime.strptime(_date, '%a %b %d %Y')
        if not db.session.query(Date).filter_by(day=d.isoformat()[:10]).scalar():
            date_obj = Date()
            date_obj.day = d
            db.session.add(date_obj)

        u = UserDate()
        u.date_id = db.session.query(Date).filter_by(day=d.isoformat()[:10]).scalar().id
        u.user_id = user.id

        db.session.add(u)
    db.session.commit()

    app.algorithm.do_your_work()

    return jsonify({'status': 'success', 'redirect': '/'}), 200


@bp.route('/self/dates', methods=['GET'])
@requires_auth()
def get_dates():
    user = User.query.filter_by(id=g.session.user_id).scalar()

    return user_dates_schema.jsonify(user)


@bp.route('/self/events', methods=['GET'])
@requires_auth()
def get_events_for_user():
    ags = UserAG.query.filter_by(user_id=g.session.user_id)
    event_list = {'events': []}
    for ag in ags:
        events = Event.query.filter_by(ag_id=ag.ag_id)
        for event in events:
            event_schema.context = {'event_id': event.id}
            event_list['events'].append(event_schema.dump(event)[0])

    return jsonify(event_list)

@bp.route("<ag_name>/user/inviteable", methods=["GET"])
@utils.requires_auth()
def get_inviteable_user(ag_name):
    if db.session.query(exists().where(AG.name == ag_name)).scalar():
        query = request.values.get('query')
        ag_id = db.session.query(AG).filter_by(name = ag_name).first().id
        users = db.session.query(User).join(UserAG, and_(UserAG.ag_id == ag_id, UserAG.user_id == User.id), isouter = True).filter(and_(UserAG.ag_id == None, User.username.like(f'%{query}%')))
        return users_schema.jsonify(users)
    
    else:
        return NotFound()

