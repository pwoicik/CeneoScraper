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

from .models import db, Product
from . import extraction


bp = Blueprint("ui", __name__, url_prefix="/")


@bp.route("/")
def index() -> Response:
    return render_template("index.html")


@bp.route("/extract")
def extract() -> Response:
    if "id" in request.args:
        url = f"https://www.ceneo.pl/{request.args['id']}"
        product_req = requests.get(url)

        if product_req.status_code == 404:
            g.error = "Nie znaleziono przedmiotu o podanym ID"
        else:
            return redirect(url_for("ui.product", product_id=request.args["id"]))
    elif "name" in request.args:
        return redirect(url_for("ui.search", product_name=request.args["name"]))

    return render_template("extract.html")


@bp.route("/product/<product_id>")
def product(product_id: str) -> Response:
    pid = int(product_id)
    prod = Product.query.filter(Product.id == pid).first()
    if not product:
        prod = extraction.extract(pid)
        db.session.add(prod)
        db.session.commit()

    return render_template("product.html", product=prod)


@bp.route("/search/<product_name>")
def search(product_name: str) -> str:
    product_name = sub(r"\s+", "+", product_name)
    # products = requests.get(f"https://www.ceneo.pl/;szukaj-{product_name}")
    return product_name


@bp.route("/products")
def products():
    return "products"


@bp.route("/about")
def about():
    return "about"
