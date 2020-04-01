from bs4 import BeautifulSoup
from requests import get

from ..models import Product
from .utils import get_reviews


__all__ = ["extract"]


def extract(pid: int) -> Product:
    url = f"https://www.ceneo.pl/{pid}"

    page_res = get(url)
    page = BeautifulSoup(page_res.content, "html.parser")

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
