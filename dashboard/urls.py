from django.urls import path
from dashboard import views 

app_name = 'dashboard'
urlpatterns = [
	path('', views.dashboard, name='dashboard'),
	path('upload/', views.upload, name='upload'),
	path('delete_newspaper/<int:paper_id>/', views.delete_newspaper, name='delete_newspaper'),

	path('snippets/', views.snippets, name='snippets'),
	path('toggle_acceptance/<int:tender_id>/', views.toggle_acceptance, name='toggle-acceptance'),

	path('newspapers/', views.newspapers, name='newspapers'),
	path('newspaper/<int:paper_id>/', views.newspaper, name='newspaper'),

	path('extract_paper/<int:paper_id>/', views.extract_paper, name='extract_paper'),
	path('split_paper/<int:paper_id>/', views.split_paper, name='split_paper')
]

