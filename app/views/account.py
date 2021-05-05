from datetime import datetime
from dateutil.relativedelta import relativedelta
import base64
import io
from sqlalchemy import or_, func
from flask import (
    render_template,
    Blueprint,
    jsonify,
    flash,
    redirect,
    url_for,
    request,
    session,
)
from flask_login import login_required, current_user
from app.models import Account, User, Subscription
from app.forms import (
    AccountAddForm,
    DeviceForm,
    AccountEditForm,
    SubscriptionForm,
    NewAccountForm,
)
from app.logger import log
from app.controllers import create_qrcode, generate_password, MDM, role_required, SimPro
from app.controllers.ldap import LDAP
from app.controllers.ssh_ps import RemoteMatrix
from config import BaseConfig as config

account_blueprint = Blueprint("account", __name__)


@account_blueprint.route("/accounts")
@login_required
def index():
    if 'accounts' in session:
        session.pop('accounts')
    return render_template("pages/accounts.html")


@account_blueprint.route("/add_account", methods=["GET", "POST"])
@login_required
def add_account():
    form = AccountAddForm(user=current_user)
    if request.method == "GET":
        form.reseller.data = current_user.username
        form.sub_activate_date.data = datetime.date(datetime.now())
        if "accounts" not in session:
            acc = {}
            ecc_id = Account.gen_ecc_id()
            ad_login = Account.gen_ad_login()
            forms = [NewAccountForm()]
            forms[0].ecc_id.data = ecc_id
            forms[0].ecc_password.data = generate_password()
            forms[0].ad_login.data = ad_login
            forms[0].ad_password.data = generate_password()
            forms[0].email.data = f"{ad_login}@kryptr.li"
            acc["ecc_id"] = forms[0].ecc_id.data
            acc["ecc_password"] = forms[0].ecc_password.data
            acc["ad_login"] = forms[0].ad_login.data
            acc["ad_password"] = forms[0].ad_password.data
            acc["email"] = forms[0].email.data
            acc["sim"] = forms[0].sim.data
            acc["comment"] = forms[0].comment.data
            session['accounts'] = [acc]
        else:
            forms = []
            for acc in session["accounts"]:
                sub_form = NewAccountForm()
                if not acc:
                    new_acc = {}
                    ecc_id = Account.gen_ecc_id()
                    ad_login = Account.gen_ad_login()
                    sub_form.ecc_id.data = ecc_id
                    sub_form.ecc_password.data = generate_password()
                    sub_form.ad_login.data = ad_login
                    sub_form.ad_password.data = generate_password()
                    sub_form.email.data = f"{ad_login}@kryptr.li"
                    new_acc["ecc_id"] = sub_form.ecc_id.data
                    new_acc["ecc_password"] = sub_form.ecc_password.data
                    new_acc["ad_login"] = sub_form.ad_login.data
                    new_acc["ad_password"] = sub_form.ad_password.data
                    new_acc["email"] = sub_form.email.data
                    new_acc["sim"] = sub_form.sim.data
                    new_acc["comment"] = sub_form.comment.data
                    session['accounts'][-1] = new_acc
                else:
                    sub_form.ecc_id.data = acc["ecc_id"]
                    sub_form.ecc_password.data = acc["ecc_password"]
                    sub_form.ad_login.data = acc["ad_login"]
                    sub_form.ad_password.data = acc["ad_password"]
                    sub_form.email.data = acc["email"]
                    sub_form.sim.data = acc["sim"]
                    sub_form.comment.data = acc["comment"]
                forms.append(sub_form)
        return render_template(
            "base_add_edit.html",
            include_header="components/_account-add.html",
            form=form,
            forms=enumerate(forms),
            description_header=("Add accounts"),
            cancel_link=url_for("account.index"),
            action_url=url_for("account.add_account"),
            count=len(forms)
        )
    if form.validate_on_submit():
        reseller = User.query.filter(User.username == form.reseller.data).first()
        for account in session["accounts"]:
            account_check = Account.query.filter(Account.sim == account["sim"])
            if account_check:
                log(log.WARNING, "Sim already has been used. Account - %s", account['ecc_id'])
                flash(f"Sim already has been used. Account {account['ecc_id']}", "danger")
                return redirect(url_for("account.add_account"))
            acc = Account(
                ecc_id=account["ecc_id"],
                ecc_password=account["ecc_password"],
                email=account["email"],
                ad_login=account["ad_login"],
                ad_password=account["ad_password"],
                sim=account["sim"],
                reseller_id=reseller.id,
                comment=account["comment"],
            ).save()
            sub = Subscription(
                account_id=acc.id,
                months=form.sub_duration.data,
                activation_date=form.sub_activate_date.data,
            ).save()
            log(
                log.INFO,
                "Generated ecc_id is. [%s] for account id [%s]",
                acc.ecc_id,
                acc.id,
            )
            if config.SIMPRO_BASE_URL:
                conn = SimPro()
                if not conn.check_sim(acc.sim):
                    log(log.WARNING, "Sim is not valid, or activated for account %s", acc.ecc_id)
                    flash(f"Sim is not valid, or not activated for account {acc.ecc_id}", "danger")
                    acc.delete()
                    sub.delete()
                    return redirect(url_for("account.add_account"))
            if config.LDAP_SERVER:
                conn = LDAP()
                user = conn.add_user(acc.ad_login)
                if not user:
                    log(log.WARNING, "Could not add user")
                    flash("Could not add user.", "danger")
                    return redirect(url_for("account.add_account"))
                error_message = user.reset_password(acc.ad_password)
                if error_message:
                    log(log.ERROR, "%s", error_message)
                    flash(error_message, "danger")
                    return redirect(url_for("account.add_account"))
                MDM().sync()
            if config.MATRIX_SERVER_HOST_NAME:
                matrix = RemoteMatrix()
                matrix.add_user(acc)
        log(log.INFO, "Account(s) creation successful.")
        flash("Account(s) creation successful.", "success")
        session.pop('accounts')
        return redirect(url_for("account.index"))

    elif form.is_submitted():
        log(log.ERROR, "Submit failed: %s", form.errors)
    return render_template(
        "base_add_edit.html",
        include_header="components/_account-add.html",
        form=form,
        description_header=("Add account"),
        cancel_link=url_for("account.index"),
        action_url=url_for("account.add_account"),
    )


@account_blueprint.route("/add_account/multiply/<int:acc_index>", methods=["POST"])
@login_required
def multiply_account(acc_index):
    form = NewAccountForm()
    if form.validate_on_submit():
        acc = session["accounts"][acc_index]
        acc["ecc_id"] = form.ecc_id.data
        acc["ecc_password"] = form.ecc_password.data
        acc["ad_login"] = form.ad_login.data
        acc["ad_password"] = form.ad_password.data
        acc["email"] = form.email.data
        acc["sim"] = form.sim.data
        acc["comment"] = form.comment.data
        session["accounts"][acc_index] = acc
        return redirect(url_for("account.add_account", _anchor=f"sub_form_{acc_index}"))


@account_blueprint.route("/add_account/add_template", methods=["GET"])
@login_required
def add_template():
    account = {}
    session['accounts'].append(account)
    acc_index = session['accounts'].index(account)
    return redirect(url_for("account.add_account", _anchor=f"sub_form_{acc_index}"))


@account_blueprint.route("/add_account/regenerate/<int:acc_index>", methods=["GET"])
@login_required
def regenerate(acc_index):
    account = session['accounts'][acc_index]
    ecc_id = Account.gen_ecc_id()
    ad_login = Account.gen_ad_login()
    account["ecc_id"] = ecc_id
    account["ecc_password"] = generate_password()
    account["ad_login"] = ad_login
    account["ad_password"] = generate_password()
    account["email"] = f"{ad_login}@kryptr.li"
    account["sim"] = ''
    account["comment"] = ''
    return redirect(url_for("account.add_account", _anchor=f"sub_form_{acc_index}"))


@account_blueprint.route("/edit_account/<int:account_id>", methods=["GET", "POST"])
@login_required
def edit_account(account_id):
    form = AccountEditForm(user=current_user)
    sub_form = SubscriptionForm()
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
            form.ecc_password.data = acc.ecc_password
            form.reseller.data = acc.reseller.username
            form.sim.data = acc.sim
            form.comment.data = acc.comment
            form.ad_login.data = acc.ad_login
            form.ad_password.data = acc.ad_password
            form.email.data = acc.email
            sub_form.sub_activate_date.data = datetime.date(datetime.now())
        if form.validate_on_submit():
            reseller = User.query.filter(User.username == form.reseller.data).first()
            acc.ecc_id = form.ecc_id.data
            acc.ecc_password = form.ecc_password.data
            acc.sim = form.sim.data
            acc.comment = form.comment.data
            acc.reseller_id = reseller.id
            acc.save()
            log(log.INFO, "Account data changed for account id [%s]", acc.id)
            return redirect(url_for("account.index"))
        elif form.is_submitted():
            log(log.ERROR, "Submit failed: %s", form.errors)
        subscription = acc.subscriptions[-1]
        expiration_date = subscription.activation_date + relativedelta(
            months=+subscription.months
        )
        return render_template(
            "base_add_edit.html",
            include_header="components/_account-edit.html",
            form=form,
            sub_form=sub_form,
            description_header=("Edit account"),
            cancel_link=url_for("account.index"),
            account_id=account_id,
            expiration_date=f'Expiration Date: {expiration_date.strftime("%d/%m/%Y, %H:%M:%S")}',
        )


@account_blueprint.route(
    "/edit_account/<int:account_id>/subscription", methods=["POST"]
)
@login_required
def extend_sub(account_id):
    form = SubscriptionForm()
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
        if form.validate_on_submit():
            expiration_date = datetime.date(
                acc.subscriptions[-1].activation_date
                + relativedelta(months=+acc.subscriptions[-1].months)
            )
            wipe_date = expiration_date + relativedelta(days=+15)
            if expiration_date > form.sub_activate_date.data:
                Subscription(
                    account_id=acc.id,
                    months=form.sub_duration.data,
                    activation_date=expiration_date,
                    type="ext",
                ).save()
            elif expiration_date < form.sub_activate_date.data < wipe_date:
                Subscription(
                    account_id=acc.id,
                    months=form.sub_duration.data,
                    activation_date=form.sub_activate_date.data,
                    type="ext",
                ).save()
            if wipe_date < form.sub_activate_date.data:
                flash("Invalid activation date", "danger")
                log(log.WARNING, "Set invalid activation date")
                return redirect(url_for("account.edit_account", account_id=account_id))
            log(log.INFO, "Account data changed for account id [%s]", acc.id)
            flash("Subscription has been updated.", "info")
            return redirect(url_for("account.index"))
        elif form.is_submitted():
            log(log.ERROR, "Submit failed: %s", form.errors)
            flash("Submit failed", "danger")
            return redirect(url_for("account.edit", account_id=account_id))


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
    accounts = current_user.accounts
    page = int(request.args.get("page", config.STARTING_PAGE))
    size = int(request.args.get("size", config.ITEMS_PER_PAGE))
    search_value = request.args.get("filters[0][value]", None)
    paginated_accs = accounts.order_by(Account.id.desc()).paginate(page, size, False)
    if search_value:
        paginated_accs = (
            accounts.filter(
                or_(
                    func.lower(Account.ecc_id).contains(func.lower(search_value)),
                    func.lower(Account.sim).contains(func.lower(search_value)),
                    func.lower(Account.ad_login).contains(func.lower(search_value)),
                )
            )
            .order_by(Account.id.desc())
            .paginate(page, size, False)
        )
    last_page = paginated_accs.pages
    return jsonify(
        {
            "last_page": last_page,
            "data": [acc.to_json() for acc in paginated_accs.items],
        }
    )


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
    command_name = request.args.get("command")
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
                    if account.ad_login == device.user.name:
                        account.mdm_device_id = device.device_id
                        account.save()
                        flash("Account device has been updated", "info")
                        log(
                            log.INFO,
                            "For account %s device has been set",
                            account.ecc_id,
                        )
                        return redirect(
                            url_for("account.device", account_id=account_id)
                        )
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
                status=status,
            )
        if form.validate_on_submit():
            action = device.action(form.command.data)
            command = form.command.data
            if command == "complete_wipe":
                device.wipe()
                account.mdm_device_id = None
                account.save()
            else:
                res = action.run()
                if res >= 400:
                    flash(f"Could not launch {command}", "danger")
                    return redirect(
                        url_for("account.device", account_id=account_id, command=None)
                    )
            flash("Commands have been run", "info")
            return redirect(
                url_for("account.device", account_id=account_id, command=command)
            )


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
