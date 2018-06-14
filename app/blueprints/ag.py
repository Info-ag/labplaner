from flask import Blueprint, g, redirect, render_template, url_for, flash
from sqlalchemy.sql import exists
from werkzeug.exceptions import NotFound, Unauthorized
from app.models.associations import UserAG
from app.models.ag import AG, AGSchema, AGSchemaIntern
from app.models import db
from app.utils import requires_auth, requires_mentor, requires_membership

from config.regex import AGRegex

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
    return render_template('ag/dashboard.html', my_role=user_ag.role, ag=schema.dump(ag),
                            title=ag.display_name)


@bp.route('/<ag_name>/invite', methods=['GET'])
@requires_auth()
@requires_mentor()
def invite_ag(ag_name, ag, user_ag):
    return render_template('ag/invite.html', ag=ag_schema_intern.dump(ag), title=f'Invite {ag.display_name}')


# Events

@bp.route('/<ag_name>/event/add', methods=['GET'])
@requires_auth()
@requires_mentor()
def create_event(ag_name, ag, user_ag):
    return render_template('ag/event/add.html', ag=ag_schema_intern.dump(ag), title=f'New Event {ag.display_name}')

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
    return render_template('ag/discover.html', ags=ags_schema.dump(ags))

@bp.route('<ag_name>/events/<event_name>/edit')
@requires_auth()
@requires_mentor()
def edit_event():
    pass