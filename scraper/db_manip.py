from flask import (
    Blueprint,
    jsonify,
    make_response,
    request,
    Response
)

from .models import db, Product, Review
from .utils import to_json


bp = Blueprint("db", __name__, url_prefix="/db")


@bp.route("/product/<int:pid>", methods=["GET", "DELETE"])
def remove_product(pid: int) -> Response:
    product = Product.query.filter(Product.id == pid).first()

    headers = {"Content-Type": "application/json"}

    if not product:
        return make_response(jsonify({"status": "couldn't find product"}), 400, headers)

    if request.method == "GET":
        return make_response(to_json(product), 200, headers)
    elif request.method == "DELETE":
        for review in product.reviews:
            db.session.delete(review)
        db.session.delete(product)
        db.session.commit()

    return make_response(jsonify({"status": "ok"}), 200, headers)
