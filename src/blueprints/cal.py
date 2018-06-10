from flask import Blueprint, flash, g, redirect, render_template, url_for
from src.models.user import User, Session
from src.main import db
from src.utils import requires_auth
bp = Blueprint('cal', __name__)


@bp.route('/', methods=['GET'])
@requires_auth()
def get():

    return render_template('cal/index.html', title='Calendar')
