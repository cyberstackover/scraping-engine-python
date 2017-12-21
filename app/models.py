from __future__ import unicode_literals
from . import db, app
from .utilities.timestamp import timestamp
import time

class NewsModel(db.Model):
    """ News model """

    __tablename__ = "news"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, index=True)
    url = db.Column(db.String)
    src = db.Column(db.String)
    lead = db.Column(db.String)
    date_created = db.Column(db.Integer, default=timestamp)
    date_updated = db.Column(db.Integer, default=timestamp)
    date_published = db.Column(db.String, default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # time.strftime("%a, %d %b %Y %H:%M:%S %z", time.localtime())

    def __repr__(self):
        return "<NewsModel: %r>" % self.title

    def save_to_db(self):
        """Save to database."""
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            raise

class TwitterModel(db.Model):

    __tablename__ = "twitter_trend"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    query = db.Column(db.String)
    timestamp = db.Column(db.String)
    url = db.Column(db.String)

    trend_details = db.relationship("TwitterModelDetail", backref="twitter_trend", lazy="dynamic")

    def save_to_db(self):
        """Save to database."""
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            raise


class TwitterModelDetail(db.Model):

    __tablename__ = "twitter_trend_detail"

    trend_id = db.Column(db.Integer, db.ForeignKey("twitter_trend.id"))

    id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String)
    created_at = db.Column(db.String)
    text = db.Column(db.String)
    link = db.Column(db.String)
    username = db.Column(db.String)
    retweet_count = db.Column(db.Integer)
    favorite_count = db.Column(db.Integer)

    def save_to_db(self):
        """Save to database."""
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            raise

class StockList(db.Model):

    __tablename__ = "stock_list"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    code = db.Column(db.String(6))
    created_at = db.Column(db.Integer, default=timestamp)

    stock_history = db.relationship("StockListHistory", backref="stock_list", lazy="dynamic")

    def save_to_db(self):
        """Save to database."""
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            raise

class StockListHistory(db.Model):

    __tablename__ = "stock_list_history"

    stock_id = db.Column(db.Integer, db.ForeignKey("stock_list.id"))

    id = db.Column(db.Integer, primary_key=True)
    date_published = db.Column(db.Integer)
    open_value = db.Column(db.String)
    high_value = db.Column(db.String)
    low_value = db.Column(db.String)
    close_value = db.Column(db.String)
    adj_close_value = db.Column(db.String)
    volume_value = db.Column(db.Integer)

    def save_to_db(self):
        """Save to database."""
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            raise
