from flask import Blueprint, flash, g, redirect, render_template, url_for
from models.user import User, Session
from app import db
import utils
bp = Blueprint("cal", __name__)


@bp.route("/", methods=["GET"])
@utils.requires_auth()
def get():

    return render_template('cal/index.html', title="Calendar")
