from django.conf.urls import url
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<pk>\d+)/$', views.detail, name='detail'),
    url(r'^archives/(?P<year>\d{4})/(?P<month>\d{1,2})/$', views.archives, name='archives'),
    url(r'^category/(?P<pk>\d+)/$', views.category, name='category'),
]

