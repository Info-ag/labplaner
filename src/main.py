#!/usr/bin/env python

#pylint: disable-all
from route import FlaskSites, APP


class DoodleFramework(FlaskSites):

    def __init__(self):
        super(DoodleFramework, self).__init__()



if __name__ == '__main__':
    DF = DoodleFramework()
    APP.run(host='127.0.0.1', port=5000, debug=True)
