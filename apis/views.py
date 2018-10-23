from django.shortcuts import render
from catalogue.models import Snippet 
from catalogue.serializers import TenderSnippetSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.conf import settings

# Create your views here.
def tenders_list(request, format=None):
	if request.method == 'GET':
		tenders = Snippet.objects.all()
		args = [request]
		serializer = TenderSnippetSerializer(tenders, many=True)
		return JsonResponse(serializer.data, safe=False)
