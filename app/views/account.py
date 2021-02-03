import secrets
import datetime

from flask import render_template, Blueprint, jsonify, flash, redirect, url_for, request
from flask_login import login_required, current_user

from app.models import Account
from app.forms import AccountForm
from app.logger import log
from app.controllers import account
from app.controllers.ldap import LDAP
from config import BaseConfig as config

account_blueprint = Blueprint("account", __name__)


@account_blueprint.route("/accounts")
@login_required
def index():
    return render_template("pages/accounts.html")


@account_blueprint.route("/add_account", methods=["GET", "POST"])
@login_required
def add_account():
    form = AccountForm()
    if request.method == "GET":
        rand_int = secrets.randbelow(17575999)
        ecc_id = account.ecc_encode(rand_int)
        form.ecc_id.data = ecc_id
        form.email.data = f"{ecc_id}@kryptr.li"
        form.ad_login.data = f"{ecc_id}@kryptr.li"
        form.ad_password.data = f"{secrets.token_urlsafe(16)}"
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
            reseller_id=current_user.id,
        )
        acc.save()
        log(
            log.INFO,
            "Generated ecc_id is. [%s] for account id [%s]",
            acc.ecc_id,
            acc.id,
        )
        if config.LDAP_SERVER:
            conn = LDAP()
            user = conn.add_user(acc.ecc_id, acc.ad_password)
            if not user:
                log(log.WARNING, "Could not add user")
        log(log.INFO, "Account creation successful. [%s]", acc)
        flash("Account creation successful.", "success")
        return redirect(url_for("account.index"))
    elif form.is_submitted():
        log(log.ERROR, "Submit failed: %s", form.errors)
    return render_template(
        "base_add_edit.html",
        include_header="components/_account-edit.html",
        form=form,
        description_header=("Add account"),
        cancel_link=url_for("account.index"),
        action_url=url_for("account.add_account"),
    )


@account_blueprint.route("/edit_account/<int:account_id>", methods=["GET", "POST"])
@login_required
def edit_account(account_id):
    log(log.INFO, "edit account [%d]", account_id)
    form = AccountForm()
    acc = Account.query.get(account_id)
    if acc:
        if request.method == "GET":
            form.name.data = acc.name
            form.ecc_id.data = acc.ecc_id
            form.email.data = acc.email
            form.ad_login.data = acc.ad_login
            form.ad_password.data = acc.ad_password
        if form.validate_on_submit():
            acc.name = form.name.data
            acc.ecc_id = form.ecc_id.data
            acc.email = form.email.data
            acc.ad_login = form.ad_login.data
            acc.ad_password = form.ad_password.data
            acc.sim = form.sim.data
            acc.imei = form.imei.data
            acc.comment = form.comment.data
            acc.reseller_id = current_user.id
            acc.save()
            log(log.INFO, "Account data changed for account id [%s]", acc.id)
            return redirect(url_for("account.index"))
        elif form.is_submitted():
            log(log.ERROR, "Submit failed: %s", form.errors)
        return render_template(
            "base_add_edit.html",
            include_header="components/_account-edit.html",
            form=form,
            description_header=("Edit account"),
            cancel_link=url_for("account.index"),
            action_url=url_for("account.edit_account", account_id=account_id),
        )
    else:
        log(log.INFO, "account[%s] is deleted or non exist", account_id)
        flash("no account found for id [%d]", account_id)
        return redirect(url_for("account.index"))


@account_blueprint.route("/delete_account", methods=["GET"])
@login_required
def delete_account():
    account_id = request.args.get("id")
    account = Account.query.get(account_id)
    if account:
        if config.LDAP_SERVER:
            conn = LDAP()
            conn.delete_user(account.ecc_id)

        account.deleted = True
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        account.name = f"{account.name} deleted {current_time}"
        account.save()
        log(log.INFO, "Account deletion successful. [%s]", account)
        flash("Account deletion successful", "success")
        return redirect(url_for("account.index"))
    else:
        log(log.WARNING, "tried to delete unexisted or deleted acc [%s]", account_id)
        flash("Account doesnt exist or already deleted", "danger")
        return redirect(url_for("account.index"))


@account_blueprint.route("/api/account_list")
@login_required
def get_account_list():
    account = Account.query
    page = request.args.get("page", 1)
    page_size = request.args.get("size", 20)
    paginated_accounts = (
        account.filter(Account.deleted == False)  # noqa e701
        .order_by(Account.id.asc())
        .paginate(int(page), int(page_size), False)
    )
    res = {
        "last_page": paginated_accounts.pages,
        "data": [acc.to_json() for acc in paginated_accounts.items],
    }
    return jsonify(res)
