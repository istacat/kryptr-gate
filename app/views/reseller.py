from datetime import datetime
from app.forms import ResellerForm
from flask import render_template, Blueprint, flash, redirect, url_for, jsonify, request
from flask_login import login_required, current_user
from app.models import User, Subordinate
from app.logger import log
from app.controllers import role_required

reseller_blueprint = Blueprint("reseller", __name__)


@reseller_blueprint.route("/resellers")
@login_required
def index():
    return render_template("pages/resellers.html")


@reseller_blueprint.route("/add_reseller", methods=["GET", "POST"])
@login_required
@role_required(roles=["admin"])
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
        Subordinate(chief_id=form.chief.data.id, subordinate_id=res.id).save()
        flash("Reseller creation successful.", "success")
        return redirect(url_for("reseller.index"))
    elif form.is_submitted():
        log(log.ERROR, "Submit failed: %s", form.errors)
    form.chief.data = current_user
    return render_template(
        "base_add_edit.html",
        include_header="components/_reseller-edit.html",
        form=form,
        description_header=("Add reseller"),
        cancel_link=url_for("reseller.index"),
        action_url=url_for("reseller.add_reseller")
    )


@reseller_blueprint.route("/edit_reseller/<int:reseller_id>", methods=["GET", "POST"])
@login_required
@role_required(roles=["admin"])
def edit_reseller(reseller_id):
    form = ResellerForm()
    id = reseller_id
    if id:
        user = (
            User.query.filter(User.deleted == False).filter(User.id == int(id)).first() # noqa e712
        )
    else:
        log(log.INFO, "No id was passed [%s]", id)
        flash("No account found for id [%s]", id)
        return redirect(url_for("reseller.index"))
    if user:
        if request.method == "GET":
            form.password.data = user.password
            form.username.data = user.username
            form.activated.data = user.activated.name
            form.role.data = user.role.name
            form.email.data = user.email
            form.chief.data = user.chief
        if form.validate_on_submit():
            user.username = form.username.data
            user.email = form.email.data
            user.password = form.password.data
            user.activated = form.activated.data
            user.role = form.role.data
            user.save()
            if user.chief != form.chief.data:
                Subordinate.query.filter(Subordinate.subordinate_id == user.id).delete()
                Subordinate(
                    chief_id=form.chief.data.id,
                    subordinate_id=user.id
                ).save()
            flash("Reseller creation successful.", "success")
            return redirect(url_for("reseller.index"))
        elif form.is_submitted():
            log(log.ERROR, "Submit failed: %s", form.errors)
        return render_template(
            "base_add_edit.html",
            include_header="components/_reseller-edit.html",
            form=form,
            description_header=("Edit reseller"),
            cancel_link=url_for("reseller.index"),
            action_url=url_for("reseller.edit_reseller", reseller_id=id),
        )
    else:
        log(log.INFO, "Reseller [%s] is deleted or unexistent", id)
        flash("No account found for id [%s]", id)
        return redirect(url_for("reseller.index"))


@reseller_blueprint.route("/delete_reseller/<int:reseller_id>", methods=["GET"])
@login_required
@role_required(roles=["admin"])
def delete_reseller(reseller_id):
    user = User.query.get(reseller_id)
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
        log(log.WARNING, "Tried to delete unexisted or deleted reseller [%s]", reseller_id)
        flash("Reseller doesnt exist or already deleted", "danger")
        return redirect(url_for("reseller.index"))


@reseller_blueprint.route("/api/reseller_list")
@login_required
@role_required(roles=["admin", "distributor"])
def get_reseller_list():
    resellers = current_user.resellers
    res = [reseller.to_json() for reseller in resellers if reseller.deleted != True] # noqa E712
    print(res)
    return jsonify(res)
