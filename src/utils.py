from functools import wraps
from flask import g, request, redirect, url_for


def role_required(role="NONE"):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # TODO check if user has role
            return redirect(url_for('login', next=request.url))

        return decorated_function

    return decorator


def after_this_request(f):
    if not hasattr(g, 'after_request_callbacks'):
        g.after_request_callbacks = []
    g.after_request_callbacks.append(f)
    return f
