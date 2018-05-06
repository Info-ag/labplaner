import datetime

from flask import Blueprint, request, jsonify
from werkzeug.exceptions import NotFound, Unauthorized, BadRequest, Forbidden


from app import db
import utils

from models.user import User, UserSchema
from models.associations import UserDate
from models.date import Date


bp = Blueprint("user_api", __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@bp.route("/", methods=["POST"])
def add_user():
    try:
        username = request.values["username"]
        if db.session.query(User).filter_by(username=username).scalar() is not None:
            return BadRequest(description='Username already exists')
        email = request.values["email"]
        if db.session.query(User).filter_by(email=email).scalar() is not None:
            return BadRequest(description='Email already exists')
        password = request.values["password"]
        if len(password) < 8:
            return BadRequest(description='Keylength too short')
        user = User()
        user.username = request.values["username"]
        user.email = request.values["email"]
        user.set_password(request.values["password"])

        db.session.add(user)
        db.session.commit()

        return user_schema.jsonify(user), 200
    except:
        return BadRequest()


@bp.route("/id/<uid>", methods=["GET"])
def get_user_by_id(uid):
    user = User.query.get(uid)
    return user_schema.jsonify(user)


@bp.route("/username/<username>", methods=["GET"])
def get_user_by_username(username):
    user = User.query.filter_by(username=username).scalar()
    return user_schema.jsonify(user)


def query_by_username(query: str, count=5):
    if count > 20:
        count = 20

    users: list = User.query.filter(
        User.username.ilike("%" + "%".join(query[i:i + 1] for i in range(0, len(query), 1)) + "%")).all()
    return users_schema.jsonify(users[:len(users) if len(users) < count else count])


@bp.route("/", methods=["GET"])
def get_all_users():
    if request.args.get('query', default=None, type=str) is not None:
        return query_by_username(
            request.args.get('query', default=None, type=str),
            count=request.args.get('count', default=5, type=int)
        )
    count = request.args.get('count', default=5, type=int)
    all_users = User.query.all()
    return users_schema.jsonify(all_users[:len(all_users) if len(all_users) < count else count])


@bp.route("/dates/<uid>", methods=["POST"])
@utils.requires_auth()
def set_dates(uid):

    if db.session.query(User).filter_by(id=uid).scalar() is None:
        return NotFound(description='UserID not found')
    else:
        print(db.session.query(User).all())
        user = db.session.query(User).filter_by(id=uid).scalar()

    #dates = request.values.getlist("dates[]")
    dates = ['Wed Oct 31 2018']
    for _date in dates:
        print(_date)
        d = datetime.datetime.strptime(_date, "%a %b %d %Y")
        if not db.session.query(Date).filter_by(day=d.isoformat()[:10]).scalar():
            date_obj = Date()
            date_obj.day = d

        db.session.add(date_obj)

        u = UserDate()
        u.date_id = db.session.query(Date).filter_by(day=d.isoformat()[:10]).scalar().id
        u.user_id = user.id

        db.session.add(u)
    db.session.commit()

    return jsonify({"status": "success", "redirect": "/"}), 200
