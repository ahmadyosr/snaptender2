
def run():
	# populate from folder and check if it exists in database  
	from django.conf import settings 
	import os
	from catalogue.models import Newspaper
