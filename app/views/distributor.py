from app.forms import DistributorForm
from flask import render_template, Blueprint, flash, redirect, url_for, jsonify
from flask_login import login_required
from app.models import User
from app.logger import log
from app.controllers import Admin
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
        flash("Distributor creation successful.", "success")
        return redirect(url_for("distributor.index"))
    elif form.is_submitted():
        log(log.ERROR, "Submit failed: %s", form.errors)
    return render_template(
        "base_add_edit.html",
        include_header="components/_user-edit.html",
        form=form,
        description_header=("Add distributor", "Edit distributor"),
        cancel_link=url_for("distributor.index"),
        action_url=url_for("distributor.add_distributor"),
    )


@distributor_blueprint.route("/api/distributor_list")
@login_required
def get_distributor_list():
    distributors = Admin.get_distributors()
    res = [distributor.to_json() for distributor in distributors]
    print(res)
    return jsonify(res)
