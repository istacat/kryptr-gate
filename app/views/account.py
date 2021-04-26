from datetime import datetime
import base64
import io
from flask import render_template, Blueprint, jsonify, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.models import Account, User
from app.forms import AccountForm, DeviceForm
from app.logger import log
from app.controllers import create_qrcode, generate_password, MDM, role_required
from app.controllers.ldap import LDAP
from app.controllers.ssh_ps import RemoteMatrix
from config import BaseConfig as config

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
        ecc_id = Account.gen_ecc_id()
        form.ecc_id.data = ecc_id
        form.email.data = f"{ecc_id}@kryptr.li"
        form.ad_login.data = f"{ecc_id}@kryptr.li"
        form.ad_password.data = generate_password()
        form.reseller.data = current_user.username
    if form.validate_on_submit():
        reseller = User.query.filter(User.username == form.reseller.data).first()
        acc = Account(
            ecc_id=form.ecc_id.data,
            email=form.email.data,
            ad_login=form.ad_login.data,
            ad_password=form.ad_password.data,
            sim=form.sim.data,
            comment=form.comment.data,
            reseller_id=reseller.id,
        ).save()
        log(
            log.INFO,
            "Generated ecc_id is. [%s] for account id [%s]",
            acc.ecc_id,
            acc.id,
        )
        if config.LDAP_SERVER:
            conn = LDAP()
            user = conn.add_user(acc.ecc_id)
            if not user:
                log(log.WARNING, "Could not add user")
                flash("Could not add user.", "danger")
                return render_template(
                    "base_add_edit.html",
                    include_header="components/_account-edit.html",
                    form=form,
                    description_header=("Add account"),
                    cancel_link=url_for("account.index"),
                    action_url=url_for("account.add_account"),
                )
            error_message = user.reset_password(acc.ad_password)
            if error_message:
                log(log.ERROR, "%s", error_message)
                flash(error_message, "danger")
                return render_template(
                    "base_add_edit.html",
                    include_header="components/_account-edit.html",
                    form=form,
                    description_header=("Add account"),
                    cancel_link=url_for("account.index"),
                    action_url=url_for("account.add_account"),
                )
            MDM().sync()
        if config.MATRIX_SERVER_HOST_NAME:
            matrix = RemoteMatrix()
            matrix.add_user(acc)
        log(log.INFO, "Account creation successful. [%s]", acc)
        flash("Account creation successful.", "success")
        return redirect(url_for("account.show_qrcode", account_id=acc.id))
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
    form = AccountForm(user=current_user)
    acc = Account.query.get(account_id)
    if acc not in current_user.accounts:
        log(
            log.ERROR,
            "User [%s] do not have permissions for acc [%s]",
            current_user,
            acc.id,
        )
        flash(f"<Access denied to account {account_id}>", "danger")
        return redirect(url_for("account.index"))
    if acc:
        if request.method == "GET":
            form.ecc_id.data = acc.ecc_id
            form.email.data = acc.email
            form.ad_login.data = acc.ad_login
            form.ad_password.data = acc.ad_password
            form.reseller.data = acc.reseller.username
            form.comment.data = acc.comment
        if form.validate_on_submit():
            reseller = User.query.filter(User.username == form.reseller.data).first()
            acc.ecc_id = form.ecc_id.data
            acc.email = form.email.data
            if acc.ad_password != form.ad_password.data and config.LDAP_SERVER:
                # change AD user password
                ldap = LDAP()
                success = ldap.change_password(acc.ecc_id, form.ad_password.data)
                if not success:
                    log(log.ERROR, "Can not change password: %s", form.errors)
                    return render_template(
                        "base_add_edit.html",
                        include_header="components/_account-edit.html",
                        form=form,
                        description_header=("Edit account"),
                        cancel_link=url_for("account.index"),
                        qrcode_url=url_for("account.show_qrcode", account_id=account_id),
                        action_url=url_for(
                            "account.edit_account", account_id=account_id
                        ),
                        account_id=account_id
                    )
            acc.ad_password = form.ad_password.data
            acc.sim = form.sim.data
            acc.comment = form.comment.data
            acc.reseller_id = reseller.id
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
            account_id=account_id,
        )


@account_blueprint.route("/delete_account/<int:account_id>", methods=["GET"])
@login_required
@role_required(roles=["admin", "support"])
def delete_account(account_id):
    account = Account.query.get(account_id)
    if account not in current_user.accounts:
        log(
            log.ERROR,
            "User [%s] do not have permissions for acc [%s]",
            current_user,
            account_id,
        )
        flash(f"<Access denied to account {account_id}>", "danger")
        return redirect(url_for("account.index"))
    if account:
        if config.LDAP_SERVER:
            conn = LDAP()
            conn.delete_user(account.ecc_id)

        account.deleted = True
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        account.comment = f"Deleted {current_time}"
        account.save()
        log(log.INFO, "Account deletion successful. [%s]", account)
        flash("Account deletion successful", "success")
        return redirect(url_for("account.index"))


@account_blueprint.route("/api/account_list")
@login_required
def get_account_list():
    accounts = [
        acc for acc in current_user.accounts if acc.deleted == False  # noqa E712
    ]
    accounts.sort(reverse=True, key=lambda x: x.id)
    return jsonify([acc.to_json() for acc in accounts])


@account_blueprint.route("/qrcode/<int:account_id>", methods=["GET"])
@login_required
def show_qrcode(account_id):
    account = Account.query.get(account_id)
    if account not in current_user.accounts:
        log(
            log.ERROR,
            "User [%s] do not have permissions for acc [%s]",
            current_user,
            account_id,
        )
        flash(f"<Access denied to account {account_id}>", "danger")
        return redirect(url_for("account.index"))
    if account:
        qrcode = create_qrcode(account)
        data = io.BytesIO()
        qrcode.save(data, "JPEG")
        encoded_img_data = base64.b64encode(data.getvalue())
        return render_template(
            "base_add_edit.html",
            include_header="components/_account-qrcode.html",
            img_data=encoded_img_data.decode("utf-8"),
            description_header=("Scan and close."),
            cancel_link=url_for("account.index"),
            action_url=url_for("account.edit_account", account_id=account_id),
        )


@account_blueprint.route("/account/<int:account_id>/device", methods=["GET", "POST"])
@login_required
def device(account_id):
    command_name = request.args.get('command')
    account = Account.query.get(account_id)
    if account not in current_user.accounts:
        log(
            log.ERROR,
            "User [%s] do not have permissions for acc [%s]",
            current_user,
            account_id,
        )
        flash(f"<Access denied to account {account_id}>", "danger")
        return redirect(url_for("account.index"))
    if account:
        conn = MDM()
        form = DeviceForm()
        device_id = account.mdm_device_id
        if not device_id:
            for device in conn.devices:
                if device.user:
                    if account.ecc_id == device.user.name:
                        account.mdm_device_id = device.device_id
                        account.save()
                        flash("Account device has been updated", "info")
                        log(
                            log.INFO,
                            "For account %s device has been set",
                            account.ecc_id,
                        )
                        return redirect(url_for("account.device", account_id=account_id))
            flash("Account has not device.", "danger")
            log(
                log.ERROR,
                "Device for account %s not set in mdm yet.",
                account.ecc_id,
            )
            return redirect(url_for("account.edit_account", account_id=account_id))
        device = conn.get_device(account.mdm_device_id)
        form.command.choices.extend(device.actions)
        if request.method == "GET":
            if command_name:
                command = device.action(command_name)
                status = f"Status: {command.status}"
                form.command.data = command_name
            else:
                status = None
            return render_template(
                "base_add_edit.html",
                form=form,
                include_header="components/_account-device.html",
                description_header=(f"{account.ecc_id} device."),
                cancel_link=url_for("account.edit_account", account_id=account_id),
                action_url=url_for("account.device", account_id=account_id),
                account_id=account_id,
                status=status
            )
        if form.validate_on_submit():
            action = device.action(form.command.data)
            command = form.command.data
            if command == 'complete_wipe':
                device.wipe()
                account.mdm_device_id = None
                account.save()
            else:
                res = action.run()
                if res >= 400:
                    flash(f"Could not launch {command}", "danger")
                    return redirect(url_for("account.device", account_id=account_id, command=None))
            flash("Commands have been run", "info")
            return redirect(url_for("account.device", account_id=account_id, command=command))


@account_blueprint.route("/account/<int:account_id>/device/wipe", methods=["GET"])
@login_required
def device_wipe(account_id):
    account = Account.query.get(account_id)
    if account not in current_user.accounts:
        log(
            log.ERROR,
            "User [%s] do not have permissions for acc [%s]",
            current_user,
            account_id,
        )
        flash(f"<Access denied to account {account_id}>", "danger")
        return redirect(url_for("account.index"))
    if account:
        conn = MDM()
        device = conn.get_device(account.mdm_device_id)
        device.wipe()
        account.mdm_device_id = None
        account.save()
        flash("The device has been wiped.", "info")
        return redirect(url_for("account.edit_account", account_id=account_id))
