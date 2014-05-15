from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'eu_elections_analytics.views.home', name='home'),

    url(r'^grupo_parlamentario/(?P<group_slug>\S+)/$', 'eu_elections_analytics.views.view_group', name='view_group'),
    url(r'^partidos_en_el_mapa/$', 'eu_elections_analytics.views.geo_group_representation', name='geo_group_representation'),
    url(r'^interacciones_en_twitter/$', 'eu_elections_analytics.views.interaction_communities', name='interaction_communities'),
    url(r'^quienes_somos/$', 'eu_elections_analytics.views.about_us', name='about_us'),

    url(r'^menciones/$', 'eu_elections_analytics.views.mentions_es', name='mentions_es'),
    url(r'^mentions/$', 'eu_elections_analytics.views.mentions_en', name='mentions_en'),

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
    url(r'^hashtags/evolucion/$', 'eu_elections_analytics.views.hashtags_evolution', name='hashtags_evolution'),


    # LANGUAGES
    #   Candidates
    url(r'^idiomas/candidato/(?P<candidate_screen_name>\S+)/$', 'eu_elections_analytics.views.languages_by_candidate', name='languages_by_candidate'),
    url(r'^idiomas/candidato/$', 'eu_elections_analytics.views.languages_candidate_index', name='languages_candidate_index'),
    #   Country
    url(r'^idiomas/pais/(?P<country_slug>\S+)/$', 'eu_elections_analytics.views.languages_by_country', name='languages_by_country'),
    url(r'^idiomas/pais/$', 'eu_elections_analytics.views.languages_country_index', name='languages_country_index'),
    #     # Group
    url(r'^idiomas/grupo_parlamentario/(?P<group_slug>\S+)/$', 'eu_elections_analytics.views.languages_by_group', name='languages_by_group'),
    url(r'^idiomas/grupo_parlamentario/$', 'eu_elections_analytics.views.languages_group_index', name='languages_group_index'),
)
