from django.shortcuts import render
from catalogue.models import Snippet 

"""
Catalogue views 
"""
def index(request):
	context = {}
	context['tenders'] = Snippet.objects.all()

	return render(request, 'index.html', context)

