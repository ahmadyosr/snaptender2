from catalogue.models import  Newspaper, NewspaperPage, Snippet
import os
from django.conf import settings
from dashboard.views import split_to_papers
from dashboard.views import extract_paper_

def run():
	paper = Newspaper.objects.last()
	# print(paper.file.name)
	# snpts = extract_paper_(paper)
	snpts = paper.snippet_set.all()
	for s in snpts : 
		print(snpts[0].bw_rate)
	# print(snpts[0].image.url)
	# print(snpts[0].image.name)