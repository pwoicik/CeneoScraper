from datetime import date
from re import match, UNICODE
from typing import Iterator, List


__all__ = [
    "filtered_reviews",
]


def filtered_reviews(reviews: List[dict], filters: str) -> List[dict]:
    for f in filters.split(";"):
        params = f.split(":")

        if match(r"aut:\w+(,\w+)*", f, UNICODE):
            authors = params[1].split(",")
            reviews = filter(
                lambda r: r["author"].lower() in authors,
                reviews
            )

        elif match(r"rec:[tf]", f):
            reviews = filter_by_bool(params[1], reviews, "is_recommending")

        elif match(r"sco:(([0-5]\.[05]-)|(-[0-5]\.[05])|([0-5]\.[05]-[0-5]\.[05]))", f):
            reviews = filter_by_num(params[1].split("-"), reviews, "score")

        elif match(r"conf:[tf]", f):
            reviews = filter_by_bool(params[1], reviews, "is_purchase_confirmed")

        elif match(
                r"isd:((\d{4}-\d{2}-\d{2}_)|(_\d{4}-\d{2}-\d{2})|(\d{4}-\d{2}-\d{2}_\d{4}-\d{2}-\d{2}))",
                f
        ):
            reviews = filter_by_date(params[1].split("_"), reviews, "issue_date")

        elif match(
                r"pcd:((\d{4}-\d{2}-\d{2}_)|(_\d{4}-\d{2}-\d{2})|(\d{4}-\d{2}-\d{2}_\d{4}-\d{2}-\d{2}))",
                f
        ):
            reviews = filter_by_date(params[1].split("_"), reviews, "purchase_date")

        elif match(r"pos:((\d+-)|(-\d+)|(\d+-\d+))", f):
            reviews = filter_by_num(params[1].split("-"), reviews, "yes_votes")

        elif match(r"neg:((\d+-)|(-\d+)|(\d+-\d+))", f):
            reviews = filter_by_num(params[1].split("-"), reviews, "no_votes")

        elif match(r"cnt:[tf]", f):
            reviews = filter_by_length(params[1], reviews, "content")

        elif match(r"pro:[tf]", f):
            reviews = filter_by_length(params[1], reviews, "pros")

        elif match(r"con:[tf]", f):
            reviews = filter_by_length(params[1], reviews, "cons")

    return list(reviews)


def filter_by_bool(b_str: str, collection: List[dict], attr: str) -> Iterator[dict]:
    return filter(
        lambda r: r[attr] is (b_str == "t"),
        collection
    )


def filter_by_num(xrange: List[str], collection: List[dict], attr: str) -> Iterator[dict]:
    fr = xrange[0]
    fr = float(fr) if len(fr) > 0 else 0.0
    to = xrange[1]
    to = float(to) if len(to) > 0 else float("inf")

    return filter(
        lambda r: to >= r[attr] >= fr,
        collection
    )


def filter_by_date(xrange: List[str], collection: List[dict], attr: str) -> Iterator[dict]:
    fr = xrange[0]
    fr = date.fromisoformat(fr) if len(fr) > 0 else date(1, 1, 1)
    to = xrange[1]
    to = date.fromisoformat(to) if len(to) > 0 else date.today()

    return filter(
        lambda r: fr <= r[attr].date() <= to,
        collection
    )


def filter_by_length(b_str: str, collection: List[dict], attr: str) -> Iterator[dict]:
    return filter(
        lambda r: (len(r[attr]) > 0) is (b_str == "t"),
        collection
    )
