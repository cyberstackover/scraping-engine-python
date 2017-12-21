# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
from flask import g, jsonify, request
from flask.ext.restful import Resource, marshal
from sqlalchemy.exc import IntegrityError
from .. import db, app
from datetime import datetime
from ..tasks.get_rss import parse_site
from ..tasks.get_item import get_item
from config.config import app_config
from flask import abort
import os

key = os.environ['FLASK_CONFIG']

class Index(Resource):
    """
    Manage responses to the index route.
    URL: /api/v1/
    Request method: GET
    """

    def get(self):
        """ Return a welcome message """

        return {"message": "Welcome to the news API. "}

class Activate(Resource):
    def get(self, id):
        secret = app_config[key].JOB_SECRET_STRING
        if id != secret:
            abort(400)

        web_list = [
            "tempo",
            "antara",
            "cnn",
            "huffington",
            "nytimes",
            "foxnews",
            "cnbc",
            "wsj",
            "guardian",
            "chinadaily",
            "dw",
            "rt",
            "yahoo",
            "google",
            "kompas",
            "ipotnews"
        ]

        parse_site(web_list)
        db.engine.execute('DELETE FROM news t1 USING news t2 WHERE t1.title = t2.title AND t1.id > t2.id')
        return ''

class List(Resource):
    def get(self):
        # Get args
        args = request.args
        page = args.get("page")
        start_date = args.get("start_date")
        end_date = args.get("end_date")

        return get_item(page, key, start_date, end_date)
