from catalogue.models import Snippet, Category
from rest_framework import serializers
from django.conf import settings 

class SnippetSerializer(serializers.ModelSerializer):
	class Meta : 
		model = Snippet
		fields = ('id', 'start_date', 'finish_date')
class SomeSerializer(serializers.Serializer):
	start_data = serializers.CharField()

	
class TenderSnippetSerializer(serializers.ModelSerializer):
	
	# image_url = serializers.SerializerMethodField()

	class Meta:
		model = Snippet
		fields = ('id',
		'start_date',
		'finish_date',
		'title',
		'newspaper',
		'publisher',
		'admin',
		'is_active', 
		# 'image', 
		'category', 

		# 'image_url'
		)

	
	# def get_image_url(self, object):
	# 	try :
	# 		if object.image :  
	# 			return settings.HOST_NAME + object.image.url
		
	# 	except AttributeError:
	# 		return '' 

	# 	return ''

class CategorySerializer(serializers.ModelSerializer):
	title = serializers.CharField(required=False)
	class Meta : 
		model = Category
		fields = ('id', 'title')

		