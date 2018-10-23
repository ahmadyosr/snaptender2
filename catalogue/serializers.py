from catalogue.models import Snippet
from rest_framework import serializers
from django.conf import settings 

class TenderSnippetSerializer(serializers.ModelSerializer):
	
	image_url = serializers.SerializerMethodField()

	class Meta:
		model = Snippet
		fields = ('start_date',
		'finish_date',
		'tender_newspaper_id',
		'publisher',
		'admin',
		'is_accepted',
		'is_accepted',
		'is_duplicated',
		'is_active', 
		'image_path', 
		'tender_text', 
		'category', 
		'coordinates',

		'image_url'
		)

	def get_image_url(self, object):
		return settings.HOST_NAME + object.image_path.url