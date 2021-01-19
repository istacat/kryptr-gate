from flask import render_template, Blueprint, flash, jsonify, redirect, url_for, request
from flask_login import login_required

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
        cancel_link=url_for("user.index"),
        action_url=url_for("user.add_user"),
    )


@user_blueprint.route("/edit_user")
@login_required
def edit_user():
    pass


@user_blueprint.route("/api/user_list")
@login_required
def get_user_list():
    users = User.query
    page = request.args.get('page', 1)
    page_size = request.args.get('size', 5)
    paginated_users = users.order_by(User.id.asc()).paginate(int(page), int(page_size), False)
    res = {'max_pages': paginated_users.pages, 'data': [acc.to_json() for acc in paginated_users.items]}

    # last_page = {'last_page': paginated_users.pages}

    # res = [user.to_json() for user in users]
    # res += last_page
    print(res)
    return jsonify(res)
