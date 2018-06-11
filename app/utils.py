from functools import wraps

from flask import g, redirect, url_for, request
from sqlalchemy import exists
from app import db
from app.models.ag import AG
from app.models.associations import UserAG

from werkzeug.exceptions import Unauthorized, NotFound


def requires_auth():
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not g.session.authenticated:
                return redirect(url_for('auth.login_get', next = request.url))
            else:
                return f(*args, **kwargs)
        return wrapped
    return wrapper


def after_this_request(f):
    if not hasattr(g, 'after_request_callbacks'):
        g.after_request_callbacks = []
    g.after_request_callbacks.append(f)
    return f

def requires_existing_ag():
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            ag_name = kwargs.get('ag_name', None)
            ag_id = kwargs.get('ag_id', None)
            if db.session.query(exists().where(AG.id == ag_id)).scalar() and ag_id is not None:
                ag: AG = AG.query.filter_by(id=ag_id).scalar()

            elif db.session.query(exists().where(AG.name == ag_name)).scalar() and ag_name is not None:
                ag: AG = AG.query.filter_by(name=ag_name).scalar()
            else:
                return NotFound(description='AG could not be found') 
            kwargs.setdefault('ag', ag)
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def requires_ag():
    def wrapper(f):
        @wraps(f)
        @requires_existing_ag()
        def wrapped(*args, **kwargs):
            ag_name = kwargs.get('ag_name', None)
            ag_id = kwargs.get('ag_id', None)
            if ag_id is not None:
                ag: AG = AG.query.filter_by(id=ag_id).scalar()
            elif ag_name is not None:
                ag: AG = AG.query.filter_by(name=ag_name).scalar()
            else:
                return NotFound(description='AG could not be found')
            kwargs.setdefault('ag', ag)
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def requires_member():
    def wrapper(f):
        @wraps(f)
        @requires_ag()
        def wrapped(*args, **kwargs):
            ag = kwargs.get('ag')
            if db.session.query(exists().where(UserAG.user_id == g.session.user_id and UserAG.ag_id == ag.id)).scalar():
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
            if(user_ag.role != 'NONE'):
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


