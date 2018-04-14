#pylint: disable-all
from flask import Flask, render_template, make_response, redirect, request, jsonify, abort, url_for
from hashlib import sha256
from random import randint
from bcrypt import hashpw, gensalt, checkpw
from database import User

APP = Flask(__name__)
USERDB = {'Simon': {'pw': b'$2b$12$dFZFqlDLXkPJyqRnTzPGhu6TqxkaWtiQ17WdE5P9o0ctFcMxYo2ge', 'id': '1', 'userid': '7ed586770508da0ffac6d19fe99750b083a1fe84235574f4d4c48f1f8d6f241a'}} #sha256(bytes('Simon' + '1', 'utf-8')).hexdigest() #hashpw(bytes('123456', 'UTF-8'), gensalt())

class FlaskSites(object):

    def __init__(self):
        pass

    @staticmethod
    @APP.route('/')
    def index(text=''):
        return render_template('index.html', message=text)

    @staticmethod
    @APP.route('/login/')
    def login():
        return render_template('login.html', warning='')

    @staticmethod
    @APP.route('/logout/', methods=['POST', 'GET'])
    def logout():
        resp = make_response(render_template('logout.html'))
        resp.set_cookie('userID', '')
        resp.set_cookie('user', '')
        return resp

    @staticmethod
    @APP.route('/dashboard/', methods=['POST', 'GET'])
    def dashboard():
        if request.method == 'POST':

            user = request.form['name']
            password = request.form['password']
            try:
                if checkpw(bytes(password, 'UTF-8'), USERDB[user]['pw']):
                    userid = USERDB[user]['userid']

                    resp = make_response(render_template('dashboard.html', name=user))
                    resp.set_cookie('userID', userid)
                    resp.set_cookie('user', user)
                    return resp
            except KeyError:
                pass
            return render_template('login.html', warning='Username or password wrong..')
        else:
            if request.cookies.get('user'):
                if request.cookies.get('user') != '':
                    return render_template('dashboard.html', name=request.cookies.get('user'))
            return redirect(url_for('login'))


    @staticmethod
    @APP.route('/planer/<name>/')
    def planer():
        return render_template('login.html', warning='Something went wrong')


    @staticmethod
    @APP.route('/api/user/<uid>/')
    def user_by_uid(uid):
        '''Returns all data of a user.'''
        client_id = request.args.get('id')
        secret_key = request.args.get('key')
        if not client_id or not secret_key:     # TODO insert API validation check
            return abort(401)

        if request.method == "GET":
            users = User()
            users.load()

            user = users.get(uid=uid)
            if not user:
                return abort(404)

            response = jsonify({"uid": user.uid,
                                "firstname": user.firstname,
                                "lastname": user.lastname,
                                "mail": user.mail,
                                "birthday": user.birthday,
                                "pgids": user.pgids,
                                "isadmin": user.isadmin,
                                "ismentor": user.ismentor,
                                "ismember": user.ismember})
            response.status_code = 201
            return response
        elif request.method == "DELETE":
            pass


    @staticmethod
    @APP.route('/api/user/<uid>/<attribute>/')
    def user_attribute_by_uid(uid, value):
        '''Returns a specified value of a user.'''
        aid = request.args.get('api')
        if not aid:     # TODO insert API validation check
            return abort(401)

        if request.method == "GET":
            users = User()
            users.load()

            user = users.get(uid=uid)
            if not user:
                return abort(404)

            value = user[attribute]
            if not value:
                return abort(404)

            response = jsonify(value)
            response.status_code = 201
            return response
        elif request.method == "PATCH":
            pass


    @staticmethod
    @APP.route('/api/users/')
    def users():
        '''Returns all datas of all users.'''
        aid = request.args.get('api')
        if not aid:     # TODO insert API validation check
            return abort(401)

        if request.method == "GET":
            users = User()
            users.load()

            all_users = users.get_all()
            if not all_users:
                return abort(404)

            response_list = []
            for user in all_users:
                response_list.append({"uid": user.uid,
                                    "firstname": user.firstname,
                                    "lastname": user.lastname,
                                    "mail": user.mail,
                                    "birthday": user.birthday,
                                    "pgids": user.pgids,
                                    "isadmin": user.isadmin,
                                    "ismentor": user.ismentor,
                                    "ismember": user.ismember})

            response = jsonify(response_list)
            response.status_code = 201
            return response
