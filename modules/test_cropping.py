import cv2
from extractors import BoxesExtractor, TendersBoxesExtractor
extracter = BoxesExtractor('images/pages/0004.jpg')
extracter.extract()
tenders = extracter.cropped_rectangles

for i,t in enumerate(tenders):
	# print(float(t.size*t.itemsize)/10000000.0)
	x = float(t.size*t.itemsize)/10000000.0
	if int(x)> 0:
		cv2.imshow(str(i), t)
		cv2.waitKey()



# extractor = TendersBoxesExtractor('images/pages/0004.jpg')
# extractor.extract()
# tenders = extractor.cropped_rectangles
# print(extractor.cropped_tenders)

# # for i,r in enumerate(tenders): 
# # 	cv2.imshow(str(i), r)
# # 	cv2.waitKey(0)

# cv2.destroyAllWindows()