from catalogue.models import  Newspaper, NewspaperPage, Snippet
import os
from django.conf import settings
from dashboard.views import split_to_papers
from dashboard.views import extract_paper_

def run():
	paper = Newspaper.objects.last()
	# print(paper.file.name)
	snpts = extract_paper_(paper)



	print(snpts[0].image.path)
	print(snpts[0].image.url)
	print(snpts[0].image.name)