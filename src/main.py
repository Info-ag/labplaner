#!/usr/bin/env python

# pylint: disable-all
from app import FlaskSites, app


class LabplanerFramework(FlaskSites):

    def __init__(self):
        super(LabplanerFramework, self).__init__()


if __name__ == '__main__':
    LF = LabplanerFramework()
    app.run(host='127.0.0.1', port=5000, debug=True)
