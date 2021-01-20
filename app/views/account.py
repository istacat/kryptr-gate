from flask import render_template, Blueprint, jsonify, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.models import Account, EccKey
from app.forms import AccountForm
from app.logger import log
from app.controllers import account
import secrets
account_blueprint = Blueprint("account", __name__)


@account_blueprint.route("/accounts")
@login_required
def index():
    return render_template("pages/accounts.html")


@account_blueprint.route("/add_account", methods=["GET", "POST"])
@login_required
def add_account():
    form = AccountForm()
    ecc_key = request.args.get('ecc_id')
    if not ecc_key:
        ecc_key = EccKey()
        ecc_key.save()
        ecc_id = account.ecc_encode(ecc_key.id)
        print(ecc_id)
        form.ecc_id.data = ecc_id
        form.email.data = f'{ecc_id}@kryptr.li'
        form.ad_login.data = f'{ecc_id}@kryptr.li'
        form.ad_password.data = f'{secrets.token_urlsafe(16)}'
    if form.validate_on_submit():

        acc = Account(
            name=form.name.data,
            ecc_id=form.ecc_id.data,
            email=form.email.data,
            ad_login=form.ad_login.data,
            ad_password=form.ad_password.data,
            sim=form.sim.data,
            imei=form.imei.data,
            comment=form.comment.data,
            reseller_id=current_user.id
        )
        acc.save()
        current_ecc_key = EccKey.query.filter(EccKey.id == ecc_key).first()
        current_ecc_key.account_id = acc.id
        current_ecc_key.save()
        log(log.INFO, "Account creation successful. [%s]", acc)
        flash("Account creation successful.", "success")
        return redirect(url_for("account.index"))
    elif form.is_submitted():
        log(log.ERROR, "Submit failed: %s", form.errors)
    return render_template(
        "base_add_edit.html",
        include_header="components/_account-edit.html",
        form=form,
        cancel_link=url_for("account.index"),
        action_url=url_for("account.add_account", ecc_id=ecc_key.id)
    )


@account_blueprint.route("/api/account_list")
@login_required
def get_account_list():
    account = Account.query
    page = request.args.get('page', 1)
    page_size = request.args.get('size', 20)
    paginated_accounts = account.order_by(Account.id.asc()).paginate(int(page), int(page_size), False)
    res = {'last_page': paginated_accounts.pages, 'data': [acc.to_json() for acc in paginated_accounts.items]}
    return jsonify(res)
