from bs4 import BeautifulSoup
from re import match
from requests import get
from .review import Review
from typing import Generator


class Product:
    def __init__(self, product_id: str):
        self.id = int(product_id)
        self.url = f"https://www.ceneo.pl/{self.id}"

        page_res = get(self.url)
        page = BeautifulSoup(page_res.content, "html.parser")
        self.name = page.select("h1.product-name")[0].text
        self.img_url = page.select("a.js_image-preview > img")[0]["src"]

        score = page.select("span.product-score")
        self.score = None if len(score) < 1 else float(score[0]["content"].replace(",", "."))

        self.reviews = self.__get_reviews()

    def __get_reviews(self) -> Generator[Review, None, None]:
        for page in self.__get_review_pages():
            for container in page.find_all("li", "review-box"):
                yield Review(container)

    def __get_review_pages(self) -> Generator[BeautifulSoup, None, None]:
        i = 1
        res = get(self.__get_review_page_url(i))
        while res.status_code == 200 and match(r"https://www.ceneo.pl/\d+/opinie-\d+", res.url) is not None:
            yield BeautifulSoup(res.content, "html.parser")
            i += 1
            res = get(self.__get_review_page_url(i))

    def __get_review_page_url(self, page: int) -> str:
        return f"https://www.ceneo.pl/{self.id}/opinie-{page}"
