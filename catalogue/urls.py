from django.urls import path
from catalogue import views 

app_name='catalogue'
urlpatterns = [
	path('index/', views.index, name='index')	
]

