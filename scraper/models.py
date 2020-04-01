from . import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.Text)
    score = db.Column(db.Float)
    reviews = db.relationship("Review", backref="product", lazy=True)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
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
