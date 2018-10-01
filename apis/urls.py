from django.urls import path
from apis import views 
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
	path('tenders_list/', views.tenders_list, name='tenders_list'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
