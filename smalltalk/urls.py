from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('SmallTalk.smalltalk.views',
    url(r'^$', 'index'),  
)
