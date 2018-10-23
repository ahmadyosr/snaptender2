from django.urls import path
from dashboard import views 

urlpatterns = [
	path('tenders/', views.tenders, name='dashboard-tenders'),
	path('toggle_acceptance/<int:tender_id>/', views.toggle_acceptance, name='dashboard-toggle-acceptance'),

	path('newspapers/', views.newspapers, name='dashboard-newspapers'),
	path('newspaper/<int:paper_id>/', views.newspaper, name='dashboard-newspaper'),
	path('import_pdfs_dir/', views.import_pdfs_dir, name='import-pdfs-dir'),
	path('extract_snippets/', views.extract_snippets, name='extract-snippets'),
	path('split_pdf/', views.split_pdf, name='split-pdf')
]

