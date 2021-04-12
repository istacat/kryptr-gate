from flask import render_template, Blueprint, jsonify, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.models import Account, User
from app.forms import AccountForm
from app.logger import log
from datetime import datetime
from app.controllers import account
from app.controllers.ldap import LDAP
import secrets

account_blueprint = Blueprint("account", __name__)


@account_blueprint.route("/accounts")
@login_required
def index():
    return render_template("pages/accounts.html")


@account_blueprint.route("/add_account", methods=["GET", "POST"])
@login_required
def add_account():
    form = AccountForm(user=current_user)
    if request.method == "GET":
        rand_int = secrets.randbelow(17575999)
        ecc_id = account.ecc_encode(rand_int)
        form.ecc_id.data = ecc_id
        form.email.data = f"{ecc_id}@kryptr.li"
        form.ad_login.data = f"{ecc_id}@kryptr.li"
        form.ad_password.data = f"{secrets.token_urlsafe(6)}"
        form.reseller.data = current_user.username
    if form.validate_on_submit():
        reseller = User.query.filter(User.username == form.reseller.data)
        acc = Account(
            ecc_id=form.ecc_id.data,
            email=form.email.data,
            ad_login=form.ad_login.data,
            ad_password=form.ad_password.data,
            sim=form.sim.data,
            comment=form.comment.data,
            reseller_id=reseller[0].id
        )
        acc.save()
        log(
            log.INFO,
            "Generated ecc_id is. [%s] for account id [%s]",
            acc.ecc_id,
            acc.id,
        )
        conn = LDAP()
        if conn:
            user = conn.add_user(acc.ecc_id, acc.ad_password)
            if not user:
                log(log.WARNING, "Couldnt add user")
        else:
            log(log.WARNING, "Couldnt connect to active directory")
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


@account_blueprint.route("/edit_account", methods=["GET", "POST"])
@login_required
def edit_account():
    id = request.args.get("id")
    form = AccountForm(user=current_user)
    acc = (
        Account.query.filter(Account.deleted == False) # noqa e712
        .filter(Account.id == int(id))
        .first()
    )
    if acc:
        if request.method == "GET":
            form.ecc_id.data = acc.ecc_id
            form.email.data = acc.email
            form.ad_login.data = acc.ad_login
            form.ad_password.data = acc.ad_password
            form.reseller.data = acc.reseller.username
        if form.validate_on_submit():
            reseller = User.query.filter(User.username == form.reseller.data)
            acc.ecc_id = form.ecc_id.data
            acc.email = form.email.data
            acc.ad_login = form.ad_login.data
            acc.ad_password = form.ad_password.data
            acc.sim = form.sim.data
            acc.comment = form.comment.data
            acc.reseller_id = reseller[0].id
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
            action_url=url_for("account.edit_account", id=id),
        )
    else:
        log(log.INFO, "account[%s] is deleted or unexistent", id)
        flash("no account found for id [%s]", id)
        return redirect(url_for("account.index"))


@account_blueprint.route("/delete_account", methods=["GET"])
@login_required
def delete_account():
    account_id = request.args.get("id")
    account = Account.query.get(account_id)
    if account:
        conn = LDAP()
        if conn:
            conn.delete_user(account.ecc_id)
        else:
            log(log.WARNING, "Couldnt connect to active directory")
        account.deleted = True
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        account.comment = f"Deleted {current_time}"
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
    account = current_user.accounts
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("size", 20))
    accounts = account[(page*page_size-page_size):(page*page_size-1)]
    if len(account) % page_size != 0:
        last_page = int(len(account) / page_size) + 1
    else:
        last_page = len(account) / page_size
    res = {
        "last_page": last_page,
        "data": [acc.to_json() for acc in accounts],
    }
    return jsonify(res)
