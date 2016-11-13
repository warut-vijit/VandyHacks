from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm

from retrieval import *
retrieval = Retrieval()

def graph_view(request, stock_id):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# def search(query, startdate, enddate):
# 	date = startdate.split()
# 	return date
def index(request):
    context = {'sectorList': retrieval.get_industries()}
    return render(request, 'base.html', context)

def search(self, s):
	return HttpResponse(s)