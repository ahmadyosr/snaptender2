from django.db import models
from django.contrib.auth.models import User
from modules.ocr.ocr import config
import os
NEWSPAPER_CHOICES = (
    ('ADDUSTOUR', 'addustour'),
    ('ALRAI', 'alrai'),
)

def find_keyword(snippet, keywords_label):
	keywords = config[keywords_label]

	for keyword in keywords: 
		if snippet.text.find(keyword) > -1:
			return True

	return False

class Category(models.Model):
	title = models.CharField(max_length=50)

	def __str__(self):
		return self.title

class Publisher(models.Model):
	title = models.CharField(max_length=50)
	
	def __str__(self):
		return self.title

class Newspaper(models.Model):
	is_extracted = models.BooleanField(default=False)
	is_splitted = models.BooleanField(default=False)
	is_ocr = models.BooleanField(default=False)
	is_find_tenders = models.BooleanField(default=False)
	

	title = models.CharField(blank=True, max_length=50,choices=NEWSPAPER_CHOICES)
	publish_date = models.DateField(null=True, blank=True, auto_now_add=False)
	file = models.FileField(blank=False, null=False, upload_to='newspapers_pdfs/', unique=True)

	def delete_file(self):
		if self.file : 
			path =  self.file.path
		else : 
			return 

		if os.path.exists(path):
			os.remove(path)

	
	def __str__(self):
		return self.file.name


class NewspaperPage(models.Model):
	newspaper = models.ForeignKey(Newspaper, null=True, on_delete=models.CASCADE)
	page_no = models.IntegerField(default=0)
	image = models.FileField(upload_to='newspapers_pages/')
	has_tenders = models.BooleanField(default=False)
	has_snippets = models.BooleanField(default=False)
	is_extracted = models.BooleanField(default=False)

class Snippet(models.Model):
	newspaper = models.ForeignKey(Newspaper, blank=True, null=True, on_delete=models.SET_NULL)
	page = models.ForeignKey(NewspaperPage,blank=True, null=True, on_delete=models.SET_NULL)

	title = models.CharField(blank=True, max_length=50)
	extract_date = models.DateField(auto_now_add=True)
	start_date = models.DateField(blank=True, null=True)
	finish_date = models.DateField(blank=True, null=True)


	publisher = models.ForeignKey(Publisher, blank=True, null=True, on_delete=models.SET_NULL)
	admin = models.ForeignKey(User,blank=True, null=True, on_delete=models.SET_NULL)

	is_ocred = models.BooleanField(default=False)
	is_tender = models.BooleanField(default=False)
	is_auction = models.BooleanField(default=False)
	is_republished = models.BooleanField(default=False)
	is_active = models.BooleanField(default=False)

	image = models.FileField(blank=True, null=True, upload_to='tenders_images/')
	text = models.CharField(blank=True, max_length=200)
	suggested_category = models.ForeignKey(Category,blank=True, null=True, on_delete=models.SET_NULL, related_name='suggested_category')
	# category = models.ForeignKey(Category,blank=True, null=True, on_delete=models.SET_NULL)
	category = models.CharField( blank=True, max_length=200)

	bw_rate = models.IntegerField(default=0)
	

	def delete_file(self):
		if self.image : 
			path =  self.image.path
		else : 
			return 

		if os.path.exists(path):
			os.remove(path)


	def check_if_tender(self):
		return find_keyword(self, 'TENDERS_KEYWORDS')

	def check_if_auction(self):
		return find_keyword(self, 'AUCTION_KEYWORDS')

	def classify(self):
		self.category = self.category
		self.save()
		
	def __str__(self):
		if self.text == '':
			return '' 
			# return self.image.url
		else : 
			return self.text[:int(len(self.text)/10)]