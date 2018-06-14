import re

from flask import Blueprint, request, jsonify, g, url_for, flash, redirect
from sqlalchemy.sql import exists, and_, or_
from werkzeug.exceptions import NotFound, BadRequest, Forbidden, PreconditionFailed

from app.models.ag import AG, AGSchema, AGSchemaIntern
from app.models.user import User, UserSchema
from app.models.associations import UserAG
from app.models import db

from app.utils import requires_auth, requires_mentor, requires_ag, requires_member_association, requires_gracefully_not_member, get_user_by_username, get_membership

from config.regex import AGRegex

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

    if db.session.query(exists().where(AG.name == name)).scalar() or not bool(re.match(AGRegex.name, name)):
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
    if db.session.query(exists().where(UserAG.user_id == g.session.user_id and UserAG.ag_id == ag_id)).scalar():
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
    if db.session.query(exists().where(UserAG.user_id == g.session.user_id and UserAG.ag_id == ag.id)).scalar():
        return ag_schema_intern.jsonify(ag), 200
    else:
        return ag_schema.jsonify(ag), 200


@bp.route('/<ag_id>/invite', methods=['POST'])
@requires_auth()
@requires_mentor()
def add_user_to_ag(ag_id, ag, user_ag):
    '''
    Invite (a) user(s) to a specific AG.
    The request body has to include the following:
        :key: users[]: A list of user names that should be added to the AG
    :param ag_id: The id of the AG
    :return: Redirect to the next step if all went as expected
    '''
    for username in request.values.getlist('users[]'):
        if db.session.query(exists().where(User.username == username)).scalar():
            user: User = User.query.filter_by(username=username).scalar()
            print(user)

            new_user_ag = db.session.query(UserAG).filter_by(user_id=user.id, ag_id=ag.id).scalar()
            if new_user_ag:
                if (new_user_ag.status == "LEFT" or new_user_ag.status == "REJECTED") and new_user_ag.role == "NONE":
                    new_user_ag.role = 'NONE'
                    new_user_ag.status = 'INVITED'
                elif new_user_ag.status == "APPLIED" and new_user_ag.role == "NONE":
                    new_user_ag.role = 'PARTICIPANT'
                    new_user_ag.status = 'ACTIVE'
                else:
                    continue
            else:
                new_user_ag = UserAG()
                new_user_ag.user_id = user.id
                new_user_ag.ag_id = ag.id
                new_user_ag.role = 'NONE'
                new_user_ag.status = 'INVITED'

            db.session.add(new_user_ag)

    db.session.commit()
    return jsonify({'redirect': f'/ag/{ag.name}'}), 200

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

@bp.route('<ag_name>/user/inviteable', methods=['GET'])
@requires_auth()
@requires_ag()
def get_inviteable_user(ag_name, ag):
    query = request.values.get('query', default='')
    users = db.session.query(User).join(UserAG, and_(UserAG.ag_id == ag.id, UserAG.user_id == User.id), isouter = True).filter(or_((and_(UserAG.ag_id == None, User.username.like(f'%{query}%'))), (and_(UserAG.ag_id == ag.id, UserAG.role == "NONE", or_(UserAG.status == "LEFT", UserAG.status == "REJECTED", UserAG.status == "APPLIED"), User.username.like(f'%{query}%')))))
    print(users)
    return users_schema.jsonify(users)

@bp.route('invitation/<ag_name>/accept')
@requires_auth()
@requires_member_association()
def accept_invitation(ag_name, ag, user_ag):
    if user_ag.role != "NONE" or user_ag.status != "INVITED":
        flash(f'This invitartion is invalid', 'error')
        return redirect(url_for('index'))
    user_ag.role = "PARTICIPANT"
    user_ag.status = "ACTIVE"
    db.session.add(user_ag)
    db.session.commit()
    flash(f'You successfully accepted the invitation to {ag.display_name}', 'success')
    return redirect(url_for('ag.ag_dashboard', ag_name=ag_name))
    

@bp.route('invitation/<ag_name>/decline')
@requires_auth()
@requires_member_association()
def decline_invitation(ag_name, ag, user_ag):
    if user_ag.role != "NONE" or user_ag.status != "INVITED":
        flash(f'This invitartion is invalid', 'error')
        return redirect(url_for('index'))
    user_ag.status = "DECLINED"
    db.session.add(user_ag)
    db.session.commit()
    flash(f'You successfully declined the invitation to {ag.display_name}', 'success')
    return redirect(url_for('index'))

@bp.route('invitation/<ag_name>/cancell/<user_id>')
@requires_auth()
@requires_member_association()
def cancell_invitation(ag_name, user_id, ag, user_ag):
    remove_user_ag = db.session.query(UserAG).filter(and_(UserAG.user_id==user_id,UserAG.ag_id==ag.id)).one()
    print(vars(remove_user_ag))
    if remove_user_ag.role != "NONE" or remove_user_ag.status != "INVITED":
        flash(f'You cannot cancell an invitation for an actual member', 'error')
        return redirect(url_for('ag.ag_dashboard', ag_name=ag_name))
    db.session.delete(remove_user_ag)
    db.session.commit()
    flash(f'You have successfully revoked the invitation for the user {remove_user_ag.user_id} for the AG {ag.display_name}', 'success')
    return redirect(url_for('ag.ag_dashboard', ag_name=ag_name))

@bp.route('<ag_name>/submit_setting', methods=["GET"])
@requires_auth()
@requires_mentor()
def update_users(ag_name, user_ag, ag):
    for user_id in request.values:
        role = request.values.get(user_id)
        if role == "MENTOR":
            for user_id in request.values:
                role = request.values.get(user_id)
                edit_user_ag = db.session.query(UserAG).filter(and_(UserAG.user_id==user_id,UserAG.ag_id==ag.id)).one()
                edit_user_ag.role = role
                db.session.flush()
            db.session.commit()
            flash(f'Successfully changed the roles in {ag.display_name}', 'success')
            return redirect(url_for('ag.ag_dashboard', ag_name=ag_name))
    flash(u'An AG needs a minimum of one Mentor', 'error')
    return redirect(url_for('ag.ag_settings', ag_name=ag_name))

@bp.route('<ag_name>/apply')
@requires_auth()
@requires_gracefully_not_member()
def apply_ag(ag_name, ag):
    user_ag = db.session.query(UserAG).filter_by(user_id=g.session.user_id, ag_id=ag.id, role="NONE").filter(or_(UserAG.status=="LEFT", UserAG.status == "DECLINED")).scalar()
    if user_ag is None:
        user_ag = UserAG()
        user_ag.user_id = g.user.id
        user_ag.ag_id = ag.id
    user_ag.role = "NONE"
    user_ag.status = "APPLIED"
    db.session.add(user_ag)
    db.session.commit()
    flash(f'You successfully applied to the AG {ag.display_name}')
    return redirect(url_for('ag.discover'))

@bp.route('<ag_name>/cancell_application')
@requires_auth()
@requires_member_association()
def cancell_application(ag_name, ag, user_ag):
    print(user_ag.role)
    if(user_ag.role != "NONE" or user_ag.status != "APPLIED"):
        flash(f'You cannot cancell a application of an actual membership to the AG {ag.display_name}')
        return redirect(url_for('ag.discover'))
    db.session.delete(user_ag)
    db.session.commit()
    flash(f'You successfully cancelled your application to the AG {ag.display_name}')
    return redirect(url_for('ag.discover'))

@bp.route('<ag_name>/application/<username>/accept')
@requires_auth()
@requires_mentor()
def accept_application(ag_name, username, ag, user_ag):
    user = get_user_by_username(username)
    applied_user_ag = get_membership(ag_id=ag.id, user_id=user.id)
    if applied_user_ag is not None and applied_user_ag.role == "NONE" and applied_user_ag.status == "APPLIED":
        applied_user_ag.role = "PARTICIPANT"
        applied_user_ag.status = "ACTIVE"
        db.session.add(applied_user_ag)
        db.session.commit()
        flash(f'You successfully accepted the application of {user.username}', 'success')
        return redirect(url_for('ag.ag_dashboard', ag_name=ag.name))
    flash(f'The applicatin of {user.username} was not valid', 'error')
    return redirect(url_for('ag.ag_dashboard', ag_name=ag.name))

@bp.route('<ag_name>/application/<username>/reject')
@requires_auth()
@requires_mentor()
def reject_application(ag_name, username, ag, user_ag):
    user = get_user_by_username(username)
    applied_user_ag = get_membership(ag_id=ag.id, user_id=user.id)
    if applied_user_ag.role == "NONE" and applied_user_ag.status == "APPLIED":
        applied_user_ag.role = "NONE"
        applied_user_ag.status = "REJECTED"
        db.session.add(applied_user_ag)
        db.session.commit()
        flash(f'You successfully rejected the application of {user.username}', 'success')
        return redirect(url_for('ag.ag_dashboard', ag_name=ag.name))
    flash(f'The applicatin of {user.username} was not valid', 'error')
    return redirect(url_for('ag.ag_dashboard', ag_name=ag.name))

@bp.route('<ag_name>/leave')
@requires_auth()
@requires_member_association()
def leave_ag(ag_name, ag, user_ag):
    if(user_ag.role == "NONE"):
        flash('You cannot leave an AG you are not in', 'error')
        return redirect(url_for('ag.ag_dashboard', ag_name=ag_name))
    user_ag.role = "NONE"
    user_ag.status = "LEFT"
    db.session.flush()
    if(len(ag.actual_users) == 0):
        db.session.delete(ag)
        db.session.flush()
        flash(f'You sucessfully left and deleted the AG {ag.name}', 'success')
    elif(len(ag.mentors) == 0):
        flash(f'You cannot leave an AG, when there is no Mentor left afterwards', 'error')
        return redirect(url_for('ag.ag_dashboard', ag_name=ag_name))
    else:
        user_ag.role = "NONE"
        user_ag.status = "LEFT"
        db.session.flush()
        flash(f'You sucessfully left the AG {ag.name}', 'success')
    db.session.commit()
    return redirect(url_for('index'))
