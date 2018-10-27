from django.shortcuts import render
from catalogue.models import Newspaper, NewspaperPage, Snippet
import datetime
from django.conf import settings 
from django.http import HttpResponse, HttpResponseRedirect
import os 
import time 
from modules.extractors import BoxesExtractor
from modules.splitter import split
from pdf2image import convert_from_path
from catalogue.forms import NewspaperForm

""" utility
"""
def split_to_papers(paper):
	paper_name = paper.file.name.split('/')[-1]
	output_path = os.path.join(settings.NEWSPAPERS_PAGES_DIR, paper_name)
	
	if not os.path.exists(output_path):
		os.makedirs(output_path)

	result = convert_from_path(paper.file.path, output_folder=output_path, thread_count=4, fmt='jpg')
	
	files = []
	for i,f in enumerate(result):
		img_name = f.filename.split('/')[-1]
		file_name_ = os.path.join(settings.NEWSPAPERS_PAGES_DIR_NAME, paper_name, img_name)
		files += [NewspaperPage(page_no=i, newspaper=paper, image=file_name_)]
		
	NewspaperPage.objects.bulk_create(files)

	return files

def extract_paper(paper):
	if paper.is_extracted:
		return 
		
	pages = NewspaperPage.objects.filter(newspaper=paper)
	

	for p in pages : 
		print('enter page')
		extractor = BoxesExtractor(p.image.path)
		extractor.extract()

		snippets = []
		# rectangles = extractor.save_rectangles(settings.SNIPPETS_POOL_PATH)

		for r, bw_rate in rectangles:
			s = Snippet(newspaper=paper,
					 page = p,
					 extract_date=datetime.date.today(), 
					 image=r, 
					 bw_rate=bw_rate)
			snippets += [s]

		if rectangles : 
			p.is_extracted = True
			p.has_rectangles = True
			p.save() 

		Snippet.objects.bulk_create(snippets)			

	paper.is_extracted = True
	paper.save()
	print('done paper id %d ', paper.id)

"""
Catalogue views 
"""

def dashboard(request):
	context = {}
	return render(request, 'dashboard.html', context)

def upload(request):
	papers = [] 

	for f in request.FILES.getlist('file'):
		p = Newspaper(file=f)
		p.save()
		papers += [p]

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_newspaper(request, paper_id):
	if request.method == 'POST': 
		Newspaper.objects.get(id=paper_id).delete()

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def snippets(request):
	context = {} 
	filter_ = request.GET.get('filter')

	if filter_ == 'tenders': 
		snippets = Snippet.objects.filter(is_tender=True)

	elif filter_ == 'not-tenders':
		snippets = Snippet.objects.filter(is_tender=False)

	elif filter_ == 'has-text': 
		snippets = Snippet.objects.exclude(text='')

	elif filter_ == 'no-text': 
		snippets = Snippet.objects.filter(text='')

	else : 
		snippets = Snippet.objects.filter(is_tender=True)

	
	context['snippets']= snippets

	return render(request, 'tenders.html', context)

def toggle_acceptance(request, tender_id):
	t = Snippet.objects.get(id=tender_id)
	Snippet.objects.filter(id=tender_id).update(is_tender= not t.is_tender)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def newspaper(request, paper_id):
	context = {}
	snippets = Snippet.objects.all().filter(newspaper=paper_id)
	context['paper'] = Newspaper.objects.get(id=paper_id)
	context['pages'] = NewspaperPage.objects.filter(newspaper=paper_id)
	context['snippets'] = snippets.filter(is_tender=False)
	context['tenders'] = snippets.filter(is_tender=True)
	print(context['pages'])
	return render(request, 'newspaper.html', context)

def newspapers(request):
	context = {} 
	newspapers = Newspaper.objects.all().order_by('-id')
	context['pdfs'] = newspapers
	context['pdfs_count'] = newspapers.count()
	context['extracted_pdfs_count'] = newspapers.filter(is_extracted=True).count()
	context['splitted_pdfs_count'] = newspapers.filter(is_splitted=True).count()
	# context['files_count'] = len(os.listdir(settings.NEWSPAPERS_POOL_PATH))
	return render(request, 'newspapers.html', context)

def split_paper(request, paper_id):

	if request.method == 'POST':
		paper = Newspaper.objects.get(id=paper_id)

		if paper.is_splitted == True : 
			return HttpResponse('Paper %d already done' % paper.id )

		r = split_to_papers(paper)
		paper.is_splitted = True
		paper.save() 

		return HttpResponse(r)

	return HttpResponse(status=403)	

def extract_paper(request, paper_id):
	if request.GET.get('page_id'):
		paper = Newspaper.objects.get(id=request.GET.get('pdf_id'))

		if paper.is_extracted == True : 
			return HttpResponse('Paper %d already done' % paper.id )

		extract_paper(paper)
		return HttpResponse('Done')
	
	newspapers = Newspaper.objects.filter(is_extracted=False)

	for paper in newspapers :
		extract_paper(paper)

	return HttpResponse('done')

