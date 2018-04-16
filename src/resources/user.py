from flask_restful import Resource, reqparse
from models.user import User


class AddUser(Resource):
    def post(selfs):
        try:
            # Parse all arguments
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str, help='User name')
            parser.add_argument('email', type=str, help='Email address')
            parser.add_argument('password', type=str, help='Password')
            args = parser.parse_args()

            _username = args['username']
            _email = args['email']
            _password = args['password']

            if not _username:
                raise AttributeError("Username is empty.")

            if not _email:
                raise AttributeError("Email is empty.")

            if len(_password) < 8:
                raise AttributeError("Password too short.")

            # TODO store user

            return {'Status': 'Success'}

        except Exception as e:
            return {'Status': 'Failed'}
