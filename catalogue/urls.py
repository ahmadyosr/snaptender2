from django.urls import path
from catalogue import views 

app_name='catalogue'
urlpatterns = [
	path('labeling/', views.labeling, name='labeling')	
]

