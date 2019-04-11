"""Models

This package contains all application models and schemes used for
database access and serialization.
We use SQLAlchemy and Marshmallow for our models and schemes.

Style guide:
    - Use plural form for database names (e.g. 'users', 'ags')
    - For relationships, use database names in alphabetical order,
    seperated by an underscore (e.g. 'ags_users', 'dates_events')
    - If possible use `id` for primary key
    - Use [table_name]_id for foreign keys, where table_name ist the
    singular form of the corresponding table (e.g. 'user_id', 'ag_id')

"""
from flask_sqlalchemy import SQLAlchemy

# App instance is set later in `app.create_app`
db = SQLAlchemy(session_options={"autoflush": False})
