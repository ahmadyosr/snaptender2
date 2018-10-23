from catalogue.models import  NewspaperPage, Snippet
import os

def run():
	
	x = Snippet.objects.all()
	# print('count of files',x.count())
	# c = 0 

	# for f in x:
	# 	if not os.path.isfile(f.image.path):
	# 		# print('not a file')
	# 		# print (f.id)
	# 		# print(f.delete())
	# 		pass
	# 	else: 
	# 		c+= 1
	# 		# print (c)	
	# print(c)

	count = x.filter(bw_rate__gte=84).count()
	count2 = x.filter(bw_rate__lte=84).count()
	print('bw_rate > 84', count)
	print('other', count2)
