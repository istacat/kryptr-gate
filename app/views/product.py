from flask import render_template, Blueprint, flash, jsonify, url_for, redirect, request
from flask_login import login_required
from app.models import Product
from app.logger import log
from app.forms import ProductForm

product_blueprint = Blueprint('product', __name__)


@product_blueprint.route('/products')
@login_required
def index():
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
        description_header=("Add product"),
        cancel_link=url_for("product.index"),
        action_url=url_for("product.add_product"),
    )


@product_blueprint.route("/edit_product", methods=["GET", "POST"])
@login_required
def edit_product():
    form = ProductForm()
    id = request.args.get("id")
    if id:
        product = Product.query.filter(Product.id == int(id)).first() # noqa e712
    else:
        log(log.INFO, "No id was passed [%s]", id)
        flash("No product found for id [%s]", id)
        return redirect(url_for("product.index"))
    if product:
        if request.method == "GET":
            form.product_name.data = product.product_name
            form.comment.data = product.comment
        if form.validate_on_submit():
            form.product_name.data = product.product_name
            form.comment.data = product.comment
            product.save()
            flash('Product creation successful.', 'success')
            return redirect(url_for("product.index"))
        elif form.is_submitted():
            log(log.ERROR, "Submit failed: %s", form.errors)
        return render_template(
            "base_add_edit.html",
            include_header="components/_product-edit.html",
            form=form,
            description_header=("Edit product"),
            cancel_link=url_for("product.index"),
            action_url=url_for("product.edit_product", id=id),
        )
    else:
        log(log.INFO, "Product [%s] is deleted or unexistent", id)
        flash("No product found for id [%s]", id)
        return redirect(url_for("product.index"))


@product_blueprint.route("/delete_product", methods=["GET"])
@login_required
def delete_product():
    product_id = request.args.get("id")
    product = Product.query.get(product_id)
    if product:
        # user.deleted = True
        # now = datetime.now()
        # current_time = now.strftime("%H:%M:%S")
        # user.username = f"{user.username} deleted {current_time}"
        # user.save()
        log(log.INFO, "Product deletion successful. [%s]", product)
        flash("Pistributor deletion successful", "success")
        return redirect(url_for("product.index"))
    else:
        log(log.WARNING, "Tried to delete unexisted or deleted product [%s]", product_id)
        flash("Product doesnt exist or already deleted", "danger")
        return redirect(url_for("product.index"))


@product_blueprint.route('/api/product_list')
@login_required
def get_product_list():
    products = Product.query.all()
    res = [prod.to_json() for prod in products]
    return jsonify(res)
