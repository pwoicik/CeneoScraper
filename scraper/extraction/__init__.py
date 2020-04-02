from typing import List

from .utils import get_page, get_reviews, get_products, FoundProduct
from ..models import Product

__all__ = ["extract_product", "find_products"]


def extract_product(pid: int) -> Product:
    url = f"https://www.ceneo.pl/{pid}"
    page = get_page(f"https://www.ceneo.pl/{pid}")

    name = page.select("h1.product-name")[0].text
    img_url = page.select("a.js_image-preview > img")[0]["src"]

    score_el = page.select("span.product-score")
    score = None if len(score_el) < 1 else float(score_el[0]["content"].replace(",", "."))

    return Product(
        id=pid,
        url=url,
        name=name,
        img_url=img_url,
        score=score,
        reviews=list(get_reviews(pid))
    )


def find_products(name: str) -> List[FoundProduct]:
    page = get_page(f"https://www.ceneo.pl/;szukaj-{name};0115-1.htm")
    return list(get_products(page.select("div.cat-prod-row:not([data-shopurl])")))
