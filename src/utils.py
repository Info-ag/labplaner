from functools import wraps

from flask import g
from werkzeug.exceptions import Unauthorized


def requires_auth():
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not g.session.authenticated:
                return Unauthorized()
            else:
                return f(*args, **kwargs)
        return wrapped
    return wrapper


def after_this_request(f):
    if not hasattr(g, 'after_request_callbacks'):
        g.after_request_callbacks = []
    g.after_request_callbacks.append(f)
    return f
