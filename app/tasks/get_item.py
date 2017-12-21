# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
from ..models import NewsModel
from ..schema import news_schema
from flask import abort
from config.config import app_config
import datetime

def get_item(page, key, start_date_orig, end_date_orig):
	if page is None or page == "1":
		start_item = 0
		end_item = 10
		next_page = 2
		prev_page = None
	elif int(page) > 1:
		start_item = (int(page)-1)*10+1
		end_item = start_item+10
		next_page = int(page)+1
		if int(page) > 1:
			prev_page = int(page)-1
		else:
			prev_page = None
	else:
		abort(400)


	if start_date_orig is not None and end_date_orig is not None:
		start_date = datetime.datetime.strptime("{} 00:00:00".format(start_date_orig), "%Y-%m-%d %H:%M:%S").strftime("%s")
		end_date = datetime.datetime.strptime("{} 23:23:59".format(end_date_orig), "%Y-%m-%d %H:%M:%S").strftime("%s")
		q = NewsModel.query.filter(NewsModel.date_created>=start_date).\
			filter(NewsModel.date_created>=end_date).\
			order_by(NewsModel.date_created.desc()).\
			order_by(NewsModel.date_published.desc()).all()
		count = len(q)
		q = q[start_item:end_item]
	else:
		q = NewsModel.query.order_by(NewsModel.date_created.desc()).\
			order_by(NewsModel.date_published.desc()).all()
		count = len(q)
		q = q[start_item:end_item]
		
	if end_item >= count:
		next_page = None

	data = news_schema.dump(q).data
	base_url = app_config[key].BASE_URL
	next_page_url = None
	prev_page_url = None
	if next_page is not None:
		if start_date_orig is not None and start_date_orig is not None:
			next_page_url = "{}/list?start_date={}&end_date={}&page={}".format(base_url, start_date_orig, end_date_orig, next_page)
		else:
			next_page_url = "{}/list?page={}".format(base_url, next_page)			
	if prev_page is not None:
		if start_date_orig is not None and start_date_orig is not None:
			prev_page_url = "{}/list?start_date={}&end_date={}&page={}".format(base_url, start_date_orig, end_date_orig, prev_page)
		else:
			prev_page_url = "{}/list?page={}".format(base_url, prev_page)

	schema = {
		"records": count,
		"next_page": next_page_url,
		"prev_page": prev_page_url,
		"data": data
	}

	return schema
