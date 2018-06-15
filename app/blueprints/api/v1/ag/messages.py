'''
All blueprint routes regarding interacting with ag messages
'''

import re
from flask import Blueprint, request, url_for, flash, redirect
from werkzeug.exceptions import PreconditionFailed

from app.models import db

from app.models.ag import AGMessage
from app.models.associations import UserAGMessage

from app.utils import requires_auth
from app.utils.assocations import requires_mentor

import app.mail as mail

from config.regex import MessageRegex



bp = Blueprint('ag_messages_api', __name__)




@bp.route('<ag_name>/messages/write', methods=['POST'])
@requires_auth()
@requires_mentor()
def write_message(ag_name, ag, user_ag):
    subject = request.values.get('subject')
    message = request.values.get('message')
    email = request.values.get('email')
    if subject is None and not bool(re.match(MessageRegex.subject, subject)):
        return PreconditionFailed(description='subject')
    if message is None and not bool(re.match(MessageRegex.message, message)):
        return PreconditionFailed(description='message')
    new_message = AGMessage()
    new_message.subject = subject
    new_message.message = message
    new_message.ag_id = ag.id
    db.session.add(new_message)
    db.session.flush()
    for user in ag.actual_users:
        new_assoc = UserAGMessage()
        new_assoc.user_id = user.id
        new_assoc.message_id = new_message.id
        new_assoc.read = False
        db.session.add(new_assoc)
    if email is not None:
        mail.ag_mail(agmessage=new_message, ag=ag)
    db.session.commit()
    flash('Successfully send message', 'success')
    return redirect(url_for('ag.ag_dashboard', ag_name=ag_name))
