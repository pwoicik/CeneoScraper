from datetime import datetime
from re import match
from typing import Generator, List

from bs4 import BeautifulSoup, element
from requests import get

from ..models import Review


def get_page(url: str) -> BeautifulSoup:
    page_res = get(url)
    return BeautifulSoup(page_res.content, "html.parser")


def get_reviews(pid: int) -> Generator[Review, None, None]:
    for page in get_review_pages(pid):
        for container in page.find_all("li", "review-box"):
            yield construct_review(container)


def get_review_pages(pid: int) -> Generator[BeautifulSoup, None, None]:
    i = 1
    res = get(get_review_page_url(pid, i))
    while res.status_code == 200 and match(r"https://www.ceneo.pl/\d+/opinie-\d+", res.url) is not None:
        yield BeautifulSoup(res.content, "html.parser")
        i += 1
        res = get(get_review_page_url(pid, i))


def get_review_page_url(pid: int, page: int) -> str:
    return f"https://www.ceneo.pl/{pid}/opinie-{page}"


def construct_review(review_container: element.Tag) -> Review:
    rid = int(review_container["data-entry-id"])
    author = review_container.select("div.reviewer-name-line")[0].text.strip()
    is_recommending = len(review_container.select("div.product-review-summary > em")) > 0

    score_el = review_container.select("span.review-score-count")
    score = None if len(score_el) == 0 else float(score_el[0].text.split("/")[0].replace(",", "."))

    is_purchase_confirmed = len(review_container.select("div.product-review-pz")) > 0

    dates = review_container.select("span.review-time > time")
    issue_date = datetime.fromisoformat(dates[0]["datetime"])
    purchase_date = datetime.fromisoformat(dates[0]["datetime"])

    yes_votes = int(review_container.select("button.vote-yes")[0]["data-total-vote"])
    no_votes = int(review_container.select("button.vote-no")[0]["data-total-vote"])

    content = review_container.select("p.product-review-body")[0].text.strip()

    pros = review_container.select("div.pros-cell > ul > li")
    if len(pros) == 0:
        pros = None
    else:
        pros = "\0".join([pro.text.strip() for pro in pros])
    cons = review_container.select("div.cons-cell > ul > li")
    if len(cons) == 0:
        cons = None
    else:
        cons = "\0".join([con.text.strip() for con in cons])

    return Review(
        id=rid,
        author=author,
        is_recommending=is_recommending,
        score=score,
        is_purchase_confirmed=is_purchase_confirmed,
        issue_date=issue_date,
        purchase_date=purchase_date,
        yes_votes=yes_votes,
        no_votes=no_votes,
        content=content,
        pros=pros,
        cons=cons
    )


class FoundProduct:
    def __init__(self, product_row: element.Tag):
        self.id = product_row["data-pid"]

        photo = product_row.select("img")[0]
        self.name = photo["alt"]
        self.img_url = photo["src"]

        score = product_row.select(".product-score")
        if len(score) > 0:
            score = float(score[0].text.split("/")[0].strip().replace(",", "."))
        else:
            score = None
        self.score = score

        review_count = product_row.select(".product-reviews-link")
        if len(review_count) > 0:
            review_count = int(review_count[0].text.split(" ")[0].strip())
        else:
            review_count = 0
        self.reviews_count = review_count


def get_products(product_rows: List[element.Tag]) -> Generator[FoundProduct, None, None]:
    for i in range(4):
        yield FoundProduct(product_rows[i])
