from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url('^dashboard/$', 'race.views.dashboard', name='dashboard'),
    url('^dashboard/overall_race/driver/$', 'race.views.overall_driver_prediction'),
    url('^dashboard/overall_race/constructor/$', 'race.views.overall_constructor_prediction'),
    url('^dashboard/race(?P<race_id>\d+)/driver/$', 'race.views.race_driver_prediction'),
    url('^dashboard/race(?P<race_id>\d+)/constructor/$', 'race.views.race_constructor_prediction'),
)
