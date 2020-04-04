from re import sub

from flask import (
    Blueprint,
    g,
    redirect,
    render_template,
    request,
    Response,
    url_for,
)

from .charts import *
from .extraction import *
from .filtering import *
from .models import db, Product
from .utils import *

bp = Blueprint("ui", __name__, url_prefix="/")


@bp.route("/")
def index() -> Response:
    return render_template("index.html")


@bp.route("/extract")
def extract_view() -> Response:
    if "id" in request.args:
        pid = request.args["id"]

        if check_if_page_exists(f"https://www.ceneo.pl/{pid}"):
            return redirect(url_for("ui.product_view", pid=int(pid)))
        else:
            g.error = "Nie znaleziono przedmiotu o podanym ID"
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

    if "filters" in request.args:
        prod["reviews"] = filtered_reviews(prod["reviews"], request.args["filters"])

    if "sort-by" in request.args:
        prod["reviews"] = sorted_reviews(
            prod["reviews"],
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
def products_list() -> Response:
    products = Product.query.all()
    format_pros_and_cons(products)
    products.sort(key=lambda x: x.name)

    return render_template("products_list.html", products=products)


@bp.route("/about")
def about() -> Response:
    return render_template("about.html")
