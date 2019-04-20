'''
module for writing mails
'''
from flask import url_for
from flask_mail import Mail, Message

from app.models.user import User
from app.models.ag import AGMessage, AG

mail = Mail()


def confirmation_mail(user: User):
    message = Message(subject='Confirm your E-Mail',
                      body=url_for('auth.confirm',
                                   token=user.confirmation_token))
    message.add_recipient(user.email)
    mail.send(message)


def ag_mail(agmessage: AGMessage, ag: AG):
    message = Message(subject=agmessage.subject, body=agmessage.message)
    for user in ag.actual_users:
        if user.email_confirmed:
            message.add_recipient(user.email)
    mail.send(message)
