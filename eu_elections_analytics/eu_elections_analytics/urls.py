from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'eu_elections_analytics.views.home', name='home'),

    url(r'^group_representation_by_country/$', 'eu_elections_analytics.views.group_representation_by_country', name='group_representation_by_country'),
    url(r'^geo_group_representation/$', 'eu_elections_analytics.views.geo_group_representation', name='geo_group_representation'),

    url(r'^admin/', include(admin.site.urls)),
)
