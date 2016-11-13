import matplotlib.finance as fin
from datetime import datetime
import matplotlib.pyplot as plt
import requests

from bs4 import BeautifulSoup
from nltk import word_tokenize, tokenize
from nltk.corpus import stopwords

from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import names
from nltk.sentiment.util import *

import urllib
from bs4 import BeautifulSoup as bsoup

import time
import datetime as dt 

class Retrieval(object):

	api_key = '7f8c3783c4e3426995efbd57fd026831'

	def __init__(self):
		self.api_key = '7f8c3783c4e3426995efbd57fd026831'


	def get_industries(self):
	    industries = {}
	    r = urllib.urlopen('https://biz.yahoo.com/p/sum_conameu.html').read()
	    soup = bsoup(r, "html.parser")
	    for td in soup.find_all("td", bgcolor='ffffee'):
	        industries[td.find("a").find("font").text] = td.find("a")['href']
	    return industries


	def get_index(self,ext):
	    r = urllib.urlopen('https://biz.yahoo.com/p/'+ext).read()
	    soup = bsoup(r, "html.parser")
	    soup = soup.find_all('tr')[10:]  # 0 through 9 are headers
	    indices = {}
	    for tr in soup:
	        tds = tr.find_all('td')
	        symbol = tds[0].find_all('a')[1].text if len(tds[0].find_all('a')) > 1 else '[No symbol available]'
	        valuetxt = tds[2].find('font').text
	        if not valuetxt[0].isdigit():
	            value = 0
	        elif valuetxt[-1] == 'B':
	            value = float(valuetxt[:-1])*1000
	        else:
	            value = float(valuetxt[:-1])
	        indices[symbol] = value
	    indices = sorted(indices.items(), key=lambda (k, v): (v, k), reverse=True)
	    weight_total = sum([pair[1] for pair in indices[:5]])
	    indices = [(index[0], index[1]/weight_total) for index in indices]
	    return indices[:5]



	def hist_stock(self,symbol, start_date, end_date):
	    #  returns array of tuples (date, year, month, day, d, open, close, high, low, volume, adjusted_close)
	    stock = [(x[0], x[6]) for x in fin.quotes_historical_yahoo_ochl(symbol, start_date, end_date, asobject=True)]
	    return stock


	def plot_stock(self,hist_data):
	    plt.plot([x[0] for x in hist_data], [x[1] for x in hist_data])
	    plt.ylabel("Closing Price ($)")
	    plt.title("Closing Prices")
	    plt.tight_layout()
	    plt.show()


	def get_news(self, y, m, d, q):
	    #NYT API
	    url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?'
	    params = {
	        'api-key': self.api_key,
	        'facet_field': 'day_of_week',
	        'facet_fiter': 'true',
	        'type_of_material': 'News',
	        'q' : str(q),
	        'begin_date': str(y)+("0"+str(m))[-2:]+("0"+str(d))[-2:],
	        'end_date': str(y)+("0"+str(m))[-2:]+("0"+str(d))[-2:]
	    }
	    for param in params:
	        url += param+'='+params[param]+'&'

	    test = requests.get(url[:-1])

	    #Error messages of data is not found
	    if ('status' not in test.json()):
	        print('API Exceeded')
	        return None
	    if(test.json()['status'] == "ERROR" ):
	    	print('No data points found')
	        return None

	    print "\nThere should be a value of test here\n"

	    response = test.json()['response']['docs']
	    headlines = []
	    for doc in response:
	        if doc['lead_paragraph'] is not None:
	            headlines.append(doc['lead_paragraph'])
	    return headlines


	def sentiment_analysis(self,headlines):
	    #removes stop words from headline
	    stop_words = list(stopwords.words('english'))
	    headlines_without_stop_words = []
	    for headline in headlines:
	         tokens = word_tokenize(headline)
	         tokens_without_stop_words = [t for t in tokens if t not in stop_words]
	         stopwordless_headline = ""
	         for word in tokens_without_stop_words:
	            stopwordless_headline += word + " "
	         headlines_without_stop_words += [stopwordless_headline] 
	 
	    #runs sentiment analysis on the headlines and prints it out
	    sid = SentimentIntensityAnalyzer()
	    total_compoud_value_for_day = 0
	    for i in range(len(headlines_without_stop_words)):
	        sentences = tokenize.sent_tokenize(headlines_without_stop_words[i])
	        for sentence in sentences:
	            ss = sid.polarity_scores(sentence)
	            total_compoud_value_for_day += ss['compound']
	            # for k in sorted(ss):
	            #     print '{0}: {1}, '.format(k, ss[k]),
	            # print("\n")
	    if (len(headlines_without_stop_words) != 0):
	        return total_compoud_value_for_day/len(headlines_without_stop_words)
	    else:
	        return 0


	def hist_to_date(self, start_date, end_date, query):
	    days = []
	    sentiments = []

	    d = start_date
	    delta = dt.timedelta(days=1)

	    while d <= end_date:
	        headlines = self.get_news( d.year, d.month, d.day, query)
	        if (headlines != None):
	            sentiment = self.sentiment_analysis(headlines)
	            days += [d]
	            sentiments += [sentiment]
	        d += delta
	        time.sleep(0.5)
	    return zip(days, sentiments)


   
