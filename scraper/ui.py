import requests
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

bp = Blueprint("ui", __name__, url_prefix="/")


@bp.route("/", methods=["GET"])
def index() -> Response:
    return render_template("index.html")


@bp.route("/extract", methods=["GET"])
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


@bp.route("/product/<product_id>", methods=["GET"])
def product(product_id: str) -> str:
    return product_id


@bp.route("/search/<product_name>", methods=["GET"])
def search(product_name: str) -> str:
    product_name = sub(r"\s+", "+", product_name)
    products = requests.get(f"https://www.ceneo.pl/;szukaj-{product_name}")
    return product_name
