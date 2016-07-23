from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.project_list, name='project_list'),
    url(r'^edit_project/(?P<id>[0-9]+)/$',
        views.edit_project, name='edit_project'),
    url(r'^add_project/$', views.add_project, name='add_project'),

]
