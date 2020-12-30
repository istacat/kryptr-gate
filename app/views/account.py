from flask import render_template, Blueprint
from flask_login import login_required

account_blueprint = Blueprint('account', __name__)


@account_blueprint.route('/accounts')
@login_required
def index():
    # accounts = Account.query.filter(Account.reseller_id == current_user.id)
    return render_template('index.html')
