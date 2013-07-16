from django.conf.urls import patterns, include, url
from mytalk import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SmallTalk.views.home', name='home'),
    # url(r'^SmallTalk/', include('SmallTalk.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
	#url(r'^mytalk/',include('mytalk.urls')),
    url(r'^',include('mytalk.urls')),
)