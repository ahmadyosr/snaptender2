"""
execute this test under django environment
this should be executed as following
./manage.py shell < <path_for_this_file>
"""

from ocr import  OceanOCR
import cv2
from catalogue.models import 

im = cv2.imread('./test_im.jpg')
print(im.shape)
x = OceanOCR.get_tender_text(im)
print(x)