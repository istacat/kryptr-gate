from flask import render_template, Blueprint, flash, jsonify, redirect, url_for, request
from flask_login import login_required
from datetime import datetime
from app.logger import log
from app.models import User
from app.forms import UserForm

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/users")
@login_required
def index():
    return render_template("pages/users.html")


@user_blueprint.route("/add_user", methods=["GET", "POST"])
@login_required
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            activated=form.activated.data,
            role=form.role.data,
        )
        user.save()
        flash('User creation successful.', 'success')
        return redirect(url_for("user.index"))
    return render_template(
        "base_add_edit.html",
        include_header="components/_user-edit.html",
        form=form,
        description_header=("Add user"),
        cancel_link=url_for("user.index"),
        action_url=url_for("user.add_user"),
    )


@user_blueprint.route("/edit_user", methods=["GET", "POST"])
@login_required
def edit_user():
    form = UserForm()
    id = request.args.get("id")
    if id:
        user = User.query.filter(User.deleted == False).filter(User.id == int(id)).first() # noqa e712
    else:
        log(log.INFO, "no id was passed [%s]", id)
        flash("no account found for id [%s]", id)
        return redirect(url_for("user.index"))
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
            flash('User creation successful.', 'success')
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
        log(log.INFO, "user [%s] is deleted or unexistent", id)
        flash("no account found for id [%s]", id)
        return redirect(url_for("user.index"))


@user_blueprint.route("/delete_user", methods=["GET"])
@login_required
def delete_user():
    user_id = request.args.get("id")
    user = User.query.get(user_id)
    if user:
        user.deleted = True
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        user.username = f"{user.username} deleted {current_time}"
        user.save()
        log(log.INFO, "user deletion successful. [%s]", user)
        flash("user deletion successful", "success")
        return redirect(url_for("user.index"))
    else:
        log(log.WARNING, "tried to delete unexisted or deleted user [%s]", user_id)
        flash("user doesnt exist or already deleted", "danger")
        return redirect(url_for("user.index"))


@user_blueprint.route("/api/user_list")
@login_required
def get_user_list():
    users = User.query
    page = request.args.get('page', 1)
    page_size = request.args.get('size', 5)
    paginated_users = users.filter(User.deleted == False).order_by(User.id.asc()).paginate(int(page), int(page_size), False) # noqa e712
    res = {'max_pages': paginated_users.pages, 'data': [acc.to_json() for acc in paginated_users.items]}
    print(res)
    return jsonify(res)
