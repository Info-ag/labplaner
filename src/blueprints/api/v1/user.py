from flask import Blueprint, request, jsonify
from models.user import User, UserSchema
from app import db
from models.associations import DateUser

bp = Blueprint("user_api", __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@bp.route("/", methods=["POST"])
def add_user():
    try:
        username = request.values["username"]
        if db.session.query(User).filter_by(username=username).scalar() is not None:
            return jsonify({"Status": "Failed", "reason": "username"}), 406
        email = request.values["email"]
        if db.session.query(User).filter_by(email=email).scalar() is not None:
            return jsonify({"Status": "Failed", "reason": "email"}), 406
        password = request.values["password"]
        if len(password) < 8:
            return jsonify({"Status": "Failed", "reason": "password"}), 406
        user = User()
        user.username = request.values["username"]
        user.email = request.values["email"]
        user.set_password(request.values["password"])

        db.session.add(user)
        db.session.commit()

        return user_schema.jsonify(user), 200
    except:
        return jsonify({"Status": "Failed"}), 406


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


@bp.route("/dates", methods=["POST"])
def set_dates():

    if not g.session.authenticated:
        return jsonify({"Status": "Failed"}), 406

    try:
        uid = request.values["uid"]
        if db.session.query(User).filter_by(id=uid).scalar() is None:
            return jsonify({"Status": "Failed", "reason": "uid"}), 406

        dates = request.values["dates"]

        for d in dates:

            d = d.replace('-', '')
            d = date(int(d[:4]), int(d[4:6]), int(d[6:]))

            if db.session.query(Date).filter_by(day=d) is None:
                date_obj = Date()
                date_obj.day = d

                db.session.add(date_obj)
                db.session.commit()


            else:
                date_obj = db.session.query(Date).filter_by(day=d)

            date_user = DateUser()
            date_user.dtid = date_obj.id
            date_user.uid = uid

            db.session.add(date_user)
            db.session.commit()
