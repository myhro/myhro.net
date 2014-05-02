from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^$', 'myhronet.views.home', name='home'),
    url(r'^(?P<hashcode>[-\w]+)$', 'myhronet.views.retrieve', name='retrieve'),
)
