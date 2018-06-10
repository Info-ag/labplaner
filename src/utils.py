from functools import wraps

from flask import g, redirect, request, url_for
from werkzeug.exceptions import Unauthorized


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
