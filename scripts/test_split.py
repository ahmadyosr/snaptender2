from catalogue.models import Newspaper as l 

def run():
	n = l.objects.last()
	# n.is_splitted=False
	# n.is_extracted=False
	# n.save()
	
	pages = n.newspaperpage_set.all()
	# print(pages.delete())
	print(pages[0].image.name)
	print('path ' , pages[0].image.path)
	print(pages[0].image.url)
