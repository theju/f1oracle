from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url('^dashboard/$', 'race.views.dashboard', name='dashboard'),
)
