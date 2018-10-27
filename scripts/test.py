from catalogue.models import  Newspaper, NewspaperPage, Snippet
import os
from django.conf import settings
from dashboard.views import split_to_papers
def run():
	# file_name = 'f1'

	# n = NewspaperPage.objects.create(image='f1')
	# n.image.name = 'pages/'+file_name
	# n.save()

	paper = Newspaper.objects.last()
	# r = split_to_papers(paper)

	# for p in r: 
	# 	print(p.image.name)
	# 	print(p.image.url)
	# 	print(p.image.path)
	# # 	break
	# paper.is_splitted= False
	# paper.save() 

	print(paper.file.name)
	print(paper.file.path)
	print(paper.file.url)
	print('--')
	papers = paper.newspaperpage_set.all()
	print(papers[0].image.name)
	print(papers[0].image.path)
	print(papers[0].image.url)
	print('--')

	
