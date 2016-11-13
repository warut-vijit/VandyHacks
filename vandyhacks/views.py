from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm

from retrieval import *
retrieval = Retrieval()

def default_view(request):
    #index(request, stockID, one month back, today);
    return None

def index(request, stock_id, start_date, end_date):
    stock_data = retrieval.hist_stock(stock_id, start_date, end_date)
    context = {'sectorList': retrieval.get_industries(), 'stock_data': stock_data}
    return render(request, 'base.html', context)

def search(self, s):
    
	return HttpResponse(s)