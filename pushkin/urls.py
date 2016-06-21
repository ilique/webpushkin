from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^demo/ajax', views.ajax),
    url(r'^demo/commands/?$', views.test_commands),
    url(r'^demo/services/?$', views.test_services),
    url(r'^demo/pushkin/?$', views.test_pushkin),
    url(r'^$', views.index),
]



