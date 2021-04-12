from flask import render_template, Blueprint, flash, jsonify, redirect, url_for, request
from flask_login import login_required
from datetime import datetime
from app.logger import log
from app.models import User
from app.forms import SupportForm
from app.controllers import role_required

support_blueprint = Blueprint("support", __name__)


@support_blueprint.route("/supports")
@login_required
def index():
    return render_template("pages/supports.html")


@support_blueprint.route("/add_support", methods=["GET", "POST"])
@login_required
@role_required(roles=["admin"])
def add_support():
    form = SupportForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            activated=form.activated.data,
            role=User.RoleType.support,
        )
        user.save()
        flash("Support creation successful.", "success")
        return redirect(url_for("support.index"))
    return render_template(
        "base_add_edit.html",
        include_header="components/_support-edit.html",
        form=form,
        description_header=("Add support"),
        cancel_link=url_for("support.index"),
        action_url=url_for("support.add_support"),
    )


@support_blueprint.route("/edit_support", methods=["GET", "POST"])
@login_required
@role_required(roles=["admin"])
def edit_support():
    form = SupportForm()
    id = request.args.get("id")
    if id:
        user = (
            User.query.filter(User.deleted == False) # noqa e712
            .filter(User.id == int(id))
            .first()
        )
    else:
        log(log.INFO, "No id was passed [%s]", id)
        flash("No account found for id [%s]", id)
        return redirect(url_for("support.index"))
    if user:
        if request.method == "GET":
            form.password.data = user.password
            form.username.data = user.username
            form.activated.data = user.activated
            form.email.data = user.email
        if form.validate_on_submit():
            user.username = form.username.data
            user.email = form.email.data
            user.password = form.password.data
            user.activated = form.activated.data
            user.save()
            flash("Support creation successful.", "success")
            return redirect(url_for("support.index"))
        elif form.is_submitted():
            log(log.ERROR, "Submit failed: %s", form.errors)
        return render_template(
            "base_add_edit.html",
            include_header="components/_support-edit.html",
            form=form,
            description_header=("Edit support"),
            cancel_link=url_for("support.index"),
            action_url=url_for("support.edit_support", id=id),
        )
    else:
        log(log.INFO, "Support [%s] is deleted or unexistent", id)
        flash("No account found for id [%s]", id)
        return redirect(url_for("support.index"))


@support_blueprint.route("/delete_support", methods=["GET"])
@login_required
@role_required(roles=["admin"])
def delete_support():
    user_id = request.args.get("id")
    user = User.query.get(user_id)
    if user:
        user.deleted = True
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        user.username = f"{user.username} deleted {current_time}"
        user.save()
        log(log.INFO, "Support deletion successful. [%s]", user)
        flash("Support deletion successful", "success")
        return redirect(url_for("support.index"))
    else:
        log(log.WARNING, "Tried to delete unexisted or deleted user [%s]", user_id)
        flash("Support doesnt exist or already deleted", "danger")
        return redirect(url_for("support.index"))


@support_blueprint.route("/api/support_list")
@login_required
@role_required(roles=["admin"])
def get_support_list():
    users = User.query.filter(User.role == "support")
    page = request.args.get("page", 1)
    page_size = request.args.get("size", 20)
    paginated_users = (
        users.filter(User.deleted == False)  # noqa e712
        .order_by(User.id.asc())
        .paginate(int(page), int(page_size), False)
    )
    res = {
        "max_pages": paginated_users.pages,
        "data": [acc.to_json() for acc in paginated_users.items],
    }
    print(res)
    return jsonify(res)
