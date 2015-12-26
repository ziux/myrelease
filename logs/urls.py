from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^sys$', views.sys, name='sys'),
    url(r'^release/$', views.release, name='release'),
    url(r'^relist/(?P<id>[0-9]+)/$', views.relist, name='relist'),
    url(r'^relog/(?P<proid>[0-9]+)/(?P<id>[0-9]+)/$', views.relog, name='relog'),
]
