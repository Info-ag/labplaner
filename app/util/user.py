'''
All utilities for the app regarding associations
'''

from app.models import db
from app.models.user import User


def get_user_by_username(username):
    user = db.session.query(User).filter_by(username=username).scalar()
    return user


def get_user_by_id(user_id):
    user = db.session.query(User).filter_by(id=user_id).scalar()
    return user
