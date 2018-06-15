'''
basic blueprint routes for interacting with an AG
'''
import re
from flask import Blueprint, request, jsonify, g, url_for, flash, redirect
from sqlalchemy.sql import exists, and_
from werkzeug.exceptions import BadRequest, PreconditionFailed
from app.models import db

from app import app

from app.models.ag import AG, AGSchema, AGSchemaIntern
from app.models.associations import UserAG

from app.utils import requires_auth
from app.utils.assocations import requires_mentor, requires_member_association
from app.utils.ag import requires_ag
from app.utils.user import get_user_by_username

from config.regex import AGRegex


from app.blueprints.api.v1.ag import applications, invitations, messages

bp = Blueprint('ag_api', __name__)

app.register_blueprint(invitations.bp, url_prefix='/invitations')
app.register_blueprint(applications.bp, url_prefix='/applications')
app.register_blueprint(messages.bp, url_prefix='/messages')


ag_schema_intern = AGSchemaIntern()
ag_schema = AGSchema()
ags_schema = AGSchema(many=True)

@bp.route('/', methods=['POST'])
@requires_auth()
def add_ag():
    '''
    Create a new AG. The request body has to include the following:
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

    if db.session.query(exists().where(AG.name == name)).scalar() or not bool(
            re.match(AGRegex.name, name)):
        return jsonify({'reason': 'name'}), 400
    if db.session.query(exists().where(AG.display_name == display_name)).scalar() or not bool(
            re.match(AGRegex.display_name, display_name)):
        return jsonify({'reason': 'display_name'}), 400
    if not bool(re.match(AGRegex.description, description)):
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
    user_ag.status = 'ACTIVE'
    user_ag.role = 'MENTOR'

    db.session.add(user_ag)
    db.session.commit()

    return jsonify({'status': 'success', 'redirect': url_for('ag.invite_ag', ag_name=ag.name)}), 200


@bp.route('/id/<ag_id>', methods=['GET'])
@requires_auth()
@requires_ag()
def get_ag_by_id(ag_id, ag):
    '''
    Query an AG specified by its id
    :param ag_id: A specific id
    :return: JSON representation of the AG
    '''
    if db.session.query(exists().where(UserAG.user_id == g.session.user_id and \
            UserAG.ag_id == ag_id)).scalar():
        return ag_schema_intern.jsonify(ag), 200
    else:
        return ag_schema.jsonify(ag), 200

@bp.route('/name/<ag_name>', methods=['GET'])
@requires_auth()
@requires_ag()
def get_ag_by_name(ag_name, ag):
    '''
    Query an AG specified by its unique name
    :param name: A specific AG name
    :return: JSON representation of the AG
    '''
    if db.session.query(exists().where(UserAG.user_id == g.session.user_id and \
            UserAG.ag_id == ag.id)).scalar():
        return ag_schema_intern.jsonify(ag), 200
    else:
        return ag_schema.jsonify(ag), 200


@bp.route('/<ag_id>', methods=['PUT'])
@requires_auth()
@requires_mentor()
def change_ag_values(ag_id, ag, user_ag):
    '''
    Change values of an AG.
    The request body may include the following:
        :key: display_name: String with new display_name
        :key: description: String with new description
    :param ag_id: AG id for which ag the provided values should be changed
    :return:
    '''
    ag: AG = AG.query.filter_by(id=ag_id).scalar()

    display_name = request.values.get('display_name', default=None)
    description = request.values.get('description', default=None)

    value_changed = False

    if display_name is not None and bool(re.match(AGRegex.display_name, display_name)):
        ag.display_name = display_name
        value_changed = True
    if description is not None and bool(re.match(AGRegex.description, description)):
        ag.description = description
        value_changed = True

    if value_changed:
        db.session.merge(ag)
        db.session.commit()
        return jsonify({'status': 'success'}), 200
    else:
        return BadRequest()

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


@bp.route('<ag_name>/submit_setting', methods=['GET'])
@requires_auth()
@requires_mentor()
def update_users(ag_name, user_ag, ag):
    for user_id in request.values:
        role = request.values.get(user_id)
        edit_user_ag = db.session.query(UserAG).filter(and_(UserAG.user_id == user_id,\
                        UserAG.ag_id == ag.id)).one()
        edit_user_ag.role = role
        db.session.flush()
    if not ag.mentors:
        flash(u'An AG needs a minimum of one Mentor', 'error')
        return redirect(url_for('ag.ag_settings', ag_name=ag_name))
    db.session.commit()
    flash(f'Successfully changed the roles in {ag.display_name}', 'success')
    return redirect(url_for('ag.ag_dashboard', ag_name=ag_name))



@bp.route('<ag_name>/leave')
@requires_auth()
@requires_member_association()
def leave_ag(ag_name, ag, user_ag):
    if user_ag.role == 'NONE':
        flash('You cannot leave an AG you are not in', 'error')
        return redirect(url_for('ag.ag_dashboard', ag_name=ag_name))
    user_ag.role = 'NONE'
    user_ag.status = 'LEFT'
    db.session.flush()
    if not ag.actual_users:
        db.session.delete(ag)
        db.session.flush()
        flash(f'You sucessfully left and deleted the AG {ag.name}', 'success')
    elif not ag.mentors:
        flash(f'You cannot leave an AG, when there is no Mentor left afterwards', 'error')
        return redirect(url_for('ag.ag_dashboard', ag_name=ag_name))
    else:
        user_ag.role = 'NONE'
        user_ag.status = 'LEFT'
        db.session.flush()
        flash(f'You sucessfully left the AG {ag.name}', 'success')
    db.session.commit()
    return redirect(url_for('index'))



@bp.route('<ag_name>/kick/<user_name>')
@requires_auth()
@requires_mentor()
def kick_user(ag_name, user_name, ag, user_ag):

    user = get_user_by_username(user_name)
    edit_user_ag = db.session.query(UserAG).filter_by(user_id=user.id, ag_id=ag.id).scalar()
    if edit_user_ag is None or edit_user_ag.role == 'NONE':
        flash(f'You cannot kick {user.username} from {ag.display_name}.')
        return redirect(url_for('ag.ag_dashboard', ag_name=ag_name))
    edit_user_ag.role = 'NONE'
    edit_user_ag.status = 'KICKED'
    db.session.flush()
    if not ag.actual_users:
        db.session.delete(ag)
        db.session.commit()
        flash(f'You sucessfully left and deleted the AG {ag.display_name}', 'success')
        return redirect(url_for('index'))
    elif not ag.mentors:
        flash(f'You cannot kick the last Mentor of {ag.display_name}', 'error')
    else:
        flash(f'You sucessfully kicked {user.username} from the AG {ag.display_name}', 'success')
        db.session.commit()
    return redirect(url_for('ag.ag_dashboard', ag_name=ag_name))

@bp.route('<ag_name>/delete')
@requires_auth()
@requires_mentor()
def delete_ag(ag_name, ag, user_ag):
    db.session.delete(ag)
    db.session.commit()
    flash(f'You successfully deleted the AG {ag.display_name}', 'success')
    return redirect(url_for('index'))
