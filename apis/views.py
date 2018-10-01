from django.shortcuts import render

# Create your views here.
def tenders_list(request, format=None):
	if request.method == 'GET':
		tenders = TenderSnippet.objects.all()
		args = [request]
		serializer = TenderSnippetSerializer(tenders, many=True)
		return JsonResponse(serializer.data, safe=False)
