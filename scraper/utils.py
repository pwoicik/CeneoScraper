import os
from datetime import date
from re import match, UNICODE
from typing import Iterator, List

import plotly.express as px
from pandas import DataFrame

from .models import Product

__all__ = [
    "format_pros_and_cons",
    "render_score_chart",
    "render_reviews_chart",
    "sorted_reviews",
    "filtered_reviews",
]


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


def render_score_chart(product: dict) -> str:
    scores_dict = dict()
    for review in product["reviews"]:
        score = review["score"]
        scores_dict[score] = scores_dict[score] + 1 if score in scores_dict else 0

    wide_df = DataFrame(dict(Score=list(scores_dict.keys()), Count=list(scores_dict.values())))
    fig = px.bar(
        data_frame=wide_df.melt(id_vars="Score"),
        orientation="h",
        x="value",
        y="Score",
        labels={"Score": "Ocena", "value": "Ilość"},
        range_y=[-0.25, 5.25],
        log_x=True,
        color="Score",
        color_continuous_scale="emrld_r",
        template="simple_white",
        width=500,
        height=350,
        title="Ilość ocen",
    )
    fig.update(layout_coloraxis_showscale=False)
    fig.show(renderer="iframe")

    return get_chart_from_html()


def render_reviews_chart(reviews: List[dict]) -> str:
    recommendations_count = len(list(
        filter(lambda r: r["is_recommending"] is True, reviews)
    ))
    not_recommending_count = len(reviews) - recommendations_count

    px.pie(
        data_frame=DataFrame(
            dict(Recommending=["Tak", "Nie"], Count=[recommendations_count, not_recommending_count])
        ).melt(id_vars="Recommending"),
        values="value",
        labels={"Recommending": "Poleca", "value": "Ilość"},
        names="Recommending",
        title="Rekomendacje",
        height=350,
        width=500,
        color="Recommending",
        color_discrete_map={"Nie": "#0d515e", "Tak": "#d3f2a3"},
    ).show(renderer="iframe")

    return get_chart_from_html()


def get_chart_from_html() -> str:
    with open("./iframe_figures/figure_0.html", "r") as f:
        iframe = f.read()

    os.remove("./iframe_figures/figure_0.html")
    return iframe


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


def sorted_reviews(reviews: List[dict], attr: str, reverse: bool) -> List[dict]:
    if attr in reviews[0]:
        reviews.sort(
            key=lambda r: r[attr],
            reverse=reverse,
        )

    return reviews
