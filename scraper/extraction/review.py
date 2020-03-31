from bs4 import element


class Review:
    def __init__(self, review_container: element.Tag):
        self.id = review_container["data-entry-id"]
        self.author = review_container.select("div.reviewer-name-line")[0].text.strip()
        self.is_recommending = len(review_container.select("div.product-review-summary > em")) > 0

        score = review_container.select("span.review-score-count")
        self.score = None if len(score) == 0 else score[0].text.split("/")[0]

        self.is_purchase_confirmed = len(review_container.select("div.product-review-pz")) > 0

        dates = review_container.select("span.review-time > time")
        self.purchase_date = dates[0]["datetime"]
        self.purchase_date = dates[0]["datetime"]

        self.yes_votes = review_container.select("button.vote-yes")[0]["data-total-vote"]
        self.no_votes = review_container.select("button.vote-no")[0]["data-total-vote"]

        self.content = review_container.select("p.product-review-body")[0].text.strip()
        self.pros = [pro.text.strip() for pro in review_container.select("div.pros-cell > ul > li")]
        self.cons = [con.text.strip() for con in review_container.select("div.cons-cell > ul > li")]
