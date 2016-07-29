from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^demo/ajax', views.ajax),
    url(r'^demo/commands/?$', views.test_commands),
    url(r'^demo/services/?$', views.test_services),
    url(r'^demo/pushkin/?$', views.test_pushkin),
    url(r'^grep/voip/tau-8/?$', views.grep_voip_config),
    url(r'^$', views.index),
]



