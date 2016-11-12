import matplotlib.finance as fin
from datetime import datetime
import matplotlib.pyplot as plt
import requests
import urllib
from bs4 import BeautifulSoup as bsoup


api_key = 'ea79de4994b64abdaf8520b0a878495a'


def get_industries():
    industries = {}
    r = urllib.urlopen('https://biz.yahoo.com/p/sum_conameu.html').read()
    soup = bsoup(r, "html.parser")
    for td in soup.find_all("td", bgcolor='ffffee'):
        industries[td.find("a").find("font").text] = td.find("a")['href']
    return industries


def get_index(ext):
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


def hist_stock(symbol, start_date, end_date):
    #  returns array of tuples (date, year, month, day, d, open, close, high, low, volume, adjusted_close)
    stock = [(x[0], x[6]) for x in fin.quotes_historical_yahoo_ochl(symbol, start_date, end_date, asobject=True)]
    return stock


def plot_stock(hist_data):
    plt.plot([x[0] for x in hist_data], [x[1] for x in hist_data])
    plt.ylabel("Closing Price ($)")
    plt.title("Closing Prices")

    plt.tight_layout()
    plt.show()


def get_news(y, m, d):
    # NYT API
    url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?'
    params = {
        'api-key': api_key,
        'facet_field': 'day_of_week',
        'facet_fiter': 'true',
        'type_of_material': 'News',
        'begin_date': str(y)+str(m)+str(d),
        'end_date': str(y)+str(m)+str(d)
    }
    for param in params:
        url += param+'='+params[param]+'&'

    test = requests.get(url[:-1])
    response = test.json()['response']['docs']
    headlines = []
    for doc in response:
        if doc['lead_paragraph'] is not None:
            headlines.append(doc['lead_paragraph'])
    return headlines


#headlines = get_news('2015', '06', '07')
#for headline in headlines:
#    print headline
#stocks_jan0116 = hist_stock('ATVI.MX', datetime(2016, 1, 1), datetime(2016, 9, 7))
#plot_stock(stocks_jan0116)
inds = get_industries()  # returns industries and url extensions
print get_index(inds[inds.keys()[1]])
