from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url('^$', 'race.views.index', name='index'),
    url('^dashboard/$', 'race.views.dashboard', name='dashboard'),
    url('^dashboard/overall_race/driver/$', 'race.views.overall_driver_prediction'),
    url('^dashboard/overall_race/constructor/$', 'race.views.overall_constructor_prediction'),
    url('^dashboard/race(?P<race_id>\d+)/driver/$', 'race.views.race_driver_prediction'),
    url('^dashboard/race(?P<race_id>\d+)/constructor/$', 'race.views.race_constructor_prediction'),
    url('^dashboard/scores/$', 'race.views.scores'),
    url('^dashboard/my_scores/$', 'race.views.my_scores'),
    url('^dashboard/results/$', 'race.views.results'),
)
