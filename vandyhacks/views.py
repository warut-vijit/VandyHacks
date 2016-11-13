from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
import datetime as dt 

from retrieval import *
retr = Retrieval()

month_to_number = {"january":1, "february":2, "march":3, "april":4, "may":5 , "june":6, "july":7, "august":8, "september":9, "october":10, "november":11, "december":12}

def default(request):
    index(request, "MSTR", datetime(2016, 10, 13), datetime(2016, 11, 12));
    return None

#@DUKE to put this in the base.html file, you'll want to use

#{% if sentiment_data in graph_data %}

#to check if the information given contains sentiment data or not.
#to access stock data you'll need to do {{graph_data.stock_data**}} where  ** is however you access the data in retrieval.py ([i] or .apple or whatever)

def index(request, stock_id, start_date, end_date, sentiment = None):
    stock_data = retr.hist_stock(stock_id, start_date, end_date)
    if (sentiment == None):
        context = {'sectorList': retr.get_industries(), 'graph_data' : {'stock_data': stock_data}}
    else:
        context = {'sectorList': retr.get_industries(), 'graph_data' : {'stock_data': stock_data, 'sentiment_data': sentiments}}
    return render(request, 'base.html', context)

def industry(request, u):
    industry_data =  retr.get_index(u)
    context = {'sectorList': retr.get_industries(), 'graph_data' : {'stock_data': stock_data, 'sentiment_data': sentiments}}

def search(self, request, s):
	sentiment_input = s.split(' ')

	if len(sentiment_input) == 7 and sentiment_input[0] == "sentiments":
		startdate = datetime(int(sentiment_input[4]),int( month_to_number[sentiment_input[3]]),1)
		print("HELLO" + str(type(startdate)))
		enddate = datetime(int(sentiment_input[6]),int( month_to_number[sentiment_input[5]]),1)
		sentiment_data = retr.hist_to_date(startdate,enddate,sentiment_input[1])
        index(request, sentiment_input[2], start_date, end_date, sentiment_data)
	if len(sentiment_input) == 5:
		startdate = datetime(int(sentiment_input[2]),int( month_to_number[sentiment_input[1]]),1)
		enddate = datetime(int(sentiment_input[4]),int( month_to_number[sentiment_input[3]]),1)
		index(request, sentiment_input[0], startdate, enddate)
	
	return None

