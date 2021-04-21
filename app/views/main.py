from flask import Blueprint, redirect
from flask.helpers import url_for
from flask_login import login_required

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
@login_required
def index():
    # return render_template('index.html')
    return redirect(url_for("account.index"))
