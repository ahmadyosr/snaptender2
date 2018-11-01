def run():
	from catalogue.models import Snippet
	from django.db.models import Q 
	import os
	import random

	tenders = Snippet.objects.filter(Q(is_tender=True) | Q(is_auction=True))

	for t in tenders :
		t = random.choice(tenders) 
		path = t.image.path
		t.image = t.image.name.replace(':', '_')
		new_path = t.image.path
		# print(path)
		# print(new_path)


		t.save() 
		try : 
			os.rename(path, new_path)
			print('1')
		except Exception as e : 
			print('one faild > ')