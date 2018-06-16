'''
basic blueprint routes for interacting with an AG
'''
# import third party modules
import re
from flask import Blueprint, request, jsonify, g, url_for, flash, redirect
from sqlalchemy.sql import exists, and_
from werkzeug.exceptions import BadRequest, PreconditionFailed

# import database instance
from app.models import db

# import app with config etc.
from app import app

# import database models
from app.models.ag import AG, AGSchema, AGSchemaIntern
from app.models.associations import UserAG

# import utilities
from app.utils import requires_auth
from app.utils.assocations import requires_mentor, requires_member_association
from app.utils.ag import requires_ag
from app.utils.user import get_user_by_username

# import additional blueprints regarding applications, invitations and messages of ags
from app.blueprints.api.v1.ag import applications, invitations, messages

# import regex config for creating an ag
from config.regex import AGRegex

# declare the blueprint variable for this blueprint
bp = Blueprint('ag_api', __name__)

# register the additional blueprints
app.register_blueprint(invitations.bp, url_prefix='/invitations')
app.register_blueprint(applications.bp, url_prefix='/applications')
app.register_blueprint(messages.bp, url_prefix='/messages')

#declare the needed marshmallow schemas
ag_schema_intern = AGSchemaIntern()
ag_schema = AGSchema()
ags_schema = AGSchema(many=True)

@bp.route('/', methods=['POST'])
# check that the requester is authenticated/logined
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

    # read request values
    name = request.values.get('name')
    display_name = request.values.get('display_name')
    description = request.values.get('description')

    # check that the ag name and displayname is not used before and
    # check that the values match the regex pattern
    # if something isn't right return a error message
    if db.session.query(exists().where(AG.name == name)).scalar() or not bool(
            re.match(AGRegex.name, name)):
        return jsonify({'reason': 'name'}), 400
    if db.session.query(exists().where(AG.display_name == display_name)).scalar() or not bool(
            re.match(AGRegex.display_name, display_name)):
        return jsonify({'reason': 'display_name'}), 400
    if not bool(re.match(AGRegex.description, description)):
        return jsonify({'reason': 'description'}), 400

    # create a new database AG entry
    ag: AG = AG()
    ag.name = name
    ag.display_name = display_name
    ag.description = description
    ag.color = request.values.get('color', default='primary')

    # Add the AG entry to the DB to create a new id
    db.session.add(ag)
    db.session.flush()

    # Create the association entry to the creating user, so he is added as mentor
    user_ag = UserAG()
    user_ag.user_id = g.session.user_id
    user_ag.ag_id = ag.id
    user_ag.status = 'ACTIVE'
    user_ag.role = 'MENTOR'

    # add the association entry and save the database changes
    db.session.add(user_ag)
    db.session.commit()

    # return a success message
    return jsonify({'status': 'success', 'redirect': url_for('ag.invite_ag', ag_name=ag.name)}), 200


@bp.route('/id/<ag_id>', methods=['GET'])
# check that the requester is authenticated/logined
@requires_auth()
# check that the ag with the ag_id exist and add it to the params/kwargs
@requires_ag()
def get_ag_by_id(ag_id, ag):
    '''
    Query an AG specified by its id
    :param ag_id: A specific id
    :return: JSON representation of the AG
    '''
    # if the requester is a member of the ag --> return the schema for a member
    # else --> return the schema for a foreign
    if db.session.query(exists().where(UserAG.user_id == g.session.user_id and \
            UserAG.ag_id == ag_id)).scalar():
        return ag_schema_intern.jsonify(ag), 200
    else:
        return ag_schema.jsonify(ag), 200

@bp.route('/name/<ag_name>', methods=['GET'])
# check that the requester is authenticated/logined
@requires_auth()
# check that the ag with the ag_name exist and add it to the params/kwargs
@requires_ag()
def get_ag_by_name(ag_name, ag):
    '''
    Query an AG specified by its unique name
    :param name: A specific AG name
    :return: JSON representation of the AG
    '''

    # if the requester is a member of the ag --> return the schema for a member
    # else --> return the schema for a foreign
    if db.session.query(exists().where(UserAG.user_id == g.session.user_id and \
            UserAG.ag_id == ag.id)).scalar():
        return ag_schema_intern.jsonify(ag), 200
    else:
        return ag_schema.jsonify(ag), 200


@bp.route('/<ag_id>', methods=['PUT'])
# check that the requester is authenticated/logined
@requires_auth()
# check that the requester is a mentor of the ag
# add the user_ag association and the ag to the params/kwargs
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

    # read the request vaalues
    display_name = request.values.get('display_name', default=None)
    description = request.values.get('description', default=None)

    value_changed = False

    # checks if the display_name or description got transmitted
    # if so update the ag entry
    if display_name is not None and bool(re.match(AGRegex.display_name, display_name)):
        ag.display_name = display_name
        value_changed = True
    if description is not None and bool(re.match(AGRegex.description, description)):
        ag.description = description
        value_changed = True

    # if some value got changed, merge the entry to the database and return a success message
    if value_changed:
        db.session.merge(ag)
        db.session.commit()
        return jsonify({'status': 'success'}), 200
    # else return a BadRequest message
    else:
        return BadRequest()

@bp.route('/', methods=['GET'])
# check that the requester is authenticated/logined
@requires_auth()
def get_all_ags():
    '''
    Query up to 20 ags
    The request body may include the following:
        :key: count: Int with the count how much ags to return
            --> if greater than 20, it will be set to 20
            :default: 5
        :key: offset: Int how many entries to skip
            :default: 0
    :return: JSON Representation of the AGs
    '''
    # read request params and set default if not set
    count = request.args.get('count', default=5, type=int)
    offset = request.args.get('offset', default=0, type=int)
    # adjust to a max of 20
    if count > 20:
        count = 20
    # query all ags (with limit and offset)
    all_ags = AG.query.offset(offset).limit(count).all()
    # return a json representation
    return ags_schema.jsonify(all_ags)


@bp.route('<ag_name>/submit_setting', methods=['GET'])
# check that the requester is authenticated/logined
@requires_auth()
# check that the requester is a mentor of the ag
# add the user_ag association and the ag to the params/kwargs
@requires_mentor()
def update_users(ag_name, user_ag, ag):
    '''
        Update the roles of users in an ag
    The Request body includes following:
        :key: <user_id>: unique database id of the user
            --> :value: <role> --> 'MENTOR' or 'PARTICIPIANT'
    :param ag_name: ag_name of the ag to be edited

    automatic filled params

        :param user_ag: database entry of the association bewteen the request user and the ag
            --> get filled by @requires_mentor
        :param ag: database entry of the ag
            --> get filled by @requires_mentor

    :return: redirect to the ag dashboard
    '''
    # for every key in rquest values --> for every user/user_id passed by the form
    for user_id in request.values:
        # the role the user got assigned to be
        role = request.values.get(user_id)
        # query the database entry of the association between the user to be edited an the ag
        edit_user_ag = db.session.query(UserAG).filter(and_(UserAG.user_id == user_id,\
                        UserAG.ag_id == ag.id)).scalar()
        # if there is an result for this user <==> the user is in the ag
        if edit_user_ag:
            # update his role and simulate the changes
            edit_user_ag.role = role
            db.session.flush()
    # if there are no mentors left
    if not ag.mentors:
        # throw error
        flash(u'An AG needs a minimum of one Mentor', 'error')
        return redirect(url_for('ag.ag_settings', ag_name=ag_name))
    # if there are still mentors
    # --> save changes to the database and redirect to the ag dashboard
    db.session.commit()
    flash(f'Successfully changed the roles in {ag.display_name}', 'success')
    return redirect(url_for('ag.ag_dashboard', ag_name=ag_name))



@bp.route('<ag_name>/leave')
# check that the requester is authenticated/logined
@requires_auth()
# check if the requester has a association to the ag
# add the association and the ag to the params/kwargs
@requires_member_association()
def leave_ag(ag_name, ag, user_ag):
    '''
    leave the specified ag
    :param ag_name: name of the ag to leave

    automatic filled params

        :param user_ag: database entry of the association bewteen the request user and the ag
            --> get filled by @requires_member_association
        :param ag: database entry of the ag
            --> get filled by @requires_member_association

    :return: redirect to the dashboard

    '''

    # if the user is not a actual user of the ag
    # return a error message
    if user_ag.role == 'NONE':
        flash('You cannot leave an AG you are not in', 'error')
        return redirect(url_for('ag.ag_dashboard', ag_name=ag_name))
    # else: update the entry, so the user is no member anymore and left the ag
    user_ag.role = 'NONE'
    user_ag.status = 'LEFT'
    # simulate the changes
    db.session.flush()
    # if there are no members left in the ag
    if not ag.actual_users:
        # delete the ag
        db.session.delete(ag)
        db.session.flush()
        # save a success message
        flash(f'You sucessfully left and deleted the AG {ag.name}', 'success')
    # else if there are no mentors left, but still members
    elif not ag.mentors:
        # return a error message
        # dont save the changes to the database and return to the ag dashboard
        flash(f'You cannot leave an AG, when there is no Mentor left afterwards', 'error')
        return redirect(url_for('ag.ag_dashboard', ag_name=ag_name))
    # else
    else:
        # save a success message
        flash(f'You sucessfully left the AG {ag.name}', 'success')
    # save the cganges to the database and return with the saved success message to the dashboard
    db.session.commit()
    return redirect(url_for('index'))



@bp.route('<ag_name>/kick/<user_name>')
# check that the requester is authenticated/logined
@requires_auth()
# check
@requires_mentor()
# check that the requester is a mentor of the ag
# add the user_ag association and the ag to the params/kwargs
@requires_mentor()
def kick_user(ag_name, user_name, ag, user_ag):
    '''
    kick a user out of an ag

    :param ag_name: name of the ag to kick the user out
    :param user_name: username of the user to be kicked out

    automatic filled params

        :param user_ag: database entry of the association bewteen the request user and the ag
            --> get filled by @requires_member_association
        :param ag: database entry of the ag
            --> get filled by @requires_member_association

    :return: redirect to the dashboard
    '''

    # query the user and his associatin
    user = get_user_by_username(user_name)
    edit_user_ag = db.session.query(UserAG).filter_by(user_id=user.id, ag_id=ag.id).scalar()
    # if the user is not an actual user
    if edit_user_ag is None or edit_user_ag.role == 'NONE':
        # return to the ag dashboard with a error message
        flash(f'You cannot kick {user.username} from {ag.display_name}.')
        return redirect(url_for('ag.ag_dashboard', ag_name=ag_name))
    # else
    # change the association entry, so the user is not a member of the ag anymore
    # and his status is kicked
    edit_user_ag.role = 'NONE'
    edit_user_ag.status = 'KICKED'
    # simulate the changes
    db.session.flush()
    # if there are no members left
    if not ag.actual_users:
        # delete the ag and return to the dashboard
        db.session.delete(ag)
        db.session.commit()
        flash(f'You sucessfully left and deleted the AG {ag.display_name}', 'success')
        return redirect(url_for('index'))
    # else if there are no mentors left
    elif not ag.mentors:
        # save a error message
        flash(f'You cannot kick the last Mentor of {ag.display_name}', 'error')
    # else
    else:
        # save a success message and save the changes to the database
        flash(f'You sucessfully kicked {user.username} from the AG {ag.display_name}', 'success')
        db.session.commit()
    # return to the ag dashboard
    return redirect(url_for('ag.ag_dashboard', ag_name=ag_name))

@bp.route('<ag_name>/delete')
# check that the requester is authenticated/logined
@requires_auth()
# check that the requester is a mentor of the ag
# add the user_ag association and the ag to the params/kwargs
@requires_mentor()
def delete_ag(ag_name, ag, user_ag):
    '''
    delete an ag

    :param ag_name: name of the ag to be deleted

    automatic filled params

        :param user_ag: database entry of the association bewteen the request user and the ag
            --> get filled by @requires_member_association
        :param ag: database entry of the ag
            --> get filled by @requires_member_association

    :return: redirect to the dashboard
    '''
    # delete the ag
    db.session.delete(ag)
    # save the changes
    db.session.commit()
    # return to the dashboard with a success message
    flash(f'You successfully deleted the AG {ag.display_name}', 'success')
    return redirect(url_for('index'))
