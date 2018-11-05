from catalogue.models import Snippet, Category
from rest_framework import serializers
from django.conf import settings 

class TenderSnippetSerializer(serializers.ModelSerializer):
	
	image_url = serializers.SerializerMethodField()

	class Meta:
		model = Snippet
		fields = ('start_date',
		'finish_date',
		'title',
		'newspaper',
		'publisher',
		'admin',
		'is_active', 
		'image', 
		'category', 

		'image_url'
		)

	def get_image_url(self, object):
		if object.image : 
			return settings.HOST_NAME + object.image.url
		return '' 

class CategoryList(serializers.ModelSerializer):
	class Meta : 
		model = Category
		fields = ('title')


# class LoginList(serializers.ModelSerializer):
# 	class Meta : 
# 		model = Category
# 		fields = ('title')