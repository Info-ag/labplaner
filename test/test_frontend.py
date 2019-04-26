import sys
import os
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from app import create_app


class SeleniumAppTest(unittest.TestCase):
    """Frontend Test class

    Using selenium, we test the frontend behaviour of our application

    Object elements:
        - app (Flask instance)
        - db (SQLAlchemy instance)
        - client (Flask test client instance)
        - driver_firefox (Selenium webdriver)

    Methods:
        - test_basic_index_endpoint
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
        
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.cache.disk.enable", False)
        profile.set_preference("browser.cache.memory.enable", False)
        profile.set_preference("browser.cache.offline.enable", False)
        profile.set_preference("network.http.use-cache", False) 
        cls.driver_firefox = webdriver.Firefox(profile)


    @classmethod
    def tearDownClass(cls):
        """Tear down class fixture

        This method is called at the end of each test class. If there is
        any connection that needs to be closed gracefully, this is the
        time to do so.
        """

        # Nothing to do
        cls.driver_firefox.close()

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
