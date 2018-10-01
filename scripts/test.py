from catalogue.models import TenderSnippet
import os

def run():
	files =os.listdir('./snippets')
	TenderSnippet.objects.all().delete()
	for fname in files : 
		path = './snippets/' + fname
		tender = TenderSnippet.objects.create(image_path=path)
		print ('object created #' + str(tender.id))
