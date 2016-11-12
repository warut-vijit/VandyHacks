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

import datetime as dt 



api_key = 'ea79de4994b64abdaf8520b0a878495a'


def hist_stock(symbol, start_date, end_date):
    #  returns array of tuples (date, year, month, day, d, open, close, high, low, volume, adjusted_close)
    
    stock = [(x[0], x[6]) for x in fin.quotes_historical_yahoo_ochl(symbol, start_date, end_date, asobject=True)]
    return stock


def plot_stock(hist_data):
    print(hist_data)
    plt.plot([x[0] for x in hist_data], [x[1] for x in hist_data])
    plt.ylabel("Closing Price ($)")
    plt.title("Closing Prices")
    plt.tight_layout()
    plt.show()


def get_news(y, m, d, q):
    #NYT API
    url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?'
    params = {
        'api-key': api_key,
        'facet_field': 'day_of_week',
        'facet_fiter': 'true',
        'type_of_material': 'News',
        'q' : str(q),
        'begin_date': str(y)+str(m)+str(d),
        'end_date': str(y)+str(m)+str(d)
    }
    for param in params:
        url += param+'='+params[param]+'&'

    test = requests.get(url[:-1])
    # print(test.json())
    if('status' not in test.json() or test.json()['status'] == "ERROR" ):
        return None
    else:
        print('passed')

    response = test.json()['response']['docs']
    headlines = []
    for doc in response:
        if doc['lead_paragraph'] is not None:
            headlines.append(doc['lead_paragraph'])
    return headlines


def sentiment_analysis(headlines):
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
            # print(sentence)
            ss = sid.polarity_scores(sentence)
            total_compoud_value_for_day += ss['compound']
            # for k in sorted(ss):
            #     print '{0}: {1}, '.format(k, ss[k]),
            # print("\n")
    return total_compoud_value_for_day/len(headlines_without_stop_words)

    # return tokens


def hist_to_date(start_date, end_date, query):
    days = []
    sentiments = []

    d = start_date
    delta = dt.timedelta(days=1)
    while d <= end_date:
        headlines = get_news(d.year, d.month, d.day, query)
        if (headlines != None):
            sentiment = sentiment_analysis(headlines)
            days += [d]
            sentiments += [sentiment]
        d += delta
    print(days)
    print(sentiments)
    return zip(days, sentiments)
   


    return "hi"


headlines = get_news('2016', '11', '11', 'Apple Inc')
sentiment_analysis(headlines)
information = hist_to_date(datetime(2016, 1, 1), datetime(2016, 1, 5), 'trump')
plot_stock(information)

# print(headlines)
# for headline in headlines:
#     print headline
# stocks_jan0116 = hist_stock('AAPL', datetime(2016, 1, 1), datetime(2016, 9, 7))
# plot_stock(stocks_jan0116)
