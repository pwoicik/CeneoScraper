from typing import List, Generator, Dict

from flask import jsonify

from .models import Product, Review


def format_pros_and_cons(products: List[Product]) -> List[Product]:
    for i, prod in enumerate(products):
        pros = []
        cons = []
        for review in prod.reviews:
            pros_split = review.pros.split("\0")
            cons_split = review.cons.split("\0")
            if len(pros_split) > 0:
                pros.extend(pros_split)
            if len(cons_split) > 0:
                cons.extend(cons_split)

        pros = set(filter(lambda x: len(x) > 0, pros))
        cons = set(filter(lambda x: len(x) > 0, cons))
        products[i].pros = pros if len(pros) > 0 else None
        products[i].cons = cons if len(cons) > 0 else None

    return products


def to_json(product: Product):
    product_as_dict = {
        "id": product.id,
        "name": product.name,
        "url": product.url,
        "score": product.score,
        "reviews": list(reviews_to_dict(product.reviews))
    }

    return jsonify(product_as_dict)


def reviews_to_dict(reviews: List[Review]) -> Generator[Dict, None, None]:
    for r in reviews:
        yield {
            "id": r.id,
            "author": r.author,
            "is_recommending": r.is_recommending,
            "score": r.score,
            "is_purchase_confirmed": r.is_purchase_confirmed,
            "issue_date": r.issue_date,
            "purchase_date": r.purchase_date,
            "yes_votes": r.yes_votes,
            "no_votes": r.no_votes,
            "content": r.content,
            "pros": r.pros.split("\0"),
            "cons": r.cons.split("\0"),
        }
