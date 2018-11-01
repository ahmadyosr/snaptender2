def run():
	from catalogue.models import Snippet
	from django.db.models import Q
	from django.conf import settings 
	import os 
	import sys
	tenders = Snippet.objects.filter(Q(is_tender=True) | Q(is_auction=True))
	# for t in tenders : 
	t = tenders.last()
	c =0 
	for i, t in enumerate(tenders) : 
		print(i)
		path  = t.image.path

		if os.path.isfile(path):
			print('1 ')
			c+= 1 

		else :
			print('0')
		continue 

		new_fname = os.path.join('tenders', t.image.name.split('/')[-1])
		print('old > ',  t.image.path)
		t.image = new_fname
		t.save()
		print('new > ',  t.image.path)
		
		new_path = os.path.join(settings.MEDIA_ROOT, new_fname)

		try : 
			os.rename(path, new_path)
			print('success')
		except Exception as e : 
			# print(str(e))
			pass

	print(c)
	print(tenders.count())