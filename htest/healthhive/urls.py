#urls.py in healthhive
from django.conf.urls import patterns, url

from healthhive import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'healthhive.views.index', name='index'),
    url(r'^search/$', 'healthhive.views.search', name='search'),
    url(r'^submit/$', 'healthhive.views.submit', name='submit'),
    #url(r'^result/$', 'healthhive.views.result', name='result'),
    url(r'^result/(?P<druga>[a-zA-Z]+)/(?P<drugb>[a-zA-Z]+)/$', 'healthhive.views.result', name='result'),
    #url(r'^result/(?P<druga>.+)/(?P<drugb>.+)/$', 'healthhive.views.result', name='result'),
    #url(r'^result/$', 'healthhive.views.result', name='result'),
    # url(r'^htest/', include('htest.foo.urls')),
)
