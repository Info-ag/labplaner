'''
All blueprint routes regarding interacting with applications to an ag
'''
from sqlalchemy import or_
from flask import Blueprint, g, redirect, url_for, flash

from app.models import db
from app.models.associations import UserAG
from app.utils import requires_auth
from app.utils.assocations import requires_gracefully_not_member, requires_member_association, requires_mentor, get_membership
from app.utils.user import get_user_by_username

bp = Blueprint('ag_applications_api', __name__)


@bp.route('<ag_name>/apply')
@requires_auth()
@requires_gracefully_not_member()
def apply_ag(ag_name, ag):
    user_ag = db.session.query(UserAG).filter_by(user_id=g.session.user_id, ag_id=ag.id,\
        role='NONE').filter(or_(UserAG.status == 'LEFT', UserAG.status == 'DECLINED')).scalar()
    if user_ag is None:
        user_ag = UserAG()
        user_ag.user_id = g.user.id
        user_ag.ag_id = ag.id
    user_ag.role = 'NONE'
    user_ag.status = 'APPLIED'
    db.session.add(user_ag)
    db.session.commit()
    flash(f'You successfully applied to the AG {ag.display_name}')
    return redirect(url_for('ag.discover'))

@bp.route('<ag_name>/cancell_application')
@requires_auth()
@requires_member_association()
def cancell_application(ag_name, ag, user_ag):
    if(user_ag.role != 'NONE' or user_ag.status != 'APPLIED'):
        flash(f'You cannot cancell an application of an actual membership of {ag.display_name}')
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
    if applied_user_ag is not None and applied_user_ag.role == 'NONE' and\
        applied_user_ag.status == 'APPLIED':
        applied_user_ag.role = 'PARTICIPANT'
        applied_user_ag.status = 'ACTIVE'
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
    if applied_user_ag.role == 'NONE' and applied_user_ag.status == 'APPLIED':
        applied_user_ag.role = 'NONE'
        applied_user_ag.status = 'REJECTED'
        db.session.add(applied_user_ag)
        db.session.commit()
        flash(f'You successfully rejected the application of {user.username}', 'success')
        return redirect(url_for('ag.ag_dashboard', ag_name=ag.name))
    flash(f'The applicatin of {user.username} was not valid', 'error')
    return redirect(url_for('ag.ag_dashboard', ag_name=ag.name))
