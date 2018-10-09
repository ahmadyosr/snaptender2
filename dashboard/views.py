from django.shortcuts import render
from catalogue.models import Newspaper
from django.conf import settings 
from django.http import HttpResponse
import os 
"""
Catalogue views 
"""
def tenders(request):
	context = {} 
	newspapers = Newspaper.objects.all()
	context['pdfs'] = newspapers
	context['pdfs_count'] = newspapers.count()
	context['processed_pdfs_count'] = newspapers.filter(is_processed=True).count()
	context['files_count'] = len(os.listdir(settings.NEWSPAPERS_POOL_PATH))
	return render(request, 'tables.html', context)

def extract_snippets(request):
	if request.GET.get('pdf_id'):
		pass
	# else -> continue
	x = Newspaper.objects.filter(is_processed=False)
	
	return HttpResponse('done')
def import_pdfs_dir(request):
	newspapers = Newspaper.objects.all()

	folder = settings.NEWSPAPERS_POOL_PATH
	files = os.listdir(folder)

	to_populate = [] 
	for i, f in enumerate(files) : 
		if not newspapers.filter(file = f).exists():
			print(f)
			to_populate += [Newspaper(file=f)] 

	r= Newspaper.objects.bulk_create(to_populate)
	return HttpResponse('created %d newspaper' % len(r))
	# return HttpResponseRedirect(request.META.get('HTTP_REFERER'))