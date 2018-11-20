from django.urls import path
from apis import views  
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'apis'

urlpatterns = [
	path('snippets/', views.SnippetList.as_view(), name='snippets'),
	path('snippet/<int:pk>/', views.SnippetDetail.as_view(), name='snippet-detail'),

	path('favorite/<int:pk>/', views.FavoriteApi.as_view(), name='snippet-favorite'),
	path('favorites/', views.FavoriteList.as_view(), name='favorites'),

	path('add_preferences/', views.AddPreferencesList.as_view(), name='add-preferences'),
	path('auth/login/', views.LoginApi.as_view(), name='login'),
	path('auth/register/', views.RegisterApi.as_view(), name='register')
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
