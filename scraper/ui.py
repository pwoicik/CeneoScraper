from re import sub

import requests
from flask import (
    Blueprint,
    g,
    redirect,
    render_template,
    request,
    Response,
    url_for,
)

from .extraction import *
from .models import db, Product
from .utils import *

bp = Blueprint("ui", __name__, url_prefix="/")


@bp.route("/")
def index() -> Response:
    return render_template("index.html")


@bp.route("/extract")
def extract_view() -> Response:
    if "id" in request.args:
        pid = int(request.args["id"])
        url = f"https://www.ceneo.pl/{pid}"
        product_req = requests.get(url)

        if product_req.status_code == 404:
            g.error = "Nie znaleziono przedmiotu o podanym ID"
        else:
            return redirect(url_for("ui.product_view", pid=pid))
    elif "name" in request.args:
        return redirect(url_for("ui.search", product_name=request.args["name"]))

    return render_template("extract.html")


@bp.route("/product/<int:pid>")
def product_view(pid: int) -> Response:
    prod = Product.query.filter(Product.id == pid).first()
    if not prod:
        prod = extract_product(pid)
        db.session.add(prod)
        db.session.commit()

    prod = prod.to_dict()
    reviews = prod["reviews"]

    if "filters" in request.args:
        prod["reviews"] = filtered_reviews(reviews, request.args["filters"])

    if "sort-by" in request.args:
        prod["reviews"] = sorted_reviews(
            reviews,
            request.args["sort-by"],
            reverse="reversed" in request.args
        )

    score_chart = render_score_chart(prod)
    recommendations_chart = render_reviews_chart(prod["reviews"])

    return render_template(
        "product.html",
        product=prod,
        score_chart=score_chart,
        recommendations_chart=recommendations_chart
    )


@bp.route("/search/<product_name>")
def search(product_name: str) -> Response:
    product_name = sub(r"\s+", "+", product_name.strip())
    products = find_products(product_name)

    return render_template("search.html", products=products)


@bp.route("/products")
def products_list():
    products = Product.query.all()
    format_pros_and_cons(products)
    products.sort(key=lambda x: x.name)

    return render_template("products_list.html", products=products)


@bp.route("/about")
def about():
    return render_template("about.html")
