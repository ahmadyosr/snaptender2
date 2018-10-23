from catalogue.models import Newspaper, NewspaperPage, Snippet
from modules.extractors import BoxesExtractor
from django.conf import settings
import datetime
import sys 
import threading 
import cv2 

def extract_paper(paper):
	if paper.is_extracted:
		print('return')
		return 

	pages = NewspaperPage.objects.filter(newspaper=paper, is_extracted=False)
	

	for p in pages : 

		# print(p.image.path)
		# im = 		cv2.imread(p.image.path)
		# im = cv2.resize(im, None, fx=0.2, fy=0.2)
		# cv2.imshow('fdsf', im )
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()
		extractor = BoxesExtractor(p.image.path)

		extractor.extract()

		snippets = []

		rectangles = extractor.save_rectangles(settings.SNIPPETS_POOL_PATH)
		if len(rectangles) > 0  : 
			print('FOUND ONE ')

		for r, bw_rate in rectangles:
			# print('inside - rectangles')

			s = Snippet(newspaper=paper,
					 page = p,
					 extract_date=datetime.date.today(), 
					 image=r, 
					 bw_rate=bw_rate*100)
			snippets += [s]

		if rectangles : 
			p.is_extracted = True
			p.has_rectangles = True
			p.save() 

		Snippet.objects.bulk_create(snippets)			

	paper.is_extracted = True
	paper.save()
	print('done paper id %d ', paper.id)

def run():
	papers = Newspaper.objects.filter(is_extracted=False)
	print(len(papers))

	for p in papers: 
		try : 
			print('--')
			extract_paper(p)
		except Exception as e: 
			print(str(e))