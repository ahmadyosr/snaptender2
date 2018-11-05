from django.urls import path
from apis import views  
from rest_framework.urlpatterns import format_suffix_patterns



urlpatterns = [
	path('snippets/', views.SnippetList.as_view(), name='snippets'),
	path('categories/', views.CategoryList.as_view(), name='categories'),
	path('auth/login/', views.Login.as_view(), name='login'),
	path('auth/logout/', views.Logout.as_view(), name='logout'),
	path('auth/register/', views.Register.as_view(), name='register')
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
# urlpatterns = format_suffix_patterns(urlpatterns)
