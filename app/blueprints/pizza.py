from flask import Blueprint, flash, g, redirect, render_template, url_for
from app import db
from app.utils import requires_auth
bp = Blueprint('pizza', __name__)


@bp.route('/ranking', methods=['GET'])
@requires_auth()
def ranking():
    return render_template('pizza/ranking.html', title='Pizza Ranking System')

@bp.route('/add', methods=['GET'])
@requires_auth()
def add():
    return render_template('pizza/add.html', title='Bewertung hinzufügen')
