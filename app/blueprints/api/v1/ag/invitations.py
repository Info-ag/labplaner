'''
All blueprint routes regarding interacting with invitations to ags
'''
from flask import Blueprint, redirect, url_for, flash, jsonify, request
from sqlalchemy import exists, and_, or_

from app.models import db

from app.models.associations import UserAG
from app.models.user import User, UserSchema
from app.utils import requires_auth
from app.utils.assocations import requires_mentor, requires_member_association
from app.utils.ag import requires_ag



bp = Blueprint('ag_invitations_api', __name__)

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

            new_user_ag = db.session.query(UserAG).filter_by(user_id=user.id, ag_id=ag.id).scalar()
            if new_user_ag:
                if (new_user_ag.status == 'LEFT' or new_user_ag.status == 'REJECTED')\
                        and new_user_ag.role == 'NONE':
                    new_user_ag.role = 'NONE'
                    new_user_ag.status = 'INVITED'
                elif new_user_ag.status == 'APPLIED' and new_user_ag.role == 'NONE':
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


@bp.route('<ag_name>/user/inviteable', methods=['GET'])
@requires_auth()
@requires_ag()
def get_inviteable_user(ag_name, ag):
    query = request.values.get('query', default='')
    users = db.session.query(User).join(UserAG, and_(UserAG.ag_id == ag.id, UserAG.user_id == User.id), isouter = True).filter(or_((and_(UserAG.ag_id == None, User.username.like(f'%{query}%'))), (and_(UserAG.ag_id == ag.id, UserAG.role == 'NONE', or_(UserAG.status == 'LEFT', UserAG.status == 'REJECTED', UserAG.status == 'APPLIED'), User.username.like(f'%{query}%')))))
    users_schema = UserSchema(many=True)
    return users_schema.jsonify(users)

@bp.route('invitation/<ag_name>/accept')
@requires_auth()
@requires_member_association()
def accept_invitation(ag_name, ag, user_ag):
    if user_ag.role != 'NONE' or user_ag.status != 'INVITED':
        flash(f'This invitartion is invalid', 'error')
        return redirect(url_for('index'))
    user_ag.role = 'PARTICIPANT'
    user_ag.status = 'ACTIVE'
    db.session.add(user_ag)
    db.session.commit()
    flash(f'You successfully accepted the invitation to {ag.display_name}', 'success')
    return redirect(url_for('ag.ag_dashboard', ag_name=ag_name))

@bp.route('invitation/<ag_name>/decline')
@requires_auth()
@requires_member_association()
def decline_invitation(ag_name, ag, user_ag):
    if user_ag.role != 'NONE' or user_ag.status != 'INVITED':
        flash(f'This invitartion is invalid', 'error')
        return redirect(url_for('index'))
    user_ag.status = 'DECLINED'
    db.session.add(user_ag)
    db.session.commit()
    flash(f'You successfully declined the invitation to {ag.display_name}', 'success')
    return redirect(url_for('index'))

@bp.route('invitation/<ag_name>/cancell/<user_id>')
@requires_auth()
@requires_member_association()
def cancell_invitation(ag_name, user_id, ag, user_ag):
    remove_user_ag = db.session.query(UserAG)\
        .filter(and_(UserAG.user_id == user_id, UserAG.ag_id == ag.id)).one()
    if remove_user_ag.role != 'NONE' or remove_user_ag.status != 'INVITED':
        flash(f'You cannot cancell an invitation for an actual member', 'error')
        return redirect(url_for('ag.ag_dashboard', ag_name=ag_name))
    db.session.delete(remove_user_ag)
    db.session.commit()
    flash(f'You have successfully revoked the invitation for the user '\
        f'{remove_user_ag.user_id} for the AG {ag.display_name}', 'success')
    return redirect(url_for('ag.ag_dashboard', ag_name=ag_name))
