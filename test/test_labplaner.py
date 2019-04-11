import sys
import os
import tempfile

import unittest

from app import create_app


class AppTest(unittest.TestCase):
    """Application Test super class

    This class can be used to test the application. It provides all the 
    necessary functions and fixtures for testing the flask application.

    Object elements:
        - app (Flask instance)
        - db (SQLAlchemy instance)
        - client (Flask test client instance)

    Methods:
        - login
        - logout
    """

    def setUp(self):
        """Setup fixture

        This method is called each time a test class is created. We use 
        it to setup the database, application and a test client.
        """
        self.app, self.db = create_app(os.path.dirname(sys.argv[0]), test=True)
        self._db_id, self._db_file = tempfile.mkstemp()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite://{self._db_file}'
        self.client = self.app.test_client()


    def login(self, username, password):
        """Login fixture
        """
        return self.client.post(app.url_for('auth.login'), data=dict(
                username=username,
                password=password,
            ), follows_redirect=True)


    def logout(self):
        """Logout fixture
        """
        return client.get('/logout', follows_redirect=True)

    def tearDown(self):
        """Tear down fixture

        This method is called at the end of each test. It is recommended
        to close all connections to the database and unlink the
        temporary file.
        """
        os.close(self._db_id)
        os.unlink(self._db_file)


class TestAuth(AppTest):
    """Authentication test

    Test the authentication procedure including:
        - sign up
        - login
        - logout
        - change password
    """

    TEST_EMAIL = 'test@labplaner.de'
    TEST_USERNAME = 'testuser'
    TEST_PASSWORD = 'testpasswod123'


    def test_login_username(self):
        """Test login using username
        """
        result = self.login(TEST_USERNAME, TEST_PASSWORD)
        self.assertEqual(result.get('status_code', 901), 200)


    def test_login_email(self):
        """Test login using email
        """
        result = self.login(TEST_EMAIL, TEST_PASSWORD)
        self.assertEqual(result.get('status_code', 901), 200)


class TestBasic(AppTest):
    """Test basic functionality of the application
    """

    def test_basic_index_endpoint(self):
        """Basic test of index endpoint

        Check if GET / returns 200
        """
        result = self.client.get('/', follow_redirects=True)
        self.assertEqual(result.get('status_code', 901), 200)


class TestPermission(AppTest):
    """Permission test

    Check if permissions are respected
    """
    pass