from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^register/$', 'accounts.views.register', name='accounts_register'),
    url(r'^login/$', 'accounts.views.login', name='accounts_login'),
    url(r'^logout/$', 'accounts.views.logout', name='accounts_logout'),
    url(r'^password/reset/$', 'accounts.views.password_reset', name='accounts_pasword_reset'),
    url(r'^password/reset/confirm/(?P<token>[0-9A-Za-z\-]+)/$',
        'accounts.views.password_reset_confirm',
        name='accounts_pasword_reset_confirm'),
)
