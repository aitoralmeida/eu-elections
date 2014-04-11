#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render

from eu_elections_analytics.models import TwitterUsers, HashCandidate, HashGroup, Groups
import mysql.connector


# Create your views here.


####################################################################################################
#####   View: home()
####################################################################################################

def home(request):
    groups = Groups.objects.all()

    return_dict = {
        'groups': groups,
    }

    return render(request, "eu_elections_analytics/index.html", return_dict)


####################################################################################################
#####   View: group_representation_by_country()
####################################################################################################

def group_representation_by_country(request):
    return render(request, "eu_elections_analytics/group_representation_by_country.html")


####################################################################################################
#####   View: geo_group_representation()
####################################################################################################

def geo_group_representation(request):
    return render(request, "eu_elections_analytics/geo_group_representation.html")



####################################################################################################
####################################################################################################
#####   HASHTAGS
####################################################################################################
####################################################################################################


####################################################################################################
#####   View: hashtags_by_candidate()
####################################################################################################

def hashtags_by_candidate(request, candidate_screen_name):
    candidate = TwitterUsers.objects.get(screen_name=candidate_screen_name)
    hashtags = HashCandidate.objects.filter(candidate_id=candidate.id)

    return_dict = {
        'candidate': candidate,
        'hashtags': hashtags,
    }
    return render(request, "eu_elections_analytics/hashtags/by_candidate.html", return_dict)


####################################################################################################
#####   View: hashtags_by_group()
####################################################################################################

def hashtags_by_group(request, group_slug):
    group = Groups.objects.get(slug=group_slug)
    
    config = {
    'user': 'elections',
    'password': 'elections',
    'host': 'thor.deusto.es',
    'database': 'eu_test2',
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    cursor.execute("Select text, total from hash_group where group_id = '%s'" % group.user_id)
    results = {}
    for result in cursor:
	results[result[0]] = result[1]
    	

    #hashtags = HashGroup.objects.filter(group_id=group.user_id)

    return_dict = {
        'group': group,
        #'hashtags': hashtags,
        'results': results,
    }

    return render(request, "eu_elections_analytics/hashtags/by_group.html", return_dict)
