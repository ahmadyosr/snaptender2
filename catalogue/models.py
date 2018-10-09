from django.db import models
from django.contrib.auth.models import User

NEWSPAPER_CHOICES = (
    ('ADDUSTOUR', 'addustour'),
    ('ALRAI', 'alrai'),
)

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
	title = models.CharField(blank=True, max_length=200)
	publish_date = models.DateField(null=True, blank=True, auto_now_add=False)
	file = models.FileField('pdfs/', unique=True)

	def __str__(self):
		return self.file.name


class NewspaperPage(models.Model):
	newspaper = models.ForeignKey(Newspaper, null=True, on_delete=models.SET_NULL)
	page_no = models.IntegerField(default=0)
	image = models.FileField('pages/')

class TenderSnippet(models.Model):
	newspaper = models.ForeignKey(Newspaper, null=True, on_delete=models.SET_NULL)

	title = models.CharField(max_length=50,choices=NEWSPAPER_CHOICES)
	extract_date = models.DateField(auto_now_add=True)
	start_date = models.DateField(blank=True, null=True)
	finish_date = models.DateField(blank=True, null=True)


	publisher = models.ForeignKey(Publisher, blank=True, null=True, on_delete=models.SET_NULL)
	admin = models.ForeignKey(User,blank=True, null=True, on_delete=models.SET_NULL)


	is_tender = models.BooleanField(default=False)
	is_republished = models.BooleanField(default=False)
	is_active = models.BooleanField(default=False)

	image = models.FileField(upload_to='tenders_images/')
	text = models.CharField(blank=True, max_length=200)
	category = models.ForeignKey(Category,blank=True, null=True, on_delete=models.SET_NULL)
	
	coordinates = models.CharField(blank=True, max_length=100)
	
	def __str__(self):
		return self.title
