def run():
	from catalogue.models import Snippet

	snippets = Snippet.objects.exclude(text='')

	for s in snippets : 
		s.id_tender = s.check_if_tender()
		s.is_auction = s.check_if_auction()
		s.save()