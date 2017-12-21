# -*- coding: utf-8 -*- 

from flask_marshmallow import Marshmallow
from .models import NewsModel

ma = Marshmallow()

class NewsSchema(ma.ModelSchema):
	class Meta:
		model = NewsModel

news_schema = NewsSchema(many=True)
