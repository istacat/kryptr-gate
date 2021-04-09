from datetime import datetime
from app.forms import DistributorForm
from flask import render_template, Blueprint, flash, redirect, url_for, jsonify, request
from flask_login import login_required, current_user
from app.models import User
from app.logger import log
from app.controllers import role_required

distributor_blueprint = Blueprint("distributor", __name__)


@distributor_blueprint.route("/distributors")
@login_required
def index():
    return render_template("pages/distributors.html")


@distributor_blueprint.route("/add_distributor", methods=["GET", "POST"])
@login_required
@role_required(roles=["admin"])
def add_distributor():
    form = DistributorForm()
    if form.validate_on_submit():
        res = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            activated=form.activated.data,
            role=form.role.data,
        )
        res.save()
        flash("Distributor creation successful.", "success")
        return redirect(url_for("distributor.index"))
    elif form.is_submitted():
        log(log.ERROR, "Submit failed: %s", form.errors)
    return render_template(
        "base_add_edit.html",
        include_header="components/_user-edit.html",
        form=form,
        description_header=("Add distributor"),
        cancel_link=url_for("distributor.index"),
        action_url=url_for("distributor.add_distributor"),
    )


@distributor_blueprint.route("/edit_distributor", methods=["GET", "POST"])
@login_required
@role_required(roles=["admin"])
def edit_distributor():
    form = DistributorForm()
    id = request.args.get("id")
    if id:
        user = (
            User.query.filter(User.deleted == False).filter(User.id == int(id)).first() # noqa e712
        )
    else:
        log(log.INFO, "No id was passed [%s]", id)
        flash("No account found for id [%s]", id)
        return redirect(url_for("distributor.index"))
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
            flash("Distributor creation successful.", "success")
            return redirect(url_for("distributor.index"))
        elif form.is_submitted():
            log(log.ERROR, "Submit failed: %s", form.errors)
        return render_template(
            "base_add_edit.html",
            include_header="components/_distributor-edit.html",
            form=form,
            description_header=("Edit distributor"),
            cancel_link=url_for("distributor.index"),
            action_url=url_for("distributor.edit_distributor", id=id),
        )
    else:
        log(log.INFO, "Distributor [%s] is deleted or unexistent", id)
        flash("No account found for id [%s]", id)
        return redirect(url_for("distributor.index"))


@distributor_blueprint.route("/delete_distributor", methods=["GET"])
@login_required
@role_required(roles=["admin"])
def delete_distributor():
    user_id = request.args.get("id")
    user = User.query.get(user_id)
    if user:
        user.deleted = True
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        user.username = f"{user.username} deleted {current_time}"
        user.save()
        log(log.INFO, "Distributor deletion successful. [%s]", user)
        flash("Distributor deletion successful", "success")
        return redirect(url_for("distributor.index"))
    else:
        log(
            log.WARNING,
            "Tried to delete unexisted or deleted distributor [%s]",
            user_id,
        )
        flash("Distributor doesnt exist or already deleted", "danger")
        return redirect(url_for("distributor.index"))


@distributor_blueprint.route("/api/distributor_list")
@login_required
@role_required(roles=["admin"])
def get_distributor_list():
    distributors = current_user.distributors
    res = [
        distributor.to_json()
        for distributor in distributors
        if distributor.deleted != True # noqa E712
    ]
    print(res)
    return jsonify(res)
