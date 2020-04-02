from typing import List

from .models import Product


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
