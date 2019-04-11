import os
import warnings

warnings.filterwarnings('ignore', message='greenlet.greenlet size changed')
# Huey uses greenlets and might produce annoying warnings

from flask import Flask, request, g, redirect, url_for

import config


def create_app(root_path, minimal=False, test=False):
    """Create new app instance

    :param root_path: absolute path to the project root directory 
    that contains the `app` directory
    :param minimal: if set to `True`, the generated app instance will 
    only include the bare minimum. This is meant to increase 
    performance as new instance is required for each task.
    :param test: if set to `True`, all necessary configurations will be
    applied for testing the application. You might want to change the
    database by your self:
        db_id, db_file = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://' + db_file
        # close database after test
        os.close(db_id)
        os.unlink(db_file)

    :return (app, db): Tuple, Flask and SQAlchemy instances
    """

    app_name = 'minimal_app' if minimal else __name__
    app: Flask = Flask(app_name, root_path=root_path)

    # Load configuration files from enviroment variables
    base = os.environ.get('BASE_CONFIG', default=config.BASE_CONFIG)
    env = os.environ.get('ENV', default='development').lower()
    secret = os.environ.get('SECRET', default=config.SECRET_CONFIG)
    default_config = config.DEV_CONFIG 
    if env == 'production':
        default_config = config.PROD_CONFIG
    
    config_file = os.environ.get('CONFIG', default=default_config)
    if test:
        config_file = os.environ.get('TEST_CONFIG', default=config.TEST_CONFIG)

    app.config.from_pyfile(os.path.abspath(base))
    app.config.from_pyfile(os.path.abspath(config_file))
    if os.path.exists(secret):
        app.config.from_pyfile(os.path.abspath(secret))

    # String needs to be encoded
    app.secret_key = app.secret_key.encode()

    # Might be redundant, but important for tasks
    app.static_url_path = app.config.get('STATIC_FOLDER')
    app.static_folder = os.path.join(app.root_path, app.static_url_path)
    app.template_folder = os.path.join(app.root_path, app.config['TEMPLATE_FOLDER']) 

    
    # Import Database
    #from app.models.user import Session, User
    #from app.models.ag import AG
    """from app.models.relationships import (
        UserAG, 
        EventDate, 
        UserDate, 
        UserAGMessage
    )"""
    from app.models import db

    db.init_app(app)

    if not minimal:
        # Add additional modules
        #from app.blueprints.api import v1
        #from app.blueprints.api.v1 import user as user_api_1
        #from app.blueprints.api.v1 import ag as ag_api_1
        #from app.blueprints.api.v1 import event as event_api_1
        #from app.blueprints.api.v1 import date as date_api_1
        #from app.blueprints import auth
        #from app.blueprints import ag
        #from app.blueprints import cal
        from app.i18n import babel
        #from app.models import ma
        #from app import util

        babel.init_app(app)
        # moment.init_app(app)
        # Create database models. This is only called in a non minimal 
        # app insance as it is the one with the first database 
        # interactions
        db.create_all(app=app)

        @app.after_request
        def call_after_request_callbacks(response):
            """Helper for callbacks after request

            Some operations (such as setting cookies) need to be 
            performed at the end of a request when the `response` is 
            already initialized.

            Actions that need to be performed at the end of a request 
            need be appended to `g.after_request_callbacks`
            :param: `response` the response instance
            """
            for callback in getattr(g, 'after_request_callbacks', ()):
                callback(response)
            return response

        @app.before_request
        def auth_middleware():
            """Authenticate user

            TODO: use flask_session and redis
            Authenticate user and set unique session cookie.
            """
            pass

        @babel.localeselector
        def get_locale():
            """Locale configuration

            This function is required by babel and specifies the locale 
            for the current request.
            :return: Locale setting for current request
            """
            return request.accept_languages.best_match(['de', 'en'])

        ##############
        # API routes #
        ##############
        """api_v1_prefix = '/api/v1%s'
        app.register_blueprint(v1.bp,
                               url_prefix=api_v1_prefix % '')
        app.register_blueprint(user_api_1.bp, 
                               url_prefix=api_v1_prefix % '/user')
        app.register_blueprint(ag_api_1.bp,
                               url_prefix=api_v1_prefix % '/ag')
        app.register_blueprint(event_api_1.bp,
                               url_prefix=api_v1_prefix % '/event')
        """
        ############
        # Frontend #
        ############
        #app.register_blueprint(auth.bp, url_prefix='/auth')
        #app.register_blueprint(ag.bp, url_prefix='/ag')
        #app.register_blueprint(cal.bp, url_prefix='/cal')
        #app.register_blueprint(pizza.bp, url_prefix='/pizza')

    return app, db