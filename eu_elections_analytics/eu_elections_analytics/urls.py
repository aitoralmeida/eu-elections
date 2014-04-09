from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'eu_elections_analytics.views.home', name='home'),

    url(r'^group_representation_by_country/$', 'eu_elections_analytics.views.group_representation_by_country', name='group_representation_by_country'),
    url(r'^party_representation_on_map/$', 'eu_elections_analytics.views.party_representation_on_map', name='party_representation_on_map'),

    url(r'^map1/$', 'eu_elections_analytics.views.map1', name='map1'),
    url(r'^map2/$', 'eu_elections_analytics.views.map2', name='map2'),

    url(r'^admin/', include(admin.site.urls)),
)
