from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
import datetime as dt 

from retrieval import *
retr = Retrieval()

month_to_number = {"january":1, "february":2, "march":3, "april":4, "may":5 , "june":6, "july":7, "august":8, "september":9, "october":10, "november":11, "december":12}

def default(request):
    data = retr.hist_stock('AAPL', datetime(2016, 1, 1), datetime(2016, 9, 7))
    context = {'sectorList': [], 'graph_data' : {'stock_data': data}}
    return render( request, 'base.html', context)

#@DUKE to put this in the base.html file, you'll want to use

#{% if sentiment_data in graph_data %}

#to check if the information given contains sentiment data or not.
#to access stock data you'll need to do {{graph_data.stock_data**}} where  ** is however you access the data in retrieval.py ([i] or .apple or whatever)

# def index(stock_id, start_date, end_date, sentiment = None):
#     stock_data = retr.hist_stock(stock_id, start_date, end_date)
#     if (sentiment == None):
#         context = {'sectorList': retr.get_industries(), 'graph_data' : {'stock_data': stock_data}}
#     else:
#         context = {'sectorList': retr.get_industries(), 'graph_data' : {'stock_data': stock_data, 'sentiment_data': sentiments}}
#     return render( 'base.html', context)


def base(request):
	data = hist_stock('AAPL', datetime(2016, 1, 1), datetime(2016, 9, 7))
	context = {'sectorList': [], 'graph_data' : {'stock_data': data}}
	return render( request, 'base.html', context)



def search(request, s):
	sentiment_input = s.split(' ')

	if len(sentiment_input) == 8:
		startdate = datetime(int(sentiment_input[4]),int( month_to_number[sentiment_input[2]]),int(sentiment_input[3]))
		enddate = datetime(int(sentiment_input[7]),int( month_to_number[sentiment_input[5]]),int(sentiment_input[6]))
		sentiment_data = retr.hist_to_date(startdate,enddate,sentiment_input[1])
		data = retr.hist_stock(sentiment_input[1], startdate, enddate )
		context = {'sectorList': [], 'graph_data' : {'stock_data': data, 'sentiment_data': sentiment_data}}
		# return render_to_response("base.html", context)
		return render( request, 'base.html', context)

	if len(sentiment_input) == 7:

		startdate = datetime(int(sentiment_input[3]),int( month_to_number[sentiment_input[1]]),int(sentiment_input[2]))
		enddate = datetime(int(sentiment_input[6]),int( month_to_number[sentiment_input[4]]),int(sentiment_input[5]))
	
		data = retr.hist_stock(sentiment_input[0], startdate, enddate)
		
		# context = {'sectorList': retr.get_industries()[:10], 'graph_data' : {'stock_data': data}}
		context = {'sectorList':[], 'graph_data' : {'stock_data': data}}
		# return render_to_response("search.html", context)
		# print("\nHERE\n")
		return render( request, 'search.html', context)

	return HttpResponse( "We fucked up")

