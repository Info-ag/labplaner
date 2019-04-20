'''
All blueprint routes regardning rendering calendar templates(well just one)
'''

from flask import Blueprint, render_template
from app.util import requires_auth
bp = Blueprint('cal', __name__)


@bp.route('/', methods=['GET'])
@requires_auth()
def get():
    return render_template('cal/index.html', title='Calendar')
