from flask import render_template, Blueprint, flash
from flask_login import current_user, login_required

from app.models import Account

account_blueprint = Blueprint('account', __name__)


@account_blueprint.route('/accounts')
@login_required
def index():
    # accounts = Account.query.filter(Account.reseller_id == current_user.id)
    return render_template('index.html')
