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
    #url(r'^site_media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_PATH}),
    url(r'^$',views.index,name='index'),
    url(r'^signIn/$',views.signIn),
    url(r'^getStoreMessage/$',views.getStoreMessage),
    url(r'^detectLogin/$',views.detectLogin),
    url(r'^exitOperation/$',views.exitOperation),
    
    url(r'^register/$',views.register),
	url(r'^register/doRegister/$',views.doRegister),
	
    url(r'^friends/$',views.friends),
    url(r'^friends/message/$',views.message),
    url(r'^friends/deleteFriend/$',views.deleteFriend),
	
    url(r'^exchangeUserMessage/$',views.exchangeUserMessage),
)

