import sys
import os
import tempfile

import unittest

from app import create_app


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app, self.db = create_app(os.path.dirname(sys.argv[0]), test=True)
        self._db_id, self._db_file = tempfile.mkstemp()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite://{self._db_file}'
        self.client = self.app.test_client()


    def login(self, username, password):
        return self.client.post(app.url_for('auth.login'), data=dict(
                username=username,
                password=password,
            ), follows_redirect=True)

    def tearDown(self):
        os.close(self._db_id)
        os.unlink(self._db_file)


class TestBasic(AppTest):
    def test_basic_index_endpoint(self):
        rv = self.client.get('/')
        #print(rv.status_code)
        assert rv.status_code == 200