from datetime import datetime
from app.forms import ResellerForm
from flask import render_template, Blueprint, flash, redirect, url_for, jsonify, request
from flask_login import login_required
from app.models import User
from app.logger import log
reseller_blueprint = Blueprint('reseller', __name__)


@reseller_blueprint.route("/resellers")
@login_required
def index():
    return render_template("pages/resellers.html")


@reseller_blueprint.route("/add_reseller", methods=["GET", "POST"])
@login_required
def add_reseller():
    form = ResellerForm()
    if form.validate_on_submit():
        res = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            activated=form.activated.data,
            role=form.role.data,
        )
        res.save()
        flash("Reseller creation successful.", "success")
        return redirect(url_for("reseller.index"))
    elif form.is_submitted():
        log(log.ERROR, "Submit failed: %s", form.errors)
    return render_template(
        "base_add_edit.html",
        include_header="components/_user-edit.html",
        form=form,
        description_header=("Add reseller"),
        cancel_link=url_for("reseller.index"),
        action_url=url_for("reseller.add_reseller"),
    )


@reseller_blueprint.route("/edit_reseller", methods=["GET", "POST"])
@login_required
def edit_reseller():
    form = ResellerForm()
    id = request.args.get("id")
    if id:
        user = User.query.filter(User.deleted == False).filter(User.id == int(id)).first() # noqa e712
    else:
        log(log.INFO, "No id was passed [%s]", id)
        flash("No account found for id [%s]", id)
        return redirect(url_for("reseller.index"))
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
            flash('Reseller creation successful.', 'success')
            return redirect(url_for("reseller.index"))
        elif form.is_submitted():
            log(log.ERROR, "Submit failed: %s", form.errors)
        return render_template(
            "base_add_edit.html",
            include_header="components/_reseller-edit.html",
            form=form,
            description_header=("Edit reseller"),
            cancel_link=url_for("reseller.index"),
            action_url=url_for("reseller.edit_reseller", id=id),
        )
    else:
        log(log.INFO, "Reseller [%s] is deleted or unexistent", id)
        flash("No account found for id [%s]", id)
        return redirect(url_for("reseller.index"))


@reseller_blueprint.route("/delete_reseller", methods=["GET"])
@login_required
def delete_reseller():
    user_id = request.args.get("id")
    user = User.query.get(user_id)
    if user:
        user.deleted = True
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        user.username = f"{user.username} deleted {current_time}"
        user.save()
        log(log.INFO, "Reseller deletion successful. [%s]", user)
        flash("Reseller deletion successful", "success")
        return redirect(url_for("reseller.index"))
    else:
        log(log.WARNING, "Tried to delete unexisted or deleted reseller [%s]", user_id)
        flash("Reseller doesnt exist or already deleted", "danger")
        return redirect(url_for("reseller.index"))


@reseller_blueprint.route("/api/reseller_list")
@login_required
def get_reseller_list():
    resellers = User.query.filter(User.role == 'reseller')
    res = [reseller.to_json() for reseller in resellers]
    print(res)
    return jsonify(res)
