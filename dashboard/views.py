from django.urls import reverse 

from django.shortcuts import render, redirect
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
from modules.ocr.ocr import  OceanOCR
import cv2
from django.db.models import Q
from django.contrib.auth import authenticate, login as contrib_login
from django.contrib.auth.decorators import login_required

""" utility
"""

def split_to_papers(paper):
	paper_name = paper.file.name.split('/')[-1]

	if not os.path.exists(settings.NEWSPAPERS_DATA_DIR):
		os.makedirs(settings.NEWSPAPERS_DATA_DIR)

	paper_dir = os.path.join(settings.NEWSPAPERS_DATA_DIR , paper_name)
	
	if not os.path.exists(paper_dir):
		os.makedirs(paper_dir)

	pages_dir = os.path.join(paper_dir, settings.ANY_NEWSPAPERS_PAGES_DIR_NAME)
	
	if not os.path.exists(pages_dir):
		os.makedirs(pages_dir)

	result = convert_from_path(paper.file.path, output_folder=pages_dir, thread_count=4, fmt='jpg')
	
	files = []

	for i,f in enumerate(result):
		img_name = f.filename.split('/')[-1]

		file_name_ = os.path.join(settings.NEWSPAPERS_DATA_DIR_NAME,
						paper_name,
						settings.ANY_NEWSPAPERS_PAGES_DIR_NAME,
						img_name)

		files += [NewspaperPage(page_no=i, newspaper=paper, image=file_name_)]
		
	NewspaperPage.objects.bulk_create(files)

	return files


def get_page_rectangles(p):
	paper_name = p.newspaper.file.name.split('/')[-1]
	
	if not os.path.exists(settings.NEWSPAPERS_DATA_DIR):
		os.makedirs(settings.NEWSPAPERS_DATA_DIR)

	pages_dir = os.path.join(settings.NEWSPAPERS_DATA_DIR , paper_name)
	
	if not os.path.exists(pages_dir):
		os.makedirs(pages_dir)

	snippets_dir = os.path.join(pages_dir, settings.ANY_NEWSPAPERS_SNIPPETS_DIR_NAME)
	
	if not os.path.exists(snippets_dir):
		os.makedirs(snippets_dir)

	extractor = BoxesExtractor(p.image.path)
	extractor.extract()


	rectangles = extractor.save_rectangles(snippets_dir)
	snippets = []

	for file_name, bw_rate in rectangles:
		file_name_ = os.path.join(settings.NEWSPAPERS_DATA_DIR_NAME,
								paper_name,
								settings.ANY_NEWSPAPERS_SNIPPETS_DIR_NAME,
								file_name)

		s = Snippet(newspaper=p.newspaper,
				 page = p,
				 extract_date=datetime.date.today(), 
				 image=file_name_, 
				 bw_rate=bw_rate*100)
		
		snippets += [s]

	return snippets

def extract_paper_(paper):
	if paper.is_extracted:
		return 

	pages = NewspaperPage.objects.filter(newspaper=paper)
	paper_snippets = [] 	

	for p in pages : 
		snippets = get_page_rectangles(p)
		
		if snippets : 
			p.has_snippets = True
			p.save() 

		Snippet.objects.bulk_create(snippets)			
		paper_snippets += snippets

	return paper_snippets 
"""
Catalogue views 
"""
@login_required(login_url='/dashboard/login/')
def dashboard(request):
	context = {}
	return render(request, 'dashboard.html', context)


@login_required(login_url='/dashboard/login/')
def upload(request):
	papers = [] 

	for f in request.FILES.getlist('file'):
		p = Newspaper(file=f)
		p.save()
		papers += [p]

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/dashboard/login/')
def delete_newspaper(request, paper_id):
	if request.method == 'POST': 
		Newspaper.objects.get(id=paper_id).delete()

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/dashboard/login/')
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

@login_required(login_url='/dashboard/login/')
def toggle_acceptance(request, tender_id):
	t = Snippet.objects.get(id=tender_id)
	Snippet.objects.filter(id=tender_id).update(is_tender= not t.is_tender)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/dashboard/login/')
def approve_category(request, tender_id):
	t = Snippet.objects.get(id=tender_id)
	t.category = t.suggested_category 

	t.save()

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/dashboard/login/')
def newspaper(request, paper_id):
	context = {}
	snippets = Snippet.objects.all().filter(newspaper=paper_id)
	context['paper'] = Newspaper.objects.get(id=paper_id)
	context['pages'] = NewspaperPage.objects.filter(newspaper=paper_id)
	context['snippets'] = snippets.filter(is_tender=False)
	context['tenders'] = snippets.filter(Q(is_tender=True) | Q(is_auction=True))

	return render(request, 'newspaper.html', context)

@login_required(login_url='/dashboard/login/')
def newspapers(request):
	context = {} 
	context['pdfs'] = Newspaper.objects.all().order_by('-id')
	return render(request, 'newspapers.html', context)

@login_required(login_url='/dashboard/login/')
def split_paper(request, paper_id):

	if request.method == 'POST':
		paper = Newspaper.objects.get(id=paper_id)

		if paper.is_splitted == True : 
			return HttpResponse('Paper %d already done' % paper.id )

		r = split_to_papers(paper)
		paper.is_splitted = True
		paper.save() 

		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	return HttpResponse(status=403)	


@login_required(login_url='/dashboard/login/')
def extract_paper(request, paper_id):
	if request.method == 'POST':
		paper = Newspaper.objects.get(id=paper_id)

		if paper.is_extracted == True : 
			return HttpResponse('Paper %d already done' % paper.id )

		extract_paper_(paper)
		paper.is_extracted = True
		paper.save() 

		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	return HttpResponse(status=403)	

@login_required(login_url='/dashboard/login/')
def ocr_paper(request, paper_id):
	if request.method == 'POST':
		paper = Newspaper.objects.get(id=paper_id)
		snippets = paper.snippet_set.all()

		for s in snippets : 
			im_path = s.image.path
			size = os.stat(im_path).st_size 
			im = cv2.imread(im_path)
			if size > 1024000 : 
				continue
						
			try :
				s.text = OceanOCR.get_image_text(im)
				if s.text : 
					s.save()

			except Exception as e :
				print(str(e))
				with open('log.txt', 'w') as f:
					f.write(str(e))

		paper.is_ocr = True
		paper.save()			
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	return HttpResponse(status=403)


@login_required(login_url='/dashboard/login/')
def find_tenders(request, paper_id):
	if request.method == 'POST':
		paper = Newspaper.objects.get(id=paper_id)
		snippets = paper.snippet_set.all()

		for s in snippets :
			s.is_tender = s.check_if_tender()
			s.is_auction = s.check_if_auction()
			s.save()

		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	return HttpResponse(status=403)



def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)

		if user : 
			contrib_login(request, user)
			return redirect('dashboard:dashboard')

		else : 
			return HttpResponse('failed to login')

	return render(request, 'login.html')
