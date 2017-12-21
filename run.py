from app.resources.base import Index, Activate, List
from app.resources.socmed import SocialMediaActivate, SocialMediaTwitter, SocialMediaTwitterTrend, SocialMediaInstagram, SocialMediaInstagramHome
from app.resources.stock import StockList, StockListSeed, StockListDetail, StockListFundamental, StockListUpdate, StockListData
from app import api, app
from redis import Redis
from rq import Queue
import time
from rq_scheduler import Scheduler
from datetime import datetime


""" Defining the API endpoints """
api.add_resource(Index, "/")
api.add_resource(List, "/list")
api.add_resource(Activate, "/activate/<id>")
api.add_resource(SocialMediaTwitterTrend, "/socialmedia/twitter")
api.add_resource(SocialMediaInstagramHome, "/socialmedia/instagram")
api.add_resource(SocialMediaInstagram, "/socialmedia/instagram/<ig_tag>")
api.add_resource(SocialMediaActivate, "/socialmedia/activate/<id>")
api.add_resource(SocialMediaTwitter, "/socialmedia/twitter/<query>")
api.add_resource(StockList, "/stock")
api.add_resource(StockListUpdate, "/stock/update")
api.add_resource(StockListDetail, "/stock/<code>")
api.add_resource(StockListFundamental, "/stock/<code>/fundamental")
api.add_resource(StockListData, "/stock/<code>/data/<start>/<end>")
api.add_resource(StockListSeed, "/stock/seed")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
