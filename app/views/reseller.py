from app.forms import ResellerForm
from flask import render_template, Blueprint, flash, redirect, url_for, jsonify
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
        cancel_link=url_for("reseller.index"),
        action_url=url_for("reseller.add_reseller"),
    )


@reseller_blueprint.route("/api/reseller_list")
@login_required
def get_reseller_list():
    resellers = User.query.filter(User.role == 'reseller')
    res = [reseller.to_json() for reseller in resellers]
    print(res)
    return jsonify(res)
