from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
	return HttpResponse("Search page!")

def result(request, druga, drugb):
	return HttpResponse("Drug A: %s. Drug B: %s." % (druga, drugb))


