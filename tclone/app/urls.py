from django.urls import path
from django.conf.urls import url
from . import views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
app_name = 'app'
urlpatterns = [
		path('', views.feed, name='feed'),
		path('profile/<profileWho>/', views.profile, name='profile'),
		path('profile/', views.login, name='login2'),
		path('edit/<profileWho>/', views.edit, name = 'edit'),
		#path('edit/success/', views.success, name = 'success'),
		#url(r'^like/$', 'myapp.views.like', name='like'),
		path('like/', views.like, name='like'),
		path('share/', views.share, name='share'),
		path('follow/', views.follow, name='follow'),
		path('search/', views.search, name='search'),
		path('options/', views.settings, name='settings'),
]

if settings.DEBUG:
		urlpatterns += static(settings.MEDIA_URL,
							  document_root=settings.MEDIA_ROOT)
		urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)