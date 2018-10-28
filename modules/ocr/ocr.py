from io import BytesIO
from modules.ocr.config import config
import cv2
import os 
import requests 

import datetime
import numpy as np
import json

class OceanOCR():

	api_key = config['OCR_API_KEY']
	tenders_keywords = config['TENDERS_KEYWORDS']
	ocr_lang = config['OCR_LANG']

	@staticmethod
	def make_ocr_api_call(tender):
		print('enter api call ')
		ret, tender_buff = cv2.imencode('.jpg',tender)
		tender_buff = tender_buff.tostring()

		tender_buffer = BytesIO(tender_buff)

		payload = {'isOverlayRequired': True,
					'apikey': OceanOCR.api_key,
					'language': OceanOCR.ocr_lang,
					}

		r = requests.post('https://api.ocr.space/parse/image',
					files={'f1.jpg': tender_buffer},
					data=payload,
		)

		tender_buffer.close()
		return r 

	@staticmethod
	def get_image_text(tender):
		r = OceanOCR.make_ocr_api_call(tender)

		decoder = json.JSONDecoder()
		result_text = decoder.decode(r.text)
		parsed_text = None 

		try : 
			parsed_text = result_text['ParsedResults'][0]['ParsedText']

			with open('o.out' ,'a') as f :
				f.write(parsed_text) 
				print(parsed_text)

		except : 
			pass 
			
		return parsed_text

