'''
All utilities for the app regarding associations
'''

from functools import wraps
from werkzeug.exceptions import Unauthorized, BadRequest, Forbidden

from flask import g
from sqlalchemy import exists, and_, or_
from app.models import db
from app.models.associations import UserAG, UserAGMessage

from app.util.ag import requires_ag, requires_ag_message



def requires_gracefully_not_member():
    def wrapper(f):
        @wraps(f)
        @requires_ag()
        def wrapped(*args, **kwargs):
            ag = kwargs.get('ag')
            if not db.session.query(exists().where(\
                    and_(UserAG.user_id == g.session.user_id, UserAG.ag_id == ag.id))).scalar() or db.session.query(\
                    exists().where(\
                            and_(UserAG.user_id == g.session.user_id, UserAG.ag_id == ag.id, UserAG.role == 'NONE',\
                                 or_(UserAG.status == 'LEFT', UserAG.status == 'DECLINED')))).scalar():
                return f(*args, **kwargs)
            else:
                return BadRequest(description='you already have some kind of relation to this AG')

        return wrapped

    return wrapper


def requires_not_member():
    def wrapper(f):
        @wraps(f)
        @requires_ag()
        def wrapped(*args, **kwargs):
            ag = kwargs.get('ag')
            if not db.session.query(
                    exists().where(and_(UserAG.user_id == g.session.user_id, UserAG.ag_id == ag.id))).scalar():
                return f(*args, **kwargs)
            else:
                return BadRequest(description='you already have some kind of relation to this AG')

        return wrapped

    return wrapper


def requires_member():
    def wrapper(f):
        @wraps(f)
        @requires_ag()
        def wrapped(*args, **kwargs):
            ag = kwargs.get('ag')
            if db.session.query(
                    exists().where(and_(UserAG.user_id == g.session.user_id, UserAG.ag_id == ag.id))).scalar():
                return f(*args, **kwargs)
            else:
                return Unauthorized()

        return wrapped

    return wrapper


def requires_member_association():
    def wrapper(f):
        @wraps(f)
        @requires_member()
        def wrapped(*args, **kwargs):
            ag = kwargs.get('ag')
            user_ag = UserAG.query.filter_by(user_id=g.session.user_id, ag_id=ag.id).scalar()
            kwargs.setdefault('user_ag', user_ag)
            return f(*args, **kwargs)

        return wrapped

    return wrapper


def requires_membership():
    def wrapper(f):
        @wraps(f)
        @requires_member()
        def wrapped(*args, **kwargs):
            ag = kwargs.get('ag')
            user_ag = UserAG.query.filter_by(user_id=g.session.user_id, ag_id=ag.id).scalar()
            if user_ag.role != 'NONE':
                kwargs.setdefault('user_ag', user_ag)
                return f(*args, **kwargs)
            else:
                return Unauthorized()

        return wrapped

    return wrapper


def requires_mentor():
    def wrapper(f):
        @wraps(f)
        @requires_membership()
        def wrapped(*args, **kwargs):
            user_ag = kwargs.get('user_ag')
            if user_ag.role == 'MENTOR':
                return f(*args, **kwargs)
            else:
                return Unauthorized(description='you need to be mentor')

        return wrapped

    return wrapper

def requires_ag_message_rights():
    def wrapper(f):
        @wraps(f)
        @requires_membership()
        @requires_ag_message()
        def wrapped(*args, **kwargs):
            ag_message = kwargs.get('ag_message')
            user_ag_message = db.session.query(UserAGMessage).filter_by(message_id=ag_message.id, user_id=g.session.user_id).scalar()
            if user_ag_message:
                kwargs.setdefault('user_ag_message', user_ag_message)
                return f(*args, **kwargs)
            else:
                return Forbidden('you have no rights to read this message')

        return wrapped

    return wrapper

def get_membership(user_id, ag_id):
    user_ag = UserAG.query.filter_by(user_id=user_id, ag_id=ag_id).scalar()
    return user_ag
