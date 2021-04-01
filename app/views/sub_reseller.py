from datetime import datetime
from app.forms import SubResellerForm
from flask import render_template, Blueprint, flash, redirect, url_for, jsonify, request
from flask_login import login_required
from app.models import User
from app.logger import log
sub_reseller_blueprint = Blueprint('sub_reseller', __name__)


@sub_reseller_blueprint.route("/sub_resellers")
@login_required
def index():
    return render_template("pages/sub_resellers.html")


@sub_reseller_blueprint.route("/add_sub_reseller", methods=["GET", "POST"])
@login_required
def add_sub_reseller():
    form = SubResellerForm()
    if form.validate_on_submit():
        res = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            activated=form.activated.data,
            role=form.role.data,
        )
        res.save()
        flash("Sub-reseller creation successful.", "success")
        return redirect(url_for("sub_reseller.index"))
    elif form.is_submitted():
        log(log.ERROR, "Submit failed: %s", form.errors)
    return render_template(
        "base_add_edit.html",
        include_header="components/_user-edit.html",
        form=form,
        description_header=("Add sub-resell"),
        cancel_link=url_for("sub_reseller.index"),
        action_url=url_for("sub_reseller.add_sub_reseller"),
    )


@sub_reseller_blueprint.route("/edit_sub_reseller", methods=["GET", "POST"])
@login_required
def edit_sub_reseller():
    form = SubResellerForm()
    id = request.args.get("id")
    if id:
        user = User.query.filter(User.deleted == False).filter(User.id == int(id)).first() # noqa e712
    else:
        log(log.INFO, "No id was passed [%s]", id)
        flash("No account found for id [%s]", id)
        return redirect(url_for("sub_reseller.index"))
    if user:
        if request.method == "GET":
            form.password.data = user.password
            form.username.data = user.username
            form.activated.data = user.activated
            form.role.data = user.role
            form.email.data = user.email
        if form.validate_on_submit():
            user.username = form.username.data
            user.email = form.email.data
            user.password = form.password.data
            user.activated = form.activated.data
            user.role = form.role.data
            user.save()
            flash('Sub-reseller creation successful.', 'success')
            return redirect(url_for("sub_reseller.index"))
        elif form.is_submitted():
            log(log.ERROR, "Submit failed: %s", form.errors)
        return render_template(
            "base_add_edit.html",
            include_header="components/_sub_reseller-edit.html",
            form=form,
            description_header=("Edit sub-reseller"),
            cancel_link=url_for("sub_reseller.index"),
            action_url=url_for("sub_reseller.edit_sub_reseller", id=id),
        )
    else:
        log(log.INFO, "Sub-reseller [%s] is deleted or unexistent", id)
        flash("No account found for id [%s]", id)
        return redirect(url_for("sub_reseller.index"))


@sub_reseller_blueprint.route("/delete_sub_reseller", methods=["GET"])
@login_required
def delete_sub_reseller():
    user_id = request.args.get("id")
    user = User.query.get(user_id)
    if user:
        user.deleted = True
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        user.username = f"{user.username} deleted {current_time}"
        user.save()
        log(log.INFO, "Sub-reseller deletion successful. [%s]", user)
        flash("Sub-reseller deletion successful", "success")
        return redirect(url_for("sub_reseller.index"))
    else:
        log(log.WARNING, "Tried to delete unexisted or deleted sub-reseller [%s]", user_id)
        flash("Sub-reseller doesnt exist or already deleted", "danger")
        return redirect(url_for("sub_reseller.index"))


@sub_reseller_blueprint.route("/api/sub_reseller_list")
@login_required
def get_reseller_list():
    sub_resellers = User.query.filter(User.role == 'sub_reseller')
    res = [sub_reseller.to_json() for sub_reseller in sub_resellers]
    print(res)
    return jsonify(res)
