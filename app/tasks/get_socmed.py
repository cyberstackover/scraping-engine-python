import twitter
import pprint
import os
from config.config import app_config
import urllib.parse
from ..models import TwitterModel, TwitterModelDetail
import requests
from bs4 import BeautifulSoup
import ast
import json
from operator import itemgetter


key = os.environ['FLASK_CONFIG']

api = twitter.Api(
	consumer_key='dgVgmFmKUSW1GbPSlAqPlKw15',
	consumer_secret='HIwlLjY3xQ398HNVA8rxE4RKnzIQSklDCj4rDK5wwj6xwhxTcg',
	access_token_key='45126413-Qsxp0zWhB47PuNy3SRoMhhD5PoLjYjnEo2ZZbUIdN',
	access_token_secret='TM301TMsYceKCA92BiYBxSmd4pfjvAHkQPAHMot0nYiP0'
)

def get_trend():

	wwtrends = api.GetTrendsCurrent()
	idtrends = api.GetTrendsWoeid(23424846)
	base_url = app_config[key].BASE_URL

	wwtrends_list = []
	for trend in wwtrends:
		wwtrends_list.append({
			"name": trend.name,
			"query": trend.query,
			"timestamp": trend.timestamp,
			"url": trend.url,
			"details": "{}/socialmedia/twitter/{}".format(base_url, trend.query)
		})

	idtrends_list = []
	for trend in idtrends:
		idtrends_list.append({
			"name": trend.name,
			"query": trend.query,
			"timestamp": trend.timestamp,
			"url": trend.url,
			"details": "{}/socialmedia/twitter/{}".format(base_url, trend.query)
		})

	data = {
		"worldwide": wwtrends_list,
		"indonesia": idtrends_list
	}
	return data

def get_top(ig_tag):
	ig_list = []

	source = requests.get("https://www.instagram.com/explore/tags/{}/".format(ig_tag))
	soup = BeautifulSoup(source.text, "lxml")
	data = soup.find_all("script")[2].getText().replace("window._sharedData =","").replace(";","")
	data_dict = json.loads(data)["entry_data"]["TagPage"][0]["tag"]["top_posts"]["nodes"]

	for item in data_dict:
		ig_list.append({
			"caption": item["caption"],
			"owner_id": item["owner"]["id"],
			"comment_count": item["comments"]["count"],
			"likes_count": item["likes"]["count"],
			"published": item["date"],
			"link": "https://www.instagram.com/p/{}".format(item["code"]),
		})

	ig_list = sorted(ig_list, key=itemgetter('likes_count'), reverse=True)

	return ig_list



def get_twitter_detail(query):
	recent = api.GetSearch(
		raw_query="f=tweets&vertical=default&q={}&src=typd".format(urllib.parse.quote_plus(query))
	)

	popular = api.GetSearch(
		raw_query="vertical=default&q={}&src=typd".format(urllib.parse.quote_plus(query))
	)

	recent_list = []
	for item in recent:
		if item.retweeted_status is not None:
			item = item.retweeted_status
		recent_list.append({
			"created_at": item.created_at,
			"name": item.user.name,
			"text": item.text,
			"link": "https://twitter.com/{}/status/{}".format(item.user.screen_name, item.id),
			"username": item.user.screen_name,
			"retweet_count": item.retweet_count,
			"favorite_count": item.favorite_count
		})

	popular_list = []
	for item in recent:
		if item.retweeted_status is not None:
			item = item.retweeted_status
		popular_list.append({
			"created_at": item.created_at,
			"name": item.user.name,
			"text": item.text,
			"link": "https://twitter.com/{}/status/{}".format(item.user.screen_name, item.id),
			"username": item.user.screen_name,
			"retweet_count": item.retweet_count,
			"favorite_count": item.favorite_count
		})

	results = {
		"popular": popular_list,
		"recent": recent_list
	}

	return results

def save_twitter_data():

	wwtrends = api.GetTrendsCurrent()
	idtrends = api.GetTrendsWoeid(23424846)

	for trend in wwtrends:
		trend = TwitterModel(
			name=trend.name,
			query=trend.query,
			timestamp=trend.timestamp,
			url=trend.url
		)
		trend.save_to_db()

		popular = api.GetSearch(
			raw_query="vertical=default&q={}&src=typd".format(urllib.parse.quote_plus(trend.query))
		)

		for item in popular:
			if item.retweeted_status is not None:
				item = item.retweeted_status
			detail = TwitterModelDetail(
				created_at=item.created_at,
				account_name=item.user.name,
				trend_id=trend.id,
				text=item.text,
				link="https://twitter.com/{}/status/{}".format(item.user.screen_name, item.id),
				username=item.user.screen_name,
				retweet_count=item.retweet_count,
				favorite_count=item.favorite_count
			)
			detail.save_to_db()


	for trend in idtrends:
		trend = TwitterModel(
			name=trend.name,
			query=trend.query,
			timestamp=trend.timestamp,
			url=trend.url
		)
		trend.save_to_db()

		popular = api.GetSearch(
			raw_query="vertical=default&q={}&src=typd".format(urllib.parse.quote_plus(trend.query))
		)

		for item in popular:
			if item.retweeted_status is not None:
				item = item.retweeted_status
			detail = TwitterModelDetail(
				created_at=item.created_at,
				account_name=item.user.name,
				trend_id=trend.id,
				text=item.text,
				link="https://twitter.com/{}/status/{}".format(item.user.screen_name, item.id),
				username=item.user.screen_name,
				retweet_count=item.retweet_count,
				favorite_count=item.favorite_count
			)
			detail.save_to_db()
