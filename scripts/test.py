from catalogue.models import  Newspaper, NewspaperPage, Snippet
import os
from django.conf import settings
from dashboard.views import split_to_papers
from django.contrib.auth.models import User 
def run():
	
	user = User.objects.create(email='ahmadxxxx@gmail.com')

	print(user)
	print(user.username)
	print(user.email)