def run():
	from catalogue.models import Snippet
	from modules.ocr.config import config

	keys = config['TENDERS_KEYWORDS']
	snippets = Snippet.objects.exclude(text='')

	c = 0 
	for s in snippets : 
		for k in keys : 
			if s.text.find(k) != -1 : 
				c+= 1 
				print(c)
				s.is_tender = True
				s.save()
				break  