from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'eu_elections_analytics.views.home', name='home'),

    url(r'^group_representation_by_country/$', 'eu_elections_analytics.views.group_representation_by_country', name='group_representation_by_country'),
    url(r'^geo_group_representation/$', 'eu_elections_analytics.views.geo_group_representation', name='geo_group_representation'),
    url(r'^interaction_communities/$', 'eu_elections_analytics.views.interaction_communities', name='interaction_communities'),

    # HASHTAGS
    #   Candidates
    url(r'^hashtags/candidato/(?P<candidate_screen_name>\S+)/$', 'eu_elections_analytics.views.hashtags_by_candidate', name='hashtags_by_candidate'),
    url(r'^hashtags/candidato/$', 'eu_elections_analytics.views.hashtags_candidate_index', name='hashtags_candidate_index'),
    #   Country
    url(r'^hashtags/pais/(?P<country_slug>\S+)/$', 'eu_elections_analytics.views.hashtags_by_country', name='hashtags_by_country'),
    url(r'^hashtags/pais/$', 'eu_elections_analytics.views.hashtags_country_index', name='hashtags_country_index'),
    #     # Group
    url(r'^hashtags/grupo_parlamentario/(?P<group_slug>\S+)/$', 'eu_elections_analytics.views.hashtags_by_group', name='hashtags_by_group'),
    url(r'^hashtags/grupo_parlamentario/$', 'eu_elections_analytics.views.hashtags_group_index', name='hashtags_group_index'),
    #   Evolution
    url(r'^hashtags/evolucion/$', 'eu_elections_analytics.views.hashtag_evolution', name='hashtag_evolution'),


    # LANGUAGES
    #   Candidates
    url(r'^idiomas/candidato/(?P<candidate_screen_name>\S+)/$', 'eu_elections_analytics.views.languages_by_candidate', name='languages_by_candidate'),
    #   Country
    url(r'^idiomas/pais/(?P<country_slug>\S+)/$', 'eu_elections_analytics.views.languages_by_country', name='languages_by_country'),
    #     # Group
    url(r'^idiomas/grupo_parlamentario/(?P<group_slug>\S+)/$', 'eu_elections_analytics.views.languages_by_group', name='languages_by_group'),
    #   Evolution
    # url(r'^idiomas/evolucion/$', 'eu_elections_analytics.views.languages_evolution', name='languages_evolution'),
    #   Index
    url(r'^idiomas/$', 'eu_elections_analytics.views.languages', name='languages'),

    # url(r'^foo/$', 'eu_elections_analytics.views.foo', name='foo'),

    url(r'^admin/', include(admin.site.urls)),
)
