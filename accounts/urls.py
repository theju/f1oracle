from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^register/$', 'accounts.views.register', name='accounts_register'),
    url(r'^login/$', 'accounts.views.login', name='accounts_login'),
)
