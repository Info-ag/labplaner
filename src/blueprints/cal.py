from flask import Blueprint, flash, g, redirect, render_template, url_for
from models.user import User, Session
from app import db

bp = Blueprint("cal", __name__)


@bp.route("/", methods=["GET"])
def get():
    if not g.session.authenticated:
        flash(u'You need to be logged in', 'error')
        return redirect(url_for("auth.login"))

    return render_template('cal/index.html', title="Calendar")
