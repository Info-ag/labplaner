# pylint: disable-all
from flask import render_template, \
    make_response, \
    redirect, \
    request, \
    jsonify, \
    abort, \
    url_for
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from bcrypt import checkpw

from database import User
import dbconfig

app = Flask(__name__)
app.config.from_object(dbconfig.DBConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

# TODO replace
USERDB = {'Simon': {'pw': b'$2b$12$dFZFqlDLXkPJyqRnTzPGhu6TqxkaWtiQ17WdE5P9o0ctFcMxYo2ge', 'id': '1',
                    'userid': '7ed586770508da0ffac6d19fe99750b083a1fe84235574f4d4c48f1f8d6f241a'}}  # sha256(bytes('Simon' + '1', 'utf-8')).hexdigest() #hashpw(bytes('123456', 'UTF-8'), gensalt())


@app.route('/')
def index(text=''):
    return render_template('index.html', message=text)


@app.route('/login/')
def login():
    return render_template('login.html', warning='')


@app.route('/logout/', methods=['POST', 'GET'])
def logout():
    resp = make_response(render_template('logout.html'))
    resp.set_cookie('userID', '')
    resp.set_cookie('user', '')
    return resp


@app.route('/dashboard/', methods=['POST', 'GET'])
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


@app.route('/planer/<name>/')
def planer():
    return render_template('login.html', warning='Something went wrong')


@app.route('/api/create/user', methods=['POST'])
def create_user():
    data = request.data
    users = User()
    users.add(firstname=data.get('lastname'), lastname=data.get('lastname'), mail=data.get('mail'),
              password=data.get('password'), birthday=data.get('birthday'), pgids=data.get('pgids'),
              ismentor=data.get('ismentor'), ismember=data.get('ismentor'), isadmin=data.get('isadmin'))


@app.route('/api/user/<uid>/', methods=['GET', 'POST'])
def user_by_uid(uid):
    '''Returns all data of a user.'''
    client_id = request.args.get('id')
    secret_key = request.args.get('key')
    if not client_id or not secret_key:  # TODO insert API validation check
        return abort(401)

    if request.method == "GET":
        user = User().get(uid=uid)
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
        users = User()
        users.delete(uid=uid)


@app.route('/api/auth', method='POST')
def dashboard():
    user = request.form['name']
    password = request.form['password']

    user = User()
    user = user.get(mail=user)
    try:
        if checkpw(bytes(password, 'UTF-8'), user.password):
            userid = USERDB[user]['userid']
            resp = make_response(render_template('dashboard.html', name=user))
            resp.set_cookie('userID', userid)
            resp.set_cookie('user', user)
            return resp
    except KeyError:
        pass
    return render_template('login.html', warning='Username or password wrong..')


@app.route('/api/user/<uid>/<attribute>/', methods=['GET'])
def user_attribute_by_uid(uid, attribute):
    '''Returns a specified value of a user.'''
    aid = request.args.get('api')
    if not aid:  # TODO insert API validation check
        return abort(401)

    if request.method == "GET":
        user = User().get(uid=uid)
        if not user:
            return abort(404)

        value = user[attribute]
        if not value:
            return abort(404)

        response = jsonify(value)
        response.status_code = 201
        return response


@app.route('/api/user/<uid>/<attribute>/<patch>', methods=['PATCH'])
def user_atrribute_by_uid(uid, attribute, patch):
    '''Returns a specified value of a user.'''
    aid = request.args.get('api')
    if not aid:  # TODO insert API validation check
        return abort(401)

    if request.method == "PATCH":
        users = User()

        users.patch(uid=uid, name=attribute, value=patch)
        response = jsonify({"success": True})
        response.status_code = 201
        return response


@app.route('/api/users/', methods=['GET'])
def users():
    '''Returns all datas of all users.'''
    aid = request.args.get('api')
    if not aid:  # TODO insert API validation check
        return abort(401)

    if request.method == "GET":
        all_users = User().get_all()
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


if __name__ == '__main__':
    app.run()