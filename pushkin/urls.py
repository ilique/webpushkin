from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^ping/(?P<ip>[0-9\.]+)/$', views.ping),

    url(r'^disable/interface/?$', views.disable_interface),
    url(r'^enable/interface/?$', views.enable_interface),
    url(r'^ports/status/?$', views.ports_status),

    url(r'^$', views.index),
]



