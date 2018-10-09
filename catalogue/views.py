from django.shortcuts import render
from catalogue.models import TenderSnippet 

"""
Catalogue views 
"""
def index(request):
	context = {}
	context['tenders'] = TenderSnippet.objects.all()

	return render(request, 'index.html', context)

