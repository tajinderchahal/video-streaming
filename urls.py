from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'shalent.views.home', name='home'),
    url(r'^terms$', 'shalent.views.terms', name='terms'),
    url(r'^index$', 'shalent.views.index', name='index'),
    url(r'^new_user$', 'shalent.views.new_user', name='new_user'),
    url(r'^get_category/all_category$', 'shalent.views.get_category'),
    url(r'^auth/', include('Auth.urls')),
)
