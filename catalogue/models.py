from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
	title = models.CharField(max_length=50)

	def __str__(self):
		return self.title

class Publisher(models.Model):
	title = models.CharField(max_length=50)

	def __str__(self):
		return self.title

class TenderSnippet(models.Model):
	title = models.CharField(default='None', max_length=200)
	extract_date = models.DateField(auto_now_add=True)
	start_date = models.DateField(blank=True, null=True)
	finish_date = models.DateField(blank=True, null=True)

	tender_newspaper_id = models.CharField(blank=True, max_length=50)
	publisher = models.ForeignKey(Publisher, blank=True, null=True, on_delete=models.CASCADE)
	admin = models.ForeignKey(User,blank=True, null=True, on_delete=models.SET_NULL)

	is_accepted = models.BooleanField(default=False)
	is_duplicated = models.BooleanField(default=False)
	is_active = models.BooleanField(default=False)

	image_path = models.FileField(upload_to='tenders_images/')
	tender_text = models.CharField(blank=True, max_length=200)
	category = models.ForeignKey(Category,blank=True, null=True, on_delete=models.SET_NULL)
	
	coordinates = models.CharField(blank=True, max_length=100)
	
	def __str__(self):
		return self.title