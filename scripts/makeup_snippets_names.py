import os 
def run():
	from catalogue.models import Snippet
	snippets = Snippet.objects.all()

	for i, x in enumerate(snippets):
		x.image.name = os.path.join('snippets', x.image.name.split('/')[-1])
		x.save()
		if (i % 1000 )== 0 : 
			print(x.image.name)
