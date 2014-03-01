from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from healthhive.models import SearchQuery

#from healthhive.models import ActiveIngredient

def index(request):
	return HttpResponseRedirect("/search/")

def search(request):
	return render(request, 'healthhive/search.html')

def submit(request):
	dra = request.POST['druga']
	drb = request.POST['drugb']
	search = SearchQuery(druga=dra, drugb=drb)
	search.save()
	return render(request, 'healthhive/result.html', {
        'druga' : dra,
        'drugb' : drb,
    })

def result(request, druga, drugb):
	context = {
		'druga' : druga,
		'drugb' : drugb
		}
	return render(request, 'healthhive/result.html', context)


