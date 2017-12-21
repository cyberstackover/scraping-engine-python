# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
import string
import requests
import feedparser
from pprint import pprint
from ..models import NewsModel
from ..schema import news_schema
from .. import db, app
from sqlalchemy.orm import scoped_session, sessionmaker
import re
from time import mktime
from datetime import datetime
import datetime
from bs4 import BeautifulSoup
import requests

def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def parse_site(sites):

    site_list = {
        "tempo": "https://rss.tempo.co/",
        "antara": "https://www.antaranews.com/rss/terkini",
        "cnn": "http://rss.cnn.com/rss/cnn_latest.rss",
        "huffington": "https://www.huffingtonpost.com/section/front-page/feed",
        "nytimes": "http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "foxnews": "http://feeds.foxnews.com/foxnews/latest",
        "cnbc": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        "wsj": "http://www.wsj.com/xml/rss/3_7085.xml",
        "guardian": "https://www.theguardian.com/uk/rss",
        "chinadaily": "http://www.chinadaily.com.cn/rss/china_rss.xml",
        "dw": "http://rss.dw.com/rdf/rss-en-all",
        "rt": "https://www.rt.com/rss/news/",
        "yahoo": "https://www.yahoo.com/news/rss/list",
        "google": "https://news.google.com/news/rss/?ned=id_id&gl=ID&hl=id",
        "kompas": "https://news.google.com/news/rss/search/section/q/kompas.com/kompas.com?hl=id&gl=ID&ned=id_id"
    }
    

    for site in sites:
        if site == "ipotnews":
            get_ipotnews()
        else:
            site_url = site_list[site]
            data = feedparser.parse(site_url)

            print("Fetching {} ...".format(site))
            save_data(data, site)

def save_data(data, site):
    entries = data.get("entries")

    latest = NewsModel.query.filter_by(src=site).order_by(NewsModel.id.desc()).limit(1000).all()
    dumped_data = news_schema.dump(latest).data
    latest_list = list(map(lambda i: i.get("title"), dumped_data))

    printable = set(string.printable)
    for entry in entries:        
        if entry.get("title") not in latest_list:
            if entry.get("published_parsed") is not None:
                published = datetime.datetime.fromtimestamp(mktime(entry.get("published_parsed")))
            else:
                published = None

            news = NewsModel(
                title=''.join(x for x in entry.get('title') if x in printable),
                url=''.join(x for x in entry.get('link') if x in printable),
                lead=''.join(x for x in cleanhtml(entry.get('summary')) if x in printable),
                src=site,
                date_published=published
            )
            news.save_to_db()
            
def get_ipotnews():
    base_url = "https://www.indopremier.com/ipotnews/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "lxml")
    news = soup.select("div.keeptogether")

    for item in news:
        data = item.select("dl.listNews")[0]

        published = data.find("small").getText().replace(" WIB", "")
        d = datetime.datetime.strptime(published, "%A, %b %d, %Y - %H:%M")
        published = datetime.date.strftime(d, "%Y-%m-%d %H:%M:00")

        link = "{}{}".format(base_url, data.find("a", href=True).get("href"))
        title = data.find("a", href=True).getText()

        news = NewsModel(
            title=title,
            url=link,
            src='ipotnews',
            date_published=published
        )
        news.save_to_db()
        
        
        
        
        
        