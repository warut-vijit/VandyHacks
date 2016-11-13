from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
import datetime as dt 

from retrieval import *
retr = Retrieval()

month_to_number = {"january":1, "february":2, "march":3, "april":4, "may":5 , "june":6, "july":7, "august":8, "september":9, "october":10, "november":11, "december":12}

def default_view(request):
    #index(request, stockID, one month back, today);
    return None

def index(request, stock_id, start_date, end_date):
    stock_data = retrieval.hist_stock(stock_id, start_date, end_date)
    context = {'sectorList': retrieval.get_industries(), 'stock_data': stock_data}
    return render(request, 'base.html', context)


def search(self, s):
	sentiment_input = s.split(' ')

	if len(sentiment_input) == 6 and sentiment_input[0] == "sentiments":
		startdate = datetime(int(sentiment_input[3]),int( month_to_number[sentiment_input[2]]),1)
		print("HELLO" + str(type(startdate)))
		enddate = datetime(int(sentiment_input[5]),int( month_to_number[sentiment_input[4]]),1)
		plot = retr.hist_to_date(startdate,enddate,sentiment_input[1])
	if len(sentiment_input) == 5:
		startdate = datetime(int(sentiment_input[2]),int( month_to_number[sentiment_input[1]]),1)
		enddate = datetime(int(sentiment_input[4]),int( month_to_number[sentiment_input[3]]),1)
		plot = retr.hist_to_date(startdate,enddate,sentiment_input[1])
	
	return HttpResponse(plot)

