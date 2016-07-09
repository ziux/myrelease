from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.login_index, name='login_index'),
    url(r'^logout/$', views.logout_account, name='logout_account'),
    url(r'^login/$', views.login_account, name='login_account'),
    url(r'^user_list/$', views.user_list, name='user_list'),
    url(r'^user_add/$', views.user_add, name='user_add'),
    url(r'^user_edit/(?P<id>[0-9]+)/$', views.user_edit, name='user_edit'),
    url(r'^user_edit_password/(?P<id>[0-9]+)/$', views.user_edit_password, name='user_edit_password'),
    url(r'^user_del/(?P<id>[0-9]+)/$', views.user_del, name='user_del'),
    url(r'^user_edit_permission/(?P<id>[0-9]+)/$', views.user_edit_permission, name='user_edit_permission'),
]
