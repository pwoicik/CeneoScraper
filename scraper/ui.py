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
import requests

from . import extraction
from .models import db, Product
from .utils import format_pros_and_cons


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
        prod = extraction.extract(pid)
        db.session.add(prod)
        db.session.commit()

    prod = prod.to_dict()

    if "sort-by" in request.args:
        sort_by = request.args["sort-by"]
        if sort_by in prod:
            prod["reviews"].sort(key=lambda r: r[sort_by])

    return render_template("product.html", product=prod)


@bp.route("/search/<product_name>")
def search(product_name: str) -> str:
    product_name = sub(r"\s+", "+", product_name)
    # products = requests.get(f"https://www.ceneo.pl/;szukaj-{product_name}")
    return product_name


@bp.route("/products")
def products_list():
    products = Product.query.all()
    format_pros_and_cons(products)
    products.sort(key=lambda x: x.name)

    return render_template("products_list.html", products=products)


@bp.route("/about")
def about():
    return "about"
