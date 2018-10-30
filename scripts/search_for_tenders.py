def run():
	from catalogue.models import Snippet
	from dashboard.views import find_keyword

	snippets = Snippet.objects.exclude(text='')

	for i, s in enumerate(snippets) :
		s.is_tender = find_keyword(s, 'TENDERS_KEYWORDS')
		s.is_auction = find_keyword(s,'AUTCTION_KEYWORDS')
		s.save()
		if i % 200 == 0: 
			print('done so far ' , i)
