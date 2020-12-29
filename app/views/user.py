from flask import render_template, Blueprint, flash, jsonify, redirect, url_for
from flask_login import current_user, login_required

from app.models import User
from app.forms import UserForm

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/users')
@login_required
def index():
    return render_template('pages/users.html')


@user_blueprint.route('/add_user')
@login_required
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username,
            email=form.email,
            password=form.password,
            activated=form.activated,
            role=form.role.value,
        )
        user.save()
        return redirect(url_for('users.index'))
    return render_template('pages/')


@user_blueprint.route('/edit_user/<int:user_id>')
@login_required
def edit_user(user_id):
    pass


@user_blueprint.route('/api/user_list')
@login_required
def get_user_list():
    users = User.query.all()
    res = [user.to_json() for user in users]
    return jsonify(res)
