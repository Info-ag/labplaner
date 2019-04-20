'''
All Blueprint routes regarding rendering ag templates
'''

from flask import Blueprint, render_template
from app.models.ag import AG, AGSchema, AGSchemaIntern, AGMessageSchema
from app.models import db
from app.util import requires_auth
from app.util.assocations import requires_mentor, requires_membership, requires_ag_message_rights

from config.regex import AGRegex, MessageRegex

bp = Blueprint('ag', __name__)

ag_schema = AGSchema()
ag_schema_intern = AGSchemaIntern()
ags_schema = AGSchema(many=True)


@bp.route('/add', methods=['GET'])
@requires_auth()
def create_ag():
    return render_template('ag/add.html', title='Create AG',
                           ag_regex=AGRegex)


@bp.route('/<ag_name>', methods=['GET'])
@requires_auth()
@requires_membership()
def ag_dashboard(ag_name, ag, user_ag):
    schema = AGSchemaIntern()
    schema.context = {'ag_id': ag.id}
    return render_template('ag/dashboard.html', my_role=user_ag.role, ag=schema.dump(ag),\
                            title=ag.display_name)


@bp.route('/<ag_name>/invite', methods=['GET'])
@requires_auth()
@requires_mentor()
def invite_ag(ag_name, ag, user_ag):
    return render_template('ag/invite.html', ag=ag_schema_intern.dump(ag),\
                            title=f'Invite {ag.display_name}')


# Events

@bp.route('/<ag_name>/event/add', methods=['GET'])
@requires_auth()
@requires_mentor()
def create_event(ag_name, ag, user_ag):
    return render_template('ag/event/add.html', ag=ag_schema_intern.dump(ag),\
                            title=f'New Event {ag.display_name}')

@bp.route('/<ag_name>/settings', methods=['GET'])
@requires_auth()
@requires_mentor()
def ag_settings(ag_name, ag, user_ag):
    schema = AGSchemaIntern()
    schema.context = {'ag_id': ag.id}
    return render_template('ag/settings.html', title='Create AG', ag=schema.dump(ag))

@bp.route('/discover', methods=['GET'])
def discover():
    ags = db.session.query(AG).all()
    schema = AGSchema(many=True)
    return render_template('ag/discover.html', ags=schema.dump(ags))

@bp.route('<ag_name>/events/<event_name>/edit')
@requires_auth()
@requires_mentor()
def edit_event():
    pass

@bp.route('<ag_name>/messages/write', methods=['GET'])
@requires_auth()
@requires_mentor()
def write_message(ag_name, ag, user_ag):
    return render_template('ag/write_message.html', title=f'Write Message for {ag.display_name}',\
                            message_regex=MessageRegex, ag_name=ag_name)

@bp.route('<ag_name>/messages/view/<message_id>')
@requires_auth()
@requires_ag_message_rights()
def view_message(ag_name, message_id, ag, user_ag, ag_message, user_ag_message):
    message_schema = AGMessageSchema()
    user_ag_message.read = True
    db.session.add(user_ag_message)
    db.session.commit()
    return render_template('ag/view_message.html', title='View Message',\
                            message=message_schema.dump(ag_message), my_role=user_ag.role)
