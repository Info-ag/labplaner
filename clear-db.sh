#!/bin/bash

rm -r migrations
rm -r app.db
rm -r src/app.db


FLASK_APP=src/app.py python3 -m flask db init
FLASK_APP=src/app.py python3 -m flask db merge -m "init"
FLASK_APP=src/app.py python3 -m flask db upgrade
