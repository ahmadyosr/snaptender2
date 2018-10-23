from catalogue.models import Newspaper, NewspaperPage, Snippet
from modules.extractors import BoxesExtractor
from django.conf import settings
import datetime

def run():
	paper = Newspaper.objects.all()[10]
	pages = NewspaperPage.objects.filter(newspaper=paper)
	

	for p in pages : 
		extractor = BoxesExtractor(p.image.path)
		extractor.extract()

		snippets = []
		rectangles = extractor.save_rectangles(settings.SNIPPETS_POOL_PATH)

		for r in rectangles:
			s = Snippet(newspaper=paper,
					 page = p,
					 extract_date=datetime.date.today(), 
					 image=r)
			snippets += [s]
		Snippet.objects.bulk_create(snippets)			
