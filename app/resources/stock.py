import os
from flask import g, jsonify, request, abort
from flask.ext.restful import Resource, marshal
from sqlalchemy.exc import IntegrityError
from .. import db, app
from datetime import datetime
from config.config import app_config
from ..tasks.get_stock import stock_list, seeddb, metadata, fundamental, update, data

key = os.environ['FLASK_CONFIG']

class StockList(Resource):
	def get(self):
		return stock_list()

class StockListDetail(Resource):
	def get(self, code):
		return metadata(code)

class StockListData(Resource):
	def get(self, code, start, end):
		return data(code, start, end)

class StockListSeed(Resource):
	def get(self):
		return seeddb()

class StockListFundamental(Resource):
	def get(self, code):
		return fundamental(code)

class StockListUpdate(Resource):
	def get(self):
		return seeddb(update=True)

		db.engine.execute('DELETE FROM stock_list_history t1 USING stock_list_history t2 WHERE t1.date_published = t2.date_published AND t1.id > t2.id AND t1.stock_id = t2.stock_id')
