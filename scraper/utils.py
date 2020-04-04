from typing import List

from requests import get

from .models import Product

__all__ = [
    "check_if_page_exists",
    "format_pros_and_cons",
    "sorted_reviews",
]


def check_if_page_exists(url: str) -> bool:
    req = get(url)
    return req.status_code != 404


def format_pros_and_cons(products: List[Product]) -> List[Product]:
    for i, prod in enumerate(products):
        pros = []
        cons = []
        for review in prod.reviews:
            pros_split = review.pros.split("\0") if review.pros else []
            cons_split = review.cons.split("\0") if review.cons else []
            if len(pros_split) > 0:
                pros.extend(pros_split)
            if len(cons_split) > 0:
                cons.extend(cons_split)

        pros = set(filter(lambda x: len(x) > 0, pros))
        cons = set(filter(lambda x: len(x) > 0, cons))
        products[i].pros = pros if len(pros) > 0 else None
        products[i].cons = cons if len(cons) > 0 else None

    return products


def sorted_reviews(reviews: List[dict], attr: str, reverse: bool) -> List[dict]:
    if attr in reviews[0]:
        reviews.sort(
            key=lambda r: r[attr],
            reverse=reverse,
        )

    return reviews
