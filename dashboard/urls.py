from django.urls import path
from dashboard import views 

app_name = 'dashboard'
urlpatterns = [
	path('', views.dashboard, name='dashboard'),
	path('upload/', views.upload, name='upload'),
	path('login/', views.login, name='login'),
	path('delete_newspaper/<int:paper_id>/', views.delete_newspaper, name='delete_newspaper'),

	path('snippets/', views.snippets, name='snippets'),
	path('toggle_acceptance/<int:tender_id>/', views.toggle_acceptance, name='toggle-acceptance'),
	path('approve_category/<int:tender_id>/', views.approve_category, name='approve_category'),

	path('newspapers/', views.newspapers, name='newspapers'),
	path('newspaper/<int:paper_id>/', views.newspaper, name='newspaper'),

	path('extract_paper/<int:paper_id>/', views.extract_paper, name='extract_paper'),
	path('split_paper/<int:paper_id>/', views.split_paper, name='split_paper'),
	path('ocr_paper/<int:paper_id>/', views.ocr_paper, name='ocr_paper'), 
	path('find_tenders/<int:paper_id>/', views.find_tenders, name='find_tenders')
]

