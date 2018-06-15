'''
main app module
'''

import os
from flask import Flask, render_template, request, g
from flask_marshmallow import Marshmallow
from werkzeug.exceptions import NotFound

#declares the Flask app
app = Flask(__name__)

#imports all models used in this file

#load the config file set by the environment variable 'LAB_CONFIG'.
# If it isn't set 'config/dev.cfg' is used as default
config = os.environ.get('LAB_CONFIG', default='config/dev.cfg')
#imports the settings from the vonfig file
app.config.from_pyfile(os.path.abspath(config))
#set the secret key of the app used for ???
app.secret_key = app.secret_key.encode()
#initiates the marhmallow instance for this app
ma = Marshmallow(app)

from app.models.user import Session, User
from app.models.ag import AG, AGSchema
from app.models.associations import UserAG
#imports all utilities used in this file
from app.utils import after_this_request, requires_auth


#import all blueprints of this app
from app.blueprints.api import v1
from app.blueprints.api.v1 import user
from app.blueprints.api.v1 import ag as ag_api
from app.blueprints.api.v1 import event as event_api
from app.blueprints.api.v1 import date as date_api
from app.blueprints import auth
from app.blueprints import ag
from app.blueprints import cal
from app.blueprints import pizza

#import the database instance from __init__.py in app/
from app.models import db

#import the mail instance
from app.mail import mail

#initiate the database and create all database if not already happened at an earlier execution
db.init_app(app)
db.create_all(app=app)

#initiate the mail instance
mail.init_app(app)

#declares the errorhandler, if the route has not been found in the blueprints
@app.errorhandler(404)
def not_found(error):
    print(error)
    return NotFound()


@app.after_request
def call_after_request_callbacks(response):
    for callback in getattr(g, 'after_request_callbacks', ()):
        callback(response)
    return response


#let this function get executed before every request
@app.before_request
def auth_middleware():
    #loads the sessionid from the cookie. If it isn't set is got the default value ''
    sid = request.cookies.get('sid', default='')
    #checks if the sessionid-cookie was set
    if sid:
        #if the sessionid-cookie was set: call a function to see whether the session is valid
        session_result = Session.verify(sid)
        if session_result:
            #if so, set the session as global flask variable for this request
            g.session = session_result
        else:
            #if not, generate a new session and set it as global flask variable for this request
            _session = Session()
            db.session.add(_session)
            db.session.commit()
            g.session = _session
    else:
        #if there was no sessionid-cookie,
        # generate a new session and set is as global flask variable for this request
        _session = Session()
        db.session.add(_session)
        db.session.commit()
        g.session = _session

    #if the session is a valid session for a real user,
    # get the user and set it as global flask variable for this request
    if g.session.authenticated:
        g.user = User.query.get(g.session.user_id)

    #execute this function after the request
    @after_this_request
    def set_cookie(response):
        if g.session.session_only:
            #if the user choose not to remember him,
            # set a sessionid-cookie, that will expire if the brwoser got closed
            response.set_cookie('sid', g.session.get_string_cookie(),
                                httponly=True)
        else:
            #if the user choose to remember him,
            # set a sessionid-cookie, that will expire 60 days after creating the cookie
            response.set_cookie('sid', g.session.get_string_cookie(),
                                httponly=True, expires=g.session.expires)



#register all imported blueprints with a unique url_prefix

app.register_blueprint(v1.bp, url_prefix='/api/v1')
app.register_blueprint(user.bp, url_prefix='/api/v1/user')
app.register_blueprint(ag_api.bp, url_prefix='/api/v1/ag')
app.register_blueprint(event_api.bp, url_prefix='/api/v1/event')
app.register_blueprint(date_api.bp, url_prefix='/api/v1/date')
app.register_blueprint(auth.bp, url_prefix='/auth')
app.register_blueprint(ag.bp, url_prefix='/ag')
app.register_blueprint(cal.bp, url_prefix='/cal')
app.register_blueprint(pizza.bp, url_prefix='/pizza')


#declare a root route
@app.route('/')
#check if the user is authenticated/logined before handling the request
@requires_auth()
def index():
    #load all ags the User is in
    ags = db.session.query(AG).join(UserAG).filter(UserAG.user_id == g.session.user_id)
    #declare the marshmallow schema for ags
    ags_schema = AGSchema(many=True)
    #send the template top the user
    return render_template('index.html', title='Dashboard', ags=ags_schema.dump(ags))
