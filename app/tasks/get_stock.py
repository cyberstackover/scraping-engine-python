from bs4 import BeautifulSoup
import requests
from config.config import app_config
import os
from ..models import StockList, StockListHistory
import time
import re
import datetime
from dateutil.relativedelta import relativedelta

key = os.environ['FLASK_CONFIG']
base_url = app_config[key].BASE_URL

def stock_list():

	source = requests.get("http://www.seputarforex.com/saham/daftar_emiten/")
	soup = BeautifulSoup(source.text, "lxml")

	table = soup.find("table", {"class": "font_general"})

	code_list = []
	for item in table.find_all("tr"):
		code = item.select("td")[1].getText().lstrip().rstrip()
		company = item.select("td")[2].getText().lstrip().rstrip()
		now = datetime.datetime.now()
		today = datetime.date.today()
		end = datetime.date(day=today.day, month=today.month, year=today.year)
		start = end - relativedelta(days=7)
		code_list.append({
			"code": code,
			"company": company,
			"link": "{}/stock/{}".format(base_url, code),
			"data": "{}/stock/{}/data/{}/{}".format(base_url, code, start, end),
			"fundamental_data": "{}/stock/{}/fundamental".format(base_url, code)
		})

	code_list.pop(0)

	return code_list

def data(code, start, end):
	urlf = "https://finance.yahoo.com/quote/{}.JK/history".format(code)
	r = requests.get(urlf)
	txt = r.text
	cookie = r.cookies['B'] # the cooke we're looking for is named 'B'
	pattern = re.compile('.*"CrumbStore":\{"crumb":"(?P<crumb>[^"]+)"\}')
	for line in txt.splitlines():
		m = pattern.match(line)
		if m is not None:
			crumb = m.groupdict()['crumb']

	start = datetime.datetime.strptime("{} 00:00:00".format(start), "%Y-%m-%d %H:%M:%S").strftime("%s")
	end = datetime.datetime.strptime("{} 23:23:59".format(end), "%Y-%m-%d %H:%M:%S").strftime("%s")
	url = "https://query1.finance.yahoo.com/v7/finance/download/{}.JK?period1={}&period2={}&interval=1d&events=history&crumb={}".format(code, start, end, crumb)

	print(url)
	data = requests.get(url, cookies={'B':cookie})
	data = data.text.split("\n")
	data.pop(0)

	result = []
	for item in data:
		item = item.split(",")
		try:
			result.append({
				"date": item[0],
				"open": item[1],
				"high": item[2],
				"low": item[3],
				"close": item[4],
				"adj_close": item[5],
				"volume": item[6]
			})
		except:
			pass

	return result

def metadata(code):
	url = "https://www.indopremier.com/module/saham/companyprofile/ComProTemplate.php?code={}".format(code)
	source = requests.get(url)
	soup = BeautifulSoup(source.text, "lxml")

	data = []
	tables = soup.find_all("table")
	contact = []
	contact.append({
		"office": tables[0].find("p").getText()
	})
	for item in tables[0].find("tbody").find_all("tr"):
		tds = item.find_all("td")
		contact.append({
			tds[0].getText(): tds[2].getText()
		})
	data.append({
		"contact": contact
	})

	profile = tables[1].find("tbody").find("p").getText()
	data.append({
		"profile": profile
	})

	shares = []
	for share in tables[2].find("tbody").find_all("tr"):
		tds = share.find_all("td")
		shares.append({
			tds[0].getText(): tds[2].getText()
		})
	data.append({
		"shares": shares
	})

	bocs = []
	for boc in tables[3].find("tbody").find_all("tr"):
		tds = boc.find_all("td")
		bocs.append({
			tds[0].getText(): tds[2].getText()
		})
	data.append({
		"bocs": bocs
	})

	bods = []
	for bod in tables[4].find("tbody").find_all("tr"):
		tds = bod.find_all("td")
		bods.append({
			tds[0].getText(): tds[2].getText()
		})
	data.append({
		"bods": bods
	})

	ipos = []
	for idx, ipo in enumerate(tables[5].find("tbody").find_all("tr")):
		tds = ipo.find_all("td")
		if idx == 2:
			lis = tds[2].find_all("li")
			if len(lis) > 0:
				list_ = []
				for li in lis:
					list_.append(li.getText())
			else:
				list_ = tds[2].getText()
			ipos.append({
				"underwriter": list_
			})
		else:
			ipos.append({
				tds[0].getText(): tds[2].getText()
			})
	data.append({
		"ipo": ipos
	})

	history = []
	for item in tables[6].find("tbody").find_all("tr"):
		tds = item.find_all("td")
		history.append({
			"type": tds[1].getText(),
			"shares": tds[2].getText(),
			"listing_date": tds[3].getText(),
			"trading_date": tds[4].getText()
		})
	data.append({
		"issued_history": history
	})

	return data

def fundamental(code):
	url = "https://www.indopremier.com/module/saham/include/fundamental.php?code={}&quarter=".format(code)
	source = requests.get(url)
	soup = BeautifulSoup(source.text, "lxml")

	table = soup.find("table")
	trs = table.find("tbody").find_all("tr")
	last_price = trs[0].find_all("td")[1].getText()
	share_out = trs[1].find_all("td")[1].getText()
	marketcap = trs[2].find_all("td")[1].getText()
	asset = trs[5].find_all("td")[1].getText()
	stb = trs[6].find_all("td")[1].getText()
	ltb = trs[7].find_all("td")[1].getText()
	equity = trs[8].find_all("td")[1].getText()
	revenue = trs[10].find_all("td")[1].getText()
	profit = trs[13].find_all("td")[1].getText()
	ebitda = trs[14].find_all("td")[1].getText()
	eps = trs[17].find_all("td")[1].getText()
	per = trs[18].find_all("td")[1].getText()
	roe = trs[22].find_all("td")[1].getText()
	der = trs[24].find_all("td")[1].getText()

	data = {
		"last_price": last_price,
		"share_out": share_out,
		"market_cap": marketcap,
		"assets": asset,
		"st_debt": stb,
		"lt_debt": ltb,
		"equity": equity,
		"revenue": revenue,
		"net_profit": profit,
		"ebitda": ebitda,
		"eps": eps,
		"per": per,
		"roe": roe,
		"der": der,
	}

	return data

def update():
	return ""

def seeddb(update=False):
	source = requests.get("http://www.seputarforex.com/saham/daftar_emiten/")
	soup = BeautifulSoup(source.text, "lxml")

	table = soup.find("table", {"class": "font_general"})

	code_list = []
	parsed = table.find_all("tr")
	parsed.pop(0)

	urlf = "https://finance.yahoo.com/quote/TLKM.JK/history"
	r = requests.get(urlf)
	txt = r.text
	cookie = r.cookies['B'] # the cooke we're looking for is named 'B'
	pattern = re.compile('.*"CrumbStore":\{"crumb":"(?P<crumb>[^"]+)"\}')
	for line in txt.splitlines():
		m = pattern.match(line)
		if m is not None:
			crumb = m.groupdict()['crumb']


	for item in parsed:
		code = item.select("td")[1].getText().lstrip().rstrip()
		company = item.select("td")[2].getText().lstrip().rstrip()

		is_exist = StockList.query.filter_by(name=company).first()
		if is_exist is not None:
			continue

		print(company)
		stock_company = StockList(
			name=company,
			code=code
		)
		stock_company.save_to_db()

		if update:
			p1 = int(time.time())-172798
		else:
			p1 = 946684800

		url = "https://query1.finance.yahoo.com/v7/finance/download/{}.JK?period1={}&period2={}&interval=1d&events=history&crumb={}".format(code, p1, int(time.time()), crumb)

		print(url)
		data = requests.get(url, cookies={'B':cookie})
		os.environ['TZ']='UTC'
		p='%Y-%m-%d'

		data = data.text.split("\n")
		data.pop(0)

		# Date,Open,High,Low,Close,Adj Close,Volume
		for item in data:
			try:
				splitted = item.split(",")
				date_ = splitted[0]
				open_ = splitted[1]
				close = splitted[2]
				high = splitted[3]
				low = splitted[4]
				adj_close = splitted[5]
				volume = splitted[6]
				epoch = int(time.mktime(time.strptime(date_,p)))

				history = StockListHistory(
					stock_id = stock_company.id,
					date_published = epoch,
					open_value = open_,
					close_value = close,
					high_value = high,
					low_value = low,
					adj_close_value = adj_close,
					volume_value = volume
				)
				history.save_to_db()

			except:
				pass
