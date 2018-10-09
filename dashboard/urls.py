from django.urls import path
from dashboard import views 

urlpatterns = [
	path('tenders/', views.tenders, name='dashboard-tenders'),
	path('import_pdfs_dir/', views.import_pdfs_dir, name='import-pdfs-dir'),
	path('extract_snippets/', views.extract_snippets, name='extract-snippets')
]

