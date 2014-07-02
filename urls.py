from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'shalent.views.home', name='home'),
    url(r'^index$', 'shalent.views.index', name='index'),
    url(r'^auth/', include('Auth.urls'))
)
