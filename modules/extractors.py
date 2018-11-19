import cv2
import datetime
import numpy as np
import requests
import json

from modules.ocr.config import config
from io import BytesIO
import os 

class BoxesExtractor():
	def __init__(self, image_path ):
		self.image_path = image_path
		self.image = None 
		self.thresh = None 
		self.buildings = []
		self.cropped_rectangles = []
		
		return 

	def prep_image(self):
		self.image =  cv2.imread(self.image_path)
		gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
		retr, self.thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)
		kernel = np.ones((5,5), np.uint8)
		self.thresh = cv2.dilate(self.thresh, kernel, iterations=1)

		return 

	def detect_rectangles(self):
		if not self.thresh.any() : 
			raise(Exception('Image is not prepared yet!'))

		_, contours, hierarchy = cv2.findContours(self.thresh, cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)

		for c in contours : 
			(x, y, w, h) = cv2.boundingRect(c)
			if w<100 and h<100:
				continue

			accuracy = 0.03 * cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, accuracy, True)
			
			if len(approx) == 4 : 
				self.detected_rectangles += [approx]
		
		return 

	def crop_recrangles(self):
		if not self.detected_rectangles : 
			raise(Exception('There are not detected rectangles yet!'))

		for approx in self.detected_rectangles:
			x_values =[v[0][0] for v in approx] 
			y_values =[v[0][1] for v in approx]
			start_row, end_row = min(y_values), max(y_values)
			start_col, end_col = min(x_values), max(x_values)

			cropped =  self.image[start_row:end_row, start_col:end_col]
			h, w = cropped.shape[:2]

			if h>120 and w>120:
				self.cropped_rectangles += [cropped]

		return 

	def bw_rate(self, im):
		'''
		check if black and white, so its an advertisment
		not a photo'''
		im = cv2.resize(im, None, fx = 0.20, fy = 0.20)
		pixels_count = im.shape[0]*im.shape[1]
		pixels = im.reshape(pixels_count,-1)

		bw_count = 0 
		for p in pixels :
			if p[0] == p[1] == p[2] and (p[0]>235 or p[0]<30) : 
				bw_count += 1

		bw_rate = bw_count/pixels_count
		
		return bw_rate

	def save_rectangles(self, output_path):
		if not self.cropped_rectangles: 
			return [] 

		images = []
		for i,cropped in enumerate(self.cropped_rectangles):
			bw_rate = self.bw_rate(cropped)

			if bw_rate < 0.45:
				continue

			file_name = str(datetime.datetime.now().time())+'_'+str(i)+'.jpg'
			file_path = os.path.join(output_path,file_name) 
			
			r = cv2.imwrite(file_path,cropped)
			
			if r : 
				images += [(file_name, bw_rate)]
	
		return images

	def save_rectangles_contours(self):
		if not self.cropped_rectangles: 
			raise(Exception('Cropped Rectangles are not ready yet!'))
			
		cv2.drawContours(self.image, self.detected_rectangles, -1, (0, 255, 0), 2)	
		image_title = 'page_contours_'+str(datetime.datetime.now().time())+'.jpg'
		cv2.imwrite(''+image_title, self.image)

		return 

	def extract(self):
		self.prep_image()
		self.detect_rectangles()
		self.crop_recrangles()
		return self.cropped_rectangles



class TendersBoxesExtractor(BoxesExtractor):

	ocr_lang = 'ara'

	def __init__(self, image_path):
		super().__init__(image_path)
		self.cropped_tenders = None 
	

	def is_tender(self, tender):
		print('enter is_tender()')

		tender_text = OceanOCR.get_image_text(tender)
		keywords = config['TENDERS_KEYWORDS']

		for keyword in keywords: 
			if tender_text.find(keyword):
				return True

		return False 

	def filter_tenders(self):

		tenders = []
		print ('enter filter tenders')

		for tender in self.cropped_rectangles: 
			tender_size = float(tender.size* tender.itemsize)/10000000.0
			if tender_size >= 1:
				continue

			print('length of tenders', len(tenders))
			if self.is_tender(tender):
				tenders += [tender]

		self.cropped_tenders = tenders 
		return 

	def extract(self):
		if not self.api_key : 
			raise(Exception('You shold set the ocr api key first'))

		self.prep_image()
		self.detect_rectangles()
		self.crop_recrangles()
		self.filter_tenders()
		return self.cropped_tenders
