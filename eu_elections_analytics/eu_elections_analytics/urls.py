from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'eu_elections_analytics.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),
)
