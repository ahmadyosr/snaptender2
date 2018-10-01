from django.shortcuts import render
from catalogue.models import TenderSnippet 
from catalogue.serializers import TenderSnippetSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.conf import settings

# Create your views here.
def index(request):
	context = {}
	context['tenders'] = TenderSnippet.objects.all()

	return render(request, 'index.html', context)

