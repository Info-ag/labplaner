"""Models

This package contains all application models and schemes used for
database access and serialization.
We use SQLAlchemy and Marshmallow for our models and schemes.
"""
from flask_sqlalchemy import SQLAlchemy

# App instance is set later in `app.create_app`
db = SQLAlchemy(session_options={"autoflush": False})
