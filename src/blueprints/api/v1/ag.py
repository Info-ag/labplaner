import re

from flask import Blueprint, request, jsonify, g
from sqlalchemy.sql import exists, and_
from werkzeug.exceptions import NotFound, BadRequest, Forbidden

from src.models.ag import AG, AGSchema, AGSchemaIntern
from src.models.user import User, UserSchema
from src.models.associations import UserAG
from src.main import db

from src.utils import requires_auth

from config.regex import ag_regex

bp = Blueprint('ag_api', __name__)

users_schema = UserSchema(many=True)
ag_schema = AGSchema()
ag_schema_intern = AGSchemaIntern()
ags_schema = AGSchema(many=True)


@bp.route('/', methods=['POST'])
@requires_auth()
def add_ag():
    '''
    Create a new AG. The request body has to inclurde the following:
        :key: name: AG name used to identify the ag (eg. /ag/<name>)
        :key: display_name: AG name that is human read able
        (can contain spaces etc.)
        :key: description: A description of the AG
    :return: If everything went as it should, the newly created AG is
    returned.
    '''
    name = request.values.get('name')
    display_name = request.values.get('display_name')
    description = request.values.get('description')

    if db.session.query(exists().where(AG.name == name)).scalar() or not bool(re.match(ag_regex.name, name)):
        return jsonify({'reason': 'name'}), 400
    if db.session.query(exists().where(AG.display_name == display_name)).scalar() or not bool(
            re.match(ag_regex.display_name, display_name)):
        return jsonify({'reason': 'display_name'}), 400
    if not bool(re.match(ag_regex.description, description)):
        return jsonify({'reason': 'description'}), 400

    ag: AG = AG()
    ag.name = name
    ag.display_name = display_name
    ag.description = description
    ag.color = request.values.get('color', default='primary')

    # Add the AG to the DB to create a new id
    db.session.add(ag)
    db.session.flush()

    user_ag = UserAG()
    user_ag.user_id = g.session.user_id
    user_ag.ag_id = ag.id
    user_ag.role = 'MENTOR'

    db.session.add(user_ag)
    db.session.commit()

    return jsonify({'status': 'success', 'redirect': f'/ag/{name}/invite'}), 200


@bp.route('/id/<ag_id>', methods=['GET'])
@requires_auth()
def get_ag_by_id(ag_id):
    '''
    Query an AG specified by its id
    :param ag_id: A specific id
    :return: JSON representation of the AG
    '''
    if db.session.query(exists().where(AG.id == ag_id)).scalar():
        ag = AG.query.get(ag_id).scalar()
        if db.session.query(exists().where(UserAG.user_id == g.session.user_id and UserAG.ag_id == ag_id)).scalar():
            return ag_schema_intern.jsonify(ag), 200
        else:
            return ag_schema.jsonify(ag), 200
    else:
        return NotFound()


@bp.route('/name/<name>', methods=['GET'])
@requires_auth()
def get_ag_by_name(name):
    '''
    Query an AG specified by its unique name
    :param name: A specific AG name
    :return: JSON representation of the AG
    '''
    if db.session.query(exists().where(AG.name == name)).scalar():
        ag = AG.query.filter_by(name=name).scalar()
        if db.session.query(exists().where(UserAG.user_id == g.session.user_id and UserAG.ag_id == ag.id)).scalar():
            return ag_schema_intern.jsonify(ag), 200
        else:
            return ag_schema.jsonify(ag), 200
    else:
        return NotFound()


@bp.route('/<ag_id>/invite', methods=['POST'])
@requires_auth()
def add_user_to_ag(ag_id):
    '''
    Invite (a) user(s) to a specific AG.
    The request body has to include the following:
        :key: users[]: A list of user names that should be added to the AG
    :param ag_id: The id of the AG
    :return: Redirect to the next step if all went as expected
    '''
    if db.session.query(exists().where(AG.id == ag_id)).scalar():
        if db.session.query(exists().where(UserAG.user_id == g.session.user_id and UserAG.ag_id == ag_id)).scalar():
            user_ag = UserAG.query.filter_by(user_id=g.session.user_id, ag_id=ag_id).scalar()
            if user_ag.role == 'MENTOR':
                ag: AG = AG.query.filter_by(id=ag_id).scalar()
                for username in request.values.getlist('users[]'):
                    if db.session.query(exists().where(User.username == username)).scalar():
                        user: User = User.query.filter_by(username=username).scalar()
                        print(user)

                        if db.session.query(UserAG.query.filter_by(user_id=user.id, ag_id=ag.id).exists()).scalar():
                            continue

                        new_user_ag = UserAG()
                        new_user_ag.role = 'PARTICIPANT'
                        new_user_ag.user_id = user.id
                        new_user_ag.ag_id = ag.id

                        db.session.add(new_user_ag)

                db.session.commit()
                return jsonify({'redirect': f'/ag/{ag.name}'}), 200
        # Either there is no relationship between the ag and the authenticated user
        # or the user is not a mentor of the ag.
        return Forbidden()
    else:
        return NotFound()


@bp.route('/<ag_id>', methods=['PUT'])
@requires_auth()
def change_ag_values(ag_id):
    '''
    Change values of an AG.
    The request body may include the following:
        :key: display_name: String with new display_name
        :key: description: String with new description
    :param ag_id: AG id for which ag the provided values should be changed
    :return:
    '''
    if db.session.query(exists().where(AG.id == ag_id)).scalar():
        if db.session.query(exists().where(UserAG.user_id == g.session.user_id and UserAG.ag_id == ag_id)).scalar():
            user_ag = UserAG.query.filter_by(user_id=g.session.user_id, ag_id=ag_id).scalar()
            if user_ag.role == 'MENTOR':
                ag: AG = AG.query.filter_by(id=ag_id).scalar()

                display_name = request.values.get('display_name')
                description = request.values.get('description')

                value_changed = False

                if bool(re.match(regex_match_display_name, display_name)):
                    ag.display_name = display_name
                    value_changed = True
                if bool(re.match(regex_match_description, description)):
                    ag.description = description
                    value_changed = True

                if value_changed:
                    db.session.merge(ag)
                    db.session.commit()
                    return jsonify({'status': 'success'}), 200
                else:
                    return BadRequest()

        # Either there is no relationship between the ag and the authenticated user
        # or the user is not a mentor of the ag.
        return Forbidden()
    else:
        return NotFound()


@bp.route('/', methods=['GET'])
@requires_auth()
def get_all_ags():
    count = request.args.get('count', default=5, type=int)
    offset = request.args.get('offset', default=0, type=int)

    if count > 20:
        count = 20

    all_ags = AG.query.all()
    # all_ags.offset(offset)
    # all_ags.limit(count)
    return ags_schema.jsonify(all_ags)

@bp.route('<ag_name>/user/inviteable', methods=['GET'])
@requires_auth()
def get_inviteable_user(ag_name):
    if db.session.query(exists().where(AG.name == ag_name)).scalar():
        query = request.values.get('query')
        ag_id = db.session.query(AG).filter_by(name = ag_name).first().id
        users = db.session.query(User).join(UserAG, and_(UserAG.ag_id == ag_id, UserAG.user_id == User.id), isouter = True).filter(and_(UserAG.ag_id == None, User.username.like(f'%{query}%')))
        return users_schema.jsonify(users)
    
    else:
        return NotFound()
