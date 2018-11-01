from django.test import TestCase
from catalogue.models import Newspaper, Snippet
from django.conf import settings
import os 
import pathlib 
import cv2

class NewspaperTestCase(TestCase):
	"""This test case depends on 
	a file that is stored in media/tests_/newspaper.pdf folder"""

	paper = None 
	file_name = 'tests_/newspaper.pdf'

	pdf_path = os.path.join(settings.BASE_DIR,  file_name)

	def setUp(self):
		self.paper = Newspaper.objects.create(
			title='Addustour',
			file = self.file_name
			)

	def test_newpaper_file_path(self):
		paper = self.paper
		p1 = pathlib.Path(paper.file.path)
		self.assertTrue(p1, self.pdf_path)




class TenderTestCase(TestCase):
	
	tender = False
	file_name = 'tests_/tender.jpg'
	expected_path = os.path.join(settings.BASE_DIR, file_name)

	def setUp(self):
		self.tender = Snippet.objects.create(image=self.file_name)

	def test_newpaper_file_path(self):
		tender = self.tender
		p1 = pathlib.Path(tender.image.path)
		self.assertTrue(p1, self.expected_path)
