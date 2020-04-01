from datetime import datetime
from re import match
from typing import Generator

from bs4 import BeautifulSoup, element
from requests import get

from ..models import Review


def get_reviews(pid: int) -> Generator[Review, None, None]:
    for page in __get_review_pages(pid):
        for container in page.find_all("li", "review-box"):
            yield __construct_review(pid, container)


def __get_review_pages(pid: int) -> Generator[BeautifulSoup, None, None]:
    i = 1
    res = get(__get_review_page_url(pid, i))
    while res.status_code == 200 and match(r"https://www.ceneo.pl/\d+/opinie-\d+", res.url) is not None:
        yield BeautifulSoup(res.content, "html.parser")
        i += 1
        res = get(__get_review_page_url(pid, i))


def __get_review_page_url(pid: int, page: int) -> str:
    return f"https://www.ceneo.pl/{pid}/opinie-{page}"


def __construct_review(pid: int, review_container: element.Tag) -> Review:
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

    pros = "\0".join([pro.text.strip() for pro in review_container.select("div.pros-cell > ul > li")])
    cons = "\0".join([con.text.strip() for con in review_container.select("div.cons-cell > ul > li")])

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
