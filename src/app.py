import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from flask import render_template, request, redirect, url_for, flash, g

app = Flask(__name__)
app.config.from_json(os.path.join(os.getcwd(), os.environ["CONFIG"]))
app.secret_key = app.secret_key.encode()
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

from models.user import Session, User

db.create_all()

from blueprints.api.v1 import api
from blueprints.api.v1 import user
from blueprints.api.v1 import ag as ag_api
from blueprints.api.v1 import event as event_api
from blueprints.api.v1 import date as date_api
from blueprints import auth
from blueprints import ag
from blueprints import cal
import utils


@app.after_request
def call_after_request_callbacks(response):
    for callback in getattr(g, 'after_request_callbacks', ()):
        callback(response)
    return response


@app.before_request
def auth_middleware():
    sid = request.cookies.get("sid", default="")
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

    @utils.after_this_request
    def set_cookie(response):
        response.set_cookie("sid", g.session.get_string_cookie(),
                            httponly=True, expires=g.session.expires)


app.register_blueprint(api.bp, url_prefix="/api/v1")
app.register_blueprint(user.bp, url_prefix="/api/v1/user")
app.register_blueprint(ag_api.bp, url_prefix="/api/v1/ag")
app.register_blueprint(event_api.bp, url_prefix="/api/v1/event")
app.register_blueprint(date_api.bp, url_prefix="/api/v1/date")
app.register_blueprint(auth.bp, url_prefix="/auth")
app.register_blueprint(ag.bp, url_prefix="/ag")
app.register_blueprint(cal.bp, url_prefix="/cal")


@app.route('/')
def index():
    if not g.session.authenticated:
        flash(u'You need to be logged in', 'error')
        return redirect(url_for("auth.login_get"))

    return render_template('index.html', title="Dashboard")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
