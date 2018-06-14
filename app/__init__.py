import os
from flask import Flask, render_template, request, g
from flask_marshmallow import Marshmallow
from werkzeug.exceptions import NotFound

app = Flask(__name__)

config = os.environ.get('LAB_CONFIG', default='config/dev.cfg')
app.config.from_pyfile(os.path.abspath(config))
app.secret_key = app.secret_key.encode()
ma = Marshmallow(app)

from app.models.user import Session, User
from app.utils import after_this_request, requires_auth

from app.blueprints.api import v1
from app.blueprints.api.v1 import user
from app.blueprints.api.v1 import ag as ag_api
from app.blueprints.api.v1 import event as event_api
from app.blueprints.api.v1 import date as date_api
from app.blueprints import auth
from app.blueprints import ag
from app.blueprints import cal
from app.blueprints import pizza

from app.models import db

db.init_app(app)
db.create_all(app=app)

@app.errorhandler(404)
def not_found(error):
    return NotFound()


@app.after_request
def call_after_request_callbacks(response):
    for callback in getattr(g, 'after_request_callbacks', ()):
        callback(response)
    return response


@app.before_request
def auth_middleware():
    sid = request.cookies.get('sid', default='')
    if sid:
        session_result = Session.verify(sid)
        if session_result:
            g.session = session_result
        else:
            _session = Session()
            db.session.add(_session)
            db.session.commit()
            g.session = _session
    else:
        _session = Session()
        db.session.add(_session)
        db.session.commit()
        g.session = _session

    if g.session.authenticated:
        g.user = User.query.get(g.session.user_id)

    @after_this_request
    def set_cookie(response):
        if g.session.session_only:
            response.set_cookie('sid', g.session.get_string_cookie(),
                                httponly=True)
        else:
            response.set_cookie('sid', g.session.get_string_cookie(),
                                httponly=True, expires=g.session.expires)



app.register_blueprint(v1.bp, url_prefix='/api/v1')
app.register_blueprint(user.bp, url_prefix='/api/v1/user')
app.register_blueprint(ag_api.bp, url_prefix='/api/v1/ag')
app.register_blueprint(event_api.bp, url_prefix='/api/v1/event')
app.register_blueprint(date_api.bp, url_prefix='/api/v1/date')
app.register_blueprint(auth.bp, url_prefix='/auth')
app.register_blueprint(ag.bp, url_prefix='/ag')
app.register_blueprint(cal.bp, url_prefix='/cal')
app.register_blueprint(pizza.bp, url_prefix='/pizza')


@app.route('/')
@requires_auth()
def index():
    return render_template('index.html', title='Dashboard')
