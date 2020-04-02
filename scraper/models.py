from typing import Generator

from . import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.Text)
    score = db.Column(db.Float)
    reviews = db.relationship("Review", backref="product", lazy=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "img_url": self.img_url,
            "url": self.url,
            "score": self.score,
            "reviews": list(self.reviews_to_dict())
        }

    def reviews_to_dict(self) -> Generator[dict, None, None]:
        for r in self.reviews:
            yield r.to_dict()


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Text, nullable=False)
    is_recommending = db.Column(db.Boolean, nullable=False)
    score = db.Column(db.Float)
    is_purchase_confirmed = db.Column(db.Boolean, nullable=False)
    issue_date = db.Column(db.DateTime, nullable=False)
    purchase_date = db.Column(db.DateTime)
    yes_votes = db.Column(db.Integer, nullable=False)
    no_votes = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    pros = db.Column(db.Text)
    cons = db.Column(db.Text)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "author": self.author,
            "is_recommending": self.is_recommending,
            "score": self.score,
            "is_purchase_confirmed": self.is_purchase_confirmed,
            "issue_date": self.issue_date,
            "purchase_date": self.purchase_date,
            "yes_votes": self.yes_votes,
            "no_votes": self.no_votes,
            "content": self.content,
            "pros": self.pros.split("\0") if self.pros else [],
            "cons": self.cons.split("\0") if self.cons else [],
        }
