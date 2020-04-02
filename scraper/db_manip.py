from flask import (
    Blueprint,
    jsonify,
    make_response,
    request,
    Response
)

from .extraction import *
from .models import db, Product


bp = Blueprint("db", __name__, url_prefix="/db")


@bp.route("/product/<int:pid>", methods=["GET", "PUT", "DELETE"])
def remove_product(pid: int) -> Response:
    product = Product.query.filter(Product.id == pid).first()

    headers = {"Content-Type": "application/json"}

    if request.method == "GET" and product:
        return make_response(jsonify(product.to_dict()), 200, headers)

    elif request.method == "PUT":
        if product:
            delete_product(product)

        product = extract(pid)
        db.session.add(product)
        db.session.commit()

        return make_response(jsonify({"status": "ok"}), 201, headers)

    elif request.method == "DELETE" and product:
        delete_product(product)
        return make_response(jsonify({"status": "ok"}), 200, headers)

    return make_response(jsonify({"status": "couldn't find product"}), 400, headers)


def delete_product(product: Product):
    for review in product.reviews:
        db.session.delete(review)
    db.session.delete(product)
    db.session.commit()
