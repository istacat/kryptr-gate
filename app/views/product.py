from flask import render_template, Blueprint, flash, jsonify, url_for, redirect
from flask_login import login_required
from app.models import Product
from app.logger import log
from app.forms import ProductForm

product_blueprint = Blueprint('product', __name__)


@product_blueprint.route('/products')
@login_required
def index():
    flash('Welcome to Machine', 'success')
    return render_template('pages/products.html')


@product_blueprint.route("/add_product", methods=["GET", "POST"])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        prod = Product(
            name=form.product_name.data,
            comment=form.comment.data,

        )
        prod.save()
        log(log.INFO, "Product creation successful. [%s]", prod)
        flash("Product creation successful.", "success")
        return redirect(url_for("product.index"))
    elif form.is_submitted():
        log(log.ERROR, "Submit failed: %s", form.errors)
    return render_template(
        "base_add_edit.html",
        include_header="components/_product-edit.html",
        form=form,
        cancel_link=url_for("product.index"),
        action_url=url_for("product.add_product"),
    )


@product_blueprint.route('/api/product_list')
@login_required
def get_product_list():
    products = Product.query.all()
    res = [prod.to_json() for prod in products]
    return jsonify(res)
