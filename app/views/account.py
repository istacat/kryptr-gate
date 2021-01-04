from flask import render_template, Blueprint, jsonify, flash, redirect, url_for
from flask_login import login_required
from app.models import Account
from app.forms import AccountForm

account_blueprint = Blueprint('account', __name__)


@account_blueprint.route('/accounts')
@login_required
def index():
    return render_template('pages/accounts.html')


@account_blueprint.route("/add_account", methods=["GET", "POST"])
@login_required
def add_account():
    form = AccountForm()
    if form.validate_on_submit():
        acc = Account(
            name=form.name.data,
            ecc_id=form.ecc_id.data,
            email=form.email.data,
            ad_login=form.ad_login.data,
            ad_password=form.ad_password.data,
            license_key=form.license_key.data,
            sim=form.sim.data,
            imei=form.imei.data,
            comment=form.comment.data,
        )
        acc.save()
        flash('Account creation successful.', 'success')
        return redirect(url_for("account.index"))
    return render_template(
        "base_add_edit.html",
        include_header="components/_account-edit.html",
        form=form,
        action_url=url_for("account.add_account"),
    )


@account_blueprint.route("/api/account_list")
@login_required
def get_user_list():
    accounts = Account.query.all()
    res = [acc.to_json() for acc in accounts]
    return jsonify(res)
