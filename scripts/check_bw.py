def run():
	from catalogue.models import Snippet
	import cv2

	ts = Snippet.objects.filter(bw_rate=95)
	print(ts.count())
	
	for t in ts : 
		print('-')
		x = cv2.imread(t.image.path)
		cv2.imshow('fdsfsd', x)
		cv2.waitKey(0)
		cv2.destroyAllWindows()