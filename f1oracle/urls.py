from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'f1oracle.views.home', name='home'),
    # url(r'^f1oracle/', include('f1oracle.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
