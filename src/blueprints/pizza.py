from flask import Blueprint, flash, g, redirect, render_template, url_for
from src.models.user import User, Session
from src.main import db

bp = Blueprint("pizza", __name__)


@bp.route("/ranking", methods=["GET"])
def ranking():
    if not g.session.authenticated:
        flash(u'You need to be logged in', 'error')
        return redirect(url_for("auth.login"))

    return render_template('pizza/ranking.html', title="Pizza Ranking System")

@bp.route("/add", methods=["GET"])
def add():
    if not g.session.authenticated:
        flash(u'You need to be logged in', 'error')
        return redirect(url_for("auth.login"))

    return render_template('pizza/add.html', title="Bewertung hinzufügen")
