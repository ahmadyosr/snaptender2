def run():
	from catalogue.models import Snippet
	import os 
	tenders = Snippet.objects.filter(is_tender=True)

	sizes = 0 
	for t in tenders :
		im = t.image.path
		s = os.stat(im).st_size 
		sizes += s

	print(sizes/1024000)
	print(tenders.count())
