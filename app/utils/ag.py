'''
All utilities for the app regarding ags
'''

from functools import wraps

from sqlalchemy import exists
from werkzeug.exceptions import NotFound, BadRequest
from app.models import db
from app.models.ag import AG, AGMessage




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

def requires_ag_message():
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            message_id = kwargs.get('message_id')
            if message_id:
                ag_message = db.session.query(AGMessage).filter_by(id=message_id).scalar()
                if ag_message:
                    kwargs.setdefault('ag_message', ag_message)
                    return f(*args, **kwargs)
                else:
                    return NotFound(description='not able to locate any message with this id')
            else:
                return BadRequest(description='you have not specified any message id')

        return wrapped

    return wrapper


def get_ag_by_name(ag_name):
    ag = db.session.query(AG).filter_by(name=ag_name).scalar()
    return ag


def get_ag_by_id(ag_id):
    ag = db.session.query(AG).filter_by(id=ag_id).scalar()
    return ag
