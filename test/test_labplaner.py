import sys
import os
import unittest

from app import create_app


class AppTest(unittest.TestCase):
    """Application Test class

    This class can be used to test the application. It provides all the 
    necessary functions and fixtures for testing the flask application.

    Object elements:
        - app (Flask instance)
        - db (SQLAlchemy instance)
        - client (Flask test client instance)

    Methods:
        - test_basic_index_endpoint
        - test_session
        - test_auth_register
        - test_auth_login
        - test_auth_logout
    """

    @classmethod
    def setUpClass(cls):
        """Setup class fixture

        This method is called each time a test class is created. We use 
        it to setup the database, application and a test client.
        """
        path = os.path.dirname(sys.argv[0])
        config = {
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        }
        cls.app, cls.db = create_app(path, test=True, **config)

    @classmethod
    def tearDownClass(cls):
        """Tear down class fixture

        This method is called at the end of each test class. If there is
        any connection that needs to be closed gracefully, this is the
        time to do so.
        """

        # Nothing to do
        pass

    def setUp(self):
        """Setup fixture

        Unlike setUpClass, this setup fixture is called each time a new
        test is run.
        """
        with self.app.app_context():
            self.db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        """Tear down fixture

        Similar to tearDownClass, this is where we can reset our
        application after tests. However, tearDown is run after each
        test unlike tearDownClass which is run at the end of a class.
        """
        with self.app.app_context():
            self.db.drop_all()

        # TODO clear session storage (redis)

        with self.client.session_transaction() as session:
            session = {}

    #########
    # Tests #
    #########

    def test_basic_index_endpoint(self):
        """Basic test of index endpoint

        Check if GET / returns 200
        """
        result = self.client.get('/', follow_redirects=True)
        self.assertEqual(result.status_code, 200)


    def test_session(self):
        """Simple session example

        This is how you can check for session functionality.
        """
        with self.client.session_transaction() as session:
            session['name'] = 'Name'

        with self.client.session_transaction() as session:
            self.assertEqual(session['name'], 'Name')
