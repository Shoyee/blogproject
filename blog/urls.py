from django.conf.urls import url
from . import views
from django.views.decorators.cache import cache_page

app_name = 'blog'
# 添加缓存页面装饰器，设置缓存时间为60秒
urlpatterns = [
    url(r'^$', cache_page(60)(views.IndexView.as_view()), name='index'),
    url(r'^post/(?P<pk>\d+)/$', cache_page(60)(views.PostDetailView.as_view()), name='detail'),
    url(r'^archives/(?P<year>\d{4})/(?P<month>\d{1,2})/$', cache_page(60)(views.ArchivesView.as_view()), name='archives'),
    url(r'^category/(?P<pk>\d+)/$', cache_page(60)(views.CategoryView.as_view()), name='category'),
    url(r'^tag/(?P<pk>\d+)/$', cache_page(60)(views.TagView.as_view()), name='tag'),
    url(r'^author/(?P<pk>\d+)/$', cache_page(60)(views.UserView.as_view()), name='author'),
    url(r'^search/$', cache_page(60)(views.search), name='search'),
]

