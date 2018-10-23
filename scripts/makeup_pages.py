def run():
	import os
	from catalogue.models import NewspaperPage
	pages = NewspaperPage.objects.all()
	
	for n in pages : 
		# print(n.newspaper.file.name)

		# try : 	
		# 	parent = n.newspaper.file.name.split('/')[1] 
		# except IndexError:
		# 	parent = n.newspaper.file.name

		# n.image.name = n.image.name.split(parent)[1] 

		# n.image.name = os.path.join('pages', n.image.name) 
		# n.save()
		print(n.image.name)
		print(n.image.path)