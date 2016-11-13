from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
# from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
# from reportlab.pdfgen import canvas

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
    return HttpResponse("Hello, world. You're at the polls index.")

def search(self, s):
	return HttpResponse(s)