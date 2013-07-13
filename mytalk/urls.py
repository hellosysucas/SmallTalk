# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from mytalk import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myHotel.views.home', name='home'),
    # url(r'^myHotel/', include('myHotel.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$',views.index),
)

