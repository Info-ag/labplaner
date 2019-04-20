'''
All blueprint routes regarding interacting with applications to an ag
'''
from sqlalchemy import or_
from flask import Blueprint, g, redirect, url_for, flash

from app.models import db
from app.models.associations import UserAG
from app.util import requires_auth
from app.util.assocations import requires_gracefully_not_member, requires_member_association, requires_mentor, get_membership
from app.util.user import get_user_by_username

bp = Blueprint('ag_applications_api', __name__)


@bp.route('<ag_name>/apply')
# check that the requester is authenticated/logined
@requires_auth()
# check that the requester is not an actual user of the ag
# and that he has no association
# or left the ag or declined a invitation
# adds the ag entry of the ag to the params/kwargs
@requires_gracefully_not_member()
def apply_ag(ag_name, ag):
    '''
    applies to a specified ag

    :param ag_name: AG name for the ag to be applied at

    automatic filled params

        :param ag: database entry of the ag
            --> get filled by @requires_gracefully_not_member

    :return: redirect to the discover site
    '''
    # query the association bewteen the requester and the ag
    user_ag = db.session.query(UserAG).filter_by(user_id=g.session.user_id, ag_id=ag.id,\
        role='NONE').filter(or_(UserAG.status == 'LEFT', UserAG.status == 'DECLINED')).scalar()
    # if there is no association
    if user_ag is None:
        #create one
        user_ag = UserAG()
        user_ag.user_id = g.user.id
        user_ag.ag_id = ag.id
    # anyways: change the association to applied status
    user_ag.role = 'NONE'
    user_ag.status = 'APPLIED'
    # add or update it and save the changes
    db.session.add(user_ag)
    db.session.commit()
    # return with a success message to the discover site
    flash(f'You successfully applied to the AG {ag.display_name}')
    return redirect(url_for('ag.discover'))

@bp.route('<ag_name>/cancell_application')
# check that the requester is authenticated/logined
@requires_auth()
# check that the requester has an association to the ag
# adds the ag and association entry to the params/kwargs
@requires_member_association()
def cancell_application(ag_name, ag, user_ag):
    '''
    cancells an application to an ag

    :param ag_name: AG name for the ag to be applied at

    automatic filled params

        :param ag: database entry of the ag
            --> get filled by @requires_member_association
        param user_ag: database entry of the user_ag association
            --> get filled by @requires_member_association


    :return: redirect to the discover site
    '''
    # if the association is not a applying relation
    if(user_ag.role != 'NONE' or user_ag.status != 'APPLIED'):
        # return with a error_message to the discover site
        flash(f'You cannot cancell an application of an actual membership of {ag.display_name}')
        return redirect(url_for('ag.discover'))
    # delete the entry
    db.session.delete(user_ag)
    # save the changes to the database
    db.session.commit()
    # return with a success message to the discover site
    flash(f'You successfully cancelled your application to the AG {ag.display_name}')
    return redirect(url_for('ag.discover'))

@bp.route('<ag_name>/application/<username>/accept')
# check that the requester is authenticated/logined
@requires_auth()
# check that the requester is a mentor of the ag
# add the user_ag association and the ag to the params/kwargs
@requires_mentor()
def accept_application(ag_name, username, ag, user_ag):
    '''
    accept the application of an user

    :param username: username of the username to be accepted
    :param ag_name: AG name for the ag to be applied at

    automatic filled params

        :param ag: database entry of the ag
            --> get filled by @requires_member_association
        param user_ag: database entry of the user_ag association
            --> get filled by @requires_member_association
    '''

    #queries the user and his association to the ag
    user = get_user_by_username(username)
    applied_user_ag = get_membership(ag_id=ag.id, user_id=user.id)
    # if the user really applied
    if applied_user_ag is not None and applied_user_ag.role == 'NONE' and\
        applied_user_ag.status == 'APPLIED':
        # update his entry to a actual user
        applied_user_ag.role = 'PARTICIPANT'
        applied_user_ag.status = 'ACTIVE'
        # save the changes
        db.session.add(applied_user_ag)
        db.session.commit()
        # return with a success message to the ag dashboard
        flash(f'You successfully accepted the application of {user.username}', 'success')
        return redirect(url_for('ag.ag_dashboard', ag_name=ag.name))
    # if the user did not really apply
    # return with a error message to the ag dashboard
    flash(f'The applicatin of {user.username} was not valid', 'error')
    return redirect(url_for('ag.ag_dashboard', ag_name=ag.name))

@bp.route('<ag_name>/application/<username>/reject')
# check that the requester is authenticated/logined
@requires_auth()
# check that the requester is a mentor of the ag
# add the user_ag association and the ag to the params/kwargs
@requires_mentor()
def reject_application(ag_name, username, ag, user_ag):
    '''
    reject the application of an user

    :param username: username of the username to be accepted
    :param ag_name: AG name for the ag to be applied at

    automatic filled params

        :param ag: database entry of the ag
            --> get filled by @requires_member_association
        param user_ag: database entry of the user_ag association
            --> get filled by @requires_member_association
    '''

    #queries the user and his association to the ag
    user = get_user_by_username(username)
    applied_user_ag = get_membership(ag_id=ag.id, user_id=user.id)

    # if the user really applied
    if applied_user_ag.role == 'NONE' and applied_user_ag.status == 'APPLIED':
        # update his entry to an rejected user
        applied_user_ag.role = 'NONE'
        applied_user_ag.status = 'REJECTED'
        # update the entry in the database
        db.session.add(applied_user_ag)
        # save the changes to the database
        db.session.commit()
        # return to the ag dhasboard with a success message
        flash(f'You successfully rejected the application of {user.username}', 'success')
        return redirect(url_for('ag.ag_dashboard', ag_name=ag.name))
    # if the user did not really applied
    # return to the ag dashboard with an error message
    flash(f'The applicatin of {user.username} was not valid', 'error')
    return redirect(url_for('ag.ag_dashboard', ag_name=ag.name))
