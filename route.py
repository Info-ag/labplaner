#pylint: disable-all
from flask import Flask, render_template, make_response, redirect, request
from hashlib import sha256
from random import randint
from bcrypt import hashpw, gensalt, checkpw

APP = Flask(__name__)
USERDB = {'Simon': {'pw': b'$2b$12$dFZFqlDLXkPJyqRnTzPGhu6TqxkaWtiQ17WdE5P9o0ctFcMxYo2ge', 'id': '1', 'userid': '7ed586770508da0ffac6d19fe99750b083a1fe84235574f4d4c48f1f8d6f241a'}} #sha256(bytes('Simon' + '1', 'utf-8')).hexdigest() #hashpw(bytes('123456', 'UTF-8'), gensalt())

class FlaskSites(object):

    def __init__(self):
        pass

    @staticmethod
    @APP.route('/')
    def index():
        return render_template('index.html')

    @staticmethod
    @APP.route('/login/')
    def login():
        return render_template('login.html', warning='')

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
                return render_template('dashboard.html', name=request.cookies.get('user'))
            else:
                return redirect(url_for('login'))

    @staticmethod
    @APP.route('/planer/<name>/')
    def planer():
        return render_template('login.html', warning='Something went wrong')
