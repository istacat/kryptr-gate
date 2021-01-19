from app.forms import DistributorForm
from flask import render_template, Blueprint, flash, redirect, url_for, jsonify
from flask_login import login_required
from app.models import User
distributor_blueprint = Blueprint('distributor', __name__)


@distributor_blueprint.route("/distributors")
@login_required
def index():
    return render_template("pages/distributors.html")


@distributor_blueprint.route("/add_distributor", methods=["GET", "POST"])
@login_required
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
        flash('User creation successful.', 'success')
        flash("Account creation successful.", "success")
        return redirect(url_for("distributor.index"))
    return render_template(
        "base_add_edit.html",
        include_header="components/_user-edit.html",
        form=form,
        cancel_link=url_for("distributor.index"),
        action_url=url_for("distributor.add_distributor"),
    )


@distributor_blueprint.route("/api/distributor_list")
@login_required
def get_distributor_list():
    distributors = User.query.filter(User.role == 'distributor')
    res = [distributor.to_json() for distributor in distributors]
    print(res)
    return jsonify(res)
