from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import  static

urlpatterns=[
    url(r'^$', views.index, name='home'),
    url(r'^image/$', views.add_image, name='upload_image'),
    url(r'^profile/$', views.profile_info, name='profile'),
    url(r'^update/$', views.profile_update, name='update'),
    url(r'^comment/(?P<image_id>\d+)', views.comment, name='comment'),
    url(r'^search/', views.search_results, name = 'search_results'),
    url(r'^follow/(?P<user_id>\d+)', views.follow, name = 'follow'),
    url(r'^unfollow/(?P<user_id>\d+)', views.unfollow, name='unfollow'),
    url(r'^likes/(\d+)/$', views.like_images,name='likes')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)