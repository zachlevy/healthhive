#urls.py in django root htest
from django.conf.urls import patterns, include, url
#from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'htest.views.index', name='index'),
    # url(r'^htest/', include('htest.foo.urls')),
    #url(r'^search/', include('healthhive.urls')),

    # when you have any url, include the app's urls.py
    url(r'^', include('healthhive.urls')),
    
    #url(r'^admin/', include(admin.site.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
