'''
All Blueprint routes regarding interacting with users
'''

import datetime

from flask import Blueprint, request, jsonify, g
from werkzeug.exceptions import BadRequest

from app.models import db
from app.util import requires_auth
# import app.algorithm

from app.models.user import User, UserSchema, UserSchemaDates
from app.models.associations import UserDate, UserAG
from app.models.date import Date
from app.models.event import Event, EventSchema

import app.mail as mail

bp = Blueprint('user_api', __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_dates_schema = UserSchemaDates()
event_schema = EventSchema()
events_schema = EventSchema(many=True)


@bp.route('/', methods=['POST'])
def add_user():
    """Create a new user

    This API route is used to sign up a user.
    username, email and password are validated
    :return: new user as JSON object
        BadRequest if validation fails
    """
    try:
        username = request.values.get('username')
        if db.session.query(User).filter_by(username=username).scalar() is not None:
            return BadRequest(description='Username already exists')
        email = request.values.get('email')
        if db.session.query(User).filter_by(email=email).scalar() is not None:
            return BadRequest(description='Email already exists')
        password = request.values.get('password')
        if len(password) < 8:
            return BadRequest(description='Keylength too short')
        user = User()
        user.username = request.values.get('username')
        user.email = request.values.get('email')
        user.set_password(request.values.get('password'))

        db.session.add(user)
        db.session.commit()
        mail.confirmation_mail(user)

        return user_schema.jsonify(user), 200
    except Exception as e:
        print(e)
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
    """POST: Set dates for a user

    Requires an array of dates (dates[])
    :return: JSON with redirect if success
        TODO error if fail
    """
    user = g.user

    UserDate.query.filter_by(user_id=g.session.user_id).delete()
    db.session.commit()

    dates = request.values.getlist('dates[]')
    for _date in dates:
        formatted_datetime = datetime.datetime.strptime(_date, '%a %b %d %Y')
        if not db.session.query(Date).filter_by(day=formatted_datetime.isoformat()[:10]).scalar():
            date_obj = Date()
            date_obj.day = formatted_datetime
            db.session.add(date_obj)

        user_date = UserDate()
        user_date.date_id = db.session.query(Date).filter_by(day=formatted_datetime.isoformat()[:10]).scalar().id
        user_date.user_id = user.id

        db.session.add(user_date)
    db.session.commit()

    # app.algorithm.do_your_work()

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
