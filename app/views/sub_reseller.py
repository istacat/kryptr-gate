from app.forms import SubResellerForm
from flask import render_template, Blueprint, flash, redirect, url_for, jsonify
from flask_login import login_required
from app.models import User
from app.logger import log
sub_reseller_blueprint = Blueprint('sub_reseller', __name__)


@sub_reseller_blueprint.route("/sub_resellers")
@login_required
def index():
    return render_template("pages/sub_resellers.html")


@sub_reseller_blueprint.route("/add_sub_reseller", methods=["GET", "POST"])
@login_required
def add_sub_reseller():
    form = SubResellerForm()
    if form.validate_on_submit():
        res = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            activated=form.activated.data,
            role=form.role.data,
        )
        res.save()
        flash("Sub reseller creation successful.", "success")
        return redirect(url_for("sub_reseller.index"))
    elif form.is_submitted():
        log(log.ERROR, "Submit failed: %s", form.errors)
    return render_template(
        "base_add_edit.html",
        include_header="components/_user-edit.html",
        form=form,
        cancel_link=url_for("sub_reseller.index"),
        action_url=url_for("sub_reseller.add_sub_reseller"),
    )


@sub_reseller_blueprint.route("/api/sub_reseller_list")
@login_required
def get_reseller_list():
    sub_resellers = User.query.filter(User.role == 'sub_reseller')
    res = [sub_reseller.to_json() for sub_reseller in sub_resellers]
    print(res)
    return jsonify(res)
