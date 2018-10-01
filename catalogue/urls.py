from django.urls import path
from catalogue import views 

urlpatterns = [
	path('index/', views.index, name='index')	
]

