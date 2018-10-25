"""
DJANGO TEST SCRIPT 
--------------------
execute this test under django environment
this should be executed as following
./manage.py shell < <path_for_this_file>
ie : 
python manage.py shell < modules/ocr/test_ocr.py


--------------------
"""

from modules.ocr.ocr import  OceanOCR
import cv2
from catalogue.models import Snippet
import sys

# def is_tender(text):
# 	from modules.ocr.ocr import config

# 	keywords = config['TENDERS_KEYWORDS']

# 	for keyword in keywords: 
# 		if text.find(keyword):
# 			return True

# 	return False

bw_rate_threshold = 84

snippets = Snippet.objects.filter(bw_rate__gte = bw_rate_threshold, text='')
c = 0

for s in snippets : 
	print(s.id)
	if not s.text :

		im = s.image.path
		im = cv2.imread(im)
		c+= 1
		print('Done so far : ' , c)

		s.text = OceanOCR.get_image_text(im)
		# if is_tender(s.text):
		# 	s.is_tender = True 
		if s.text : 
			s.save()

		# try : 
		# 	s.text = OceanOCR.get_image_text(im)

		# 	if is_tender(s.text):
		# 		s.is_tender = True 

		# 	s.save()

		# except Exception as e :
		# 	print('error')

		# 	x = str(e) 
		# 	with open('errors_log.txt', 'a') as f:
		# 		f.write(x)

		# 	print(x)

		cv2.destroyAllWindows()


