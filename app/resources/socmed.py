import os
from flask import g, jsonify, request, abort
from flask.ext.restful import Resource, marshal
from sqlalchemy.exc import IntegrityError
from .. import db, app
from datetime import datetime
from config.config import app_config
from ..tasks.get_socmed import get_trend, get_twitter_detail, save_twitter_data, get_top

key = os.environ['FLASK_CONFIG']

class SocialMediaTwitterTrend(Resource):
	def get(self):
		return get_trend()

class SocialMediaInstagram(Resource):
	def get(self, ig_tag):
		return get_top(ig_tag)

class SocialMediaInstagramHome(Resource):
	def get(self):
		return 'Please provide tag'

class SocialMediaTwitter(Resource):
	def get(self, query):
		return get_twitter_detail(query)

class SocialMediaActivate(Resource):
	def get(self, id):
		secret = app_config[key].JOB_SECRET_STRING
		if id != secret:
		    abort(400)

		return save_twitter_data()
