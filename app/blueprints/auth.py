'''
All Blueprint routes regardning rendering authentication templates
    except:
        /login [POST] --> handeling the login, has nothing todo with rendering a template
'''

from sqlalchemy.sql import exists
from werkzeug.exceptions import BadRequest
from flask import Blueprint, request, jsonify, g, redirect, render_template, flash

from app.models import db

from app.models.user import User, Session

bp = Blueprint('auth', __name__)


@bp.route('/signup', methods=['GET'])
def signup_get():
    if g.session.authenticated:
        flash(u'You are already logged in', 'success')
        next_url = request.values.get('next', default='/')
        return redirect(next_url)
    next_url = request.values.get('next', default='/')
    return render_template('auth/signup.html', title='Signup', next=next_url)


@bp.route('/login', methods=['GET'])
def login_get():
    if g.session.authenticated:
        flash(u'You are already logged in', 'success')
        next_url = request.values.get('next', default='/')
        return redirect(next_url)

    next_url = request.values.get('next', default='/')
    return render_template('auth/login.html', title='Login', next=next_url)


@bp.route('/login', methods=['POST'])
def login():
    next_url = request.values.get('next', default='/')
    if g.session.authenticated:
        return jsonify({'redirect': next_url}), 200

    try:
        email = request.values.get('email')
        if '@' in email:
            user = User.query.filter_by(email=email).one()
        else:
            user = User.query.filter_by(username=email).one()

        if user and user.check_password(request.values.get('password')):
            g.session.revoked = True
            db.session.merge(g.session)
            db.session.commit()

            _session = Session(user)
            _session.session_only = not bool(request.values.get('remember', default=False))
            db.session.add(_session)
            db.session.commit()
            g.session = _session
            return jsonify({'redirect': next_url}), 200
        return jsonify({'Status': 'Failed', 'reason': 'password'}), 406
    except:
        return jsonify({'Status': 'Failed', 'reason': 'email'}), 406


@bp.route('/confirm')
def confirm():
    token = request.args.get('token')
    if token and db.session.query(exists().where(User.confirmation_token == token)).scalar():
        user = User.query.filter_by(confirmation_token=token).one()
        user.email_confirmed = True
        user.confirmation_token = None
        db.session.merge(user)
        db.session.commit()

        return redirect('/')

    else:
        return BadRequest()


@bp.route('/logout')
def logout():
    if g.session.authenticated:
        g.session.revoked = True
        db.session.merge(g.session)
        db.session.commit()

        _session = Session()
        db.session.add(_session)
        db.session.commit()
        g.session = _session

    return redirect('/')
