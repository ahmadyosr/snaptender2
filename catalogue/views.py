from django.shortcuts import render
from catalogue.models import Snippet 
from django.http import HttpResponseRedirect
from django.db.models import Q
import random
"""
Catalogue views 
"""
def labeling(request):
	context = {}
	label =	request.GET.get('label')
	tenders = Snippet.objects.filter(Q(is_tender=True) | Q(is_auction=True))

	context['done'] = tenders.exclude(category='').count()
	context['remaining'] = tenders.filter(category='').count()

	if request.GET.get('remove_last_tender'):
		id_ = request.session['last_tender']
		Snippet.objects.filter(id=id_).update(category='')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))	

	
	if label:
		id_ = request.GET.get('tender_id')
		Snippet.objects.filter(id=id_).update(category=label)
		request.session['last_tender'] = id_
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	context['tender'] = random.choice(tenders.exclude(category='idk'))

	return render(request, 'index.html', context)

