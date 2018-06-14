from flask import url_for
from flask_mail import Mail, Message

from app.models.user import User

mail = Mail()


def confirmation_mail(user: User):
    message = Message(subject='Confirm your E-Mail',
                      body=url_for('auth.confirm', token=user.confirmation_token)
                      )
    message.add_recipient(user.email)
    mail.send(message)
