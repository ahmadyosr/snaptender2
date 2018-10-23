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
""" utility
"""

def split_to_papers(paper):

	output_path = os.path.join(settings.MEDIA_ROOT, 'pages/'+paper.file.name)
	paper_path = os.path.join(settings.NEWSPAPERS_POOL_PATH, paper.file.name)
	
	if not os.path.exists(output_path):
		os.makedirs(output_path)

	result = convert_from_path(paper_path, output_folder=output_path, thread_count=4, fmt='jpg')
	
	files = []
	for i,f in enumerate(result): 
		files += [NewspaperPage(page_no=i, newspaper=paper, image=f.filename)]
		
	NewspaperPage.objects.bulk_create(files)

	return result

def extract_paper(paper):
	if paper.is_extracted:
		return 
		
	pages = NewspaperPage.objects.filter(newspaper=paper)
	

	for p in pages : 
		print('enter page')
		extractor = BoxesExtractor(p.image.path)
		extractor.extract()

		snippets = []
		rectangles = extractor.save_rectangles(settings.SNIPPETS_POOL_PATH)

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

def tenders(request):
	context = {} 
	context['tenders'] = Snippet.objects.filter(is_tender=True)
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
	return render(request, 'newspaper.html', context)

def newspapers(request):
	context = {} 
	newspapers = Newspaper.objects.all().order_by('-id')
	context['pdfs'] = newspapers
	context['pdfs_count'] = newspapers.count()
	context['extracted_pdfs_count'] = newspapers.filter(is_extracted=True).count()
	context['splitted_pdfs_count'] = newspapers.filter(is_splitted=True).count()
	context['files_count'] = len(os.listdir(settings.NEWSPAPERS_POOL_PATH))
	return render(request, 'newspapers.html', context)

def split_pdf(request):
	if request.GET.get('pdf_id'):
		paper = Newspaper.objects.get(id=request.GET.get('pdf_id'))

		if paper.is_splitted == True : 
			return HttpResponse('Paper %d already done' % paper.id )

		paper.is_splitted = True
		paper.save() 
		r = split_to_papers(paper)
		return HttpResponse(r)
 	
	newspapers = Newspaper.objects.filter(is_splitted=False)
	done = []

	for paper in newspapers : 
		s = time.time()
		split_to_papers(paper)
		paper.is_splitted = True
		paper.save() 
		done += [paper]
		print('time elapsed : ', time.time()-s)
	
	return HttpResponse(done)

def extract_snippets(request):
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
