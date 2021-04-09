from flask import render_template, Blueprint, flash, jsonify, redirect, url_for, request
from flask_login import login_required
from datetime import datetime
from app.logger import log
from app.models import User
from app.forms import UserForm
from app.controllers import role_required

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/users")
@login_required
def index():
    return render_template("pages/users.html")


@user_blueprint.route("/add_user", methods=["GET", "POST"])
@login_required
@role_required(roles=["admin"])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            activated=form.activated.data,
            role=User.RoleType.admin,
        )
        user.save()
        flash("User creation successful.", "success")
        return redirect(url_for("user.index"))
    return render_template(
        "base_add_edit.html",
        include_header="components/_user-edit.html",
        form=form,
        description_header=("Add admin"),
        cancel_link=url_for("user.index"),
        action_url=url_for("user.add_user"),
    )


@user_blueprint.route("/edit_user", methods=["GET", "POST"])
@login_required
@role_required(roles=["admin"])
def edit_user():
    form = UserForm()
    id = request.args.get("id")
    if id:
        user = (
            User.query.filter(User.deleted == False).filter(User.id == int(id)).first() # noqa e712
        )
    else:
        log(log.INFO, "No id was passed [%s]", id)
        flash("No account found for id [%s]", id)
        return redirect(url_for("user.index"))
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
            flash("User creation successful.", "success")
            return redirect(url_for("user.index"))
        elif form.is_submitted():
            log(log.ERROR, "Submit failed: %s", form.errors)
        return render_template(
            "base_add_edit.html",
            include_header="components/_user-edit.html",
            form=form,
            description_header=("Edit user"),
            cancel_link=url_for("user.index"),
            action_url=url_for("user.edit_user", id=id),
        )
    else:
        log(log.INFO, "User [%s] is deleted or unexistent", id)
        flash("No account found for id [%s]", id)
        return redirect(url_for("user.index"))


@user_blueprint.route("/delete_user", methods=["GET"])
@login_required
@role_required(roles=["admin"])
def delete_user():
    user_id = request.args.get("id")
    user = User.query.get(user_id)
    if user:
        user.deleted = True
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        user.username = f"{user.username} deleted {current_time}"
        user.save()
        log(log.INFO, "User deletion successful. [%s]", user)
        flash("User deletion successful", "success")
        return redirect(url_for("user.index"))
    else:
        log(log.WARNING, "Tried to delete unexisted or deleted user [%s]", user_id)
        flash("User doesnt exist or already deleted", "danger")
        return redirect(url_for("user.index"))


@user_blueprint.route("/api/user_list")
@login_required
@role_required(roles=["admin"])
def get_user_list():
    users = User.query
    page = request.args.get("page", 1)
    page_size = request.args.get("size", 20)
    paginated_users = (
        users.filter(User.deleted == False) # noqa e712
        .order_by(User.id.asc())
        .paginate(int(page), int(page_size), False)
    )
    res = {
        "max_pages": paginated_users.pages,
        "data": [acc.to_json() for acc in paginated_users.items],
    }
    print(res)
    return jsonify(res)


# @user_blueprint.route("/api/chief_list")
# @login_required
# @role_required(roles=["admin"])
# def get_chief_list():
#     role = request.args.get("role")
#     if role == "sub_reseller":
#         query = User.query.filter(
#             User.role.name.in_(["admin", "distributor", "reseller"])
#         ).filter(
#             User.deleted == False # noqa e712
#         )
#         data = [user.id for user in query]
#         return jsonify(data)
#     elif role == "reseller":
#         query = User.query.filter(User.role.name.in_(["admin", "distributor"])).filter(
#             User.deleted == False # noqa e712
#         )
#         data = [user.id for user in query]
#         return jsonify(data)
#     else:
#         query = User.query.filter(User.role.name == "admin").filter(
#             User.deleted == False # noqa e712
#         )
#         data = [user.id for user in query]
#         return jsonify(data)
