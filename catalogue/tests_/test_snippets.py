from django.test import TestCase
from catalogue.models import Snippet
from modules.ocr.ocr import config

class SnippetTestCase(TestCase):
	s1 = None
	
	def setUp(self):
		self.s1 = Snippet.objects.create()
		
	def test_check_if_tender(self):	
		tenders_keywords = config['TENDERS_KEYWORDS']

		not_tender = Snippet(text='ahmad yosr almashni')
		tenders = [Snippet(text='fdsf %s fdsfsd ' %k) for k in tenders_keywords ]

		for s in tenders : 
			self.assertTrue(s.check_if_tender())
		self.assertFalse(not_tender.check_if_tender())

	def test_check_if_auction(self):
		self.assertTrue(True)
		
	def test_(self):
		self.assertTrue(True)
