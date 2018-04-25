# pylint: disable-all
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from flask import render_template, \
    request, \
    g

import dbconfig

app = Flask(__name__)
app.config.from_object(dbconfig.DBConfig)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

from models.user import Session

db.create_all()

from blueprints.api.v1 import user
from blueprints import auth
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

    @utils.after_this_request
    def set_cookie(response):
        response.set_cookie("sid", g.session.get_string_cookie(),
                            httponly=True, expires=g.session.expires)


app.register_blueprint(user.bp, url_prefix="/api/v1/user")
app.register_blueprint(auth.bp, url_prefix="/auth")


@app.route('/')
def index(text=''):
    return render_template('index.html', message=text)


if __name__ == '__main__':
    app.config.update(
        DEBUG=True,
        TESTING=True,
        TEMPLATES_AUTO_RELOAD=True
    )
    app.run(host='127.0.0.1', port=5000, debug=True)
