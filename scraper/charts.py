import os
from typing import List

import plotly.express as px
from pandas import DataFrame

__all__ = [
    "render_score_chart",
    "render_reviews_chart",
]


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
