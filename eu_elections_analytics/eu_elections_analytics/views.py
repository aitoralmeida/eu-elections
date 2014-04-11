#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render

from eu_elections_analytics.models import Users, HashCandidate, Groups


# Create your views here.


####################################################################################################
#####   View: home()
####################################################################################################

def home(request):
    groups = Groups.objects.all()

    candidate_ids_set = set()

    for group in groups:
        candidate_ids_set.add(group.candidate_id)
        try:
            candidate_ids_set.add(group.subcandidate_id)
        except:
            pass

    candidate_ids = list(candidate_ids_set)

    candidates = Users.objects.filter(id__in=candidate_ids)

    return_dict = {
        'candidates': candidates,
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
    candidate = Users.objects.get(screen_name=candidate_screen_name)
    hashtags = HashCandidate.objects.filter(candidate_id=candidate.id)

    return_dict = {
        'candidate': candidate,
        'hashtags': hashtags,
    }
    return render(request, "eu_elections_analytics/hashtags/by_candidate.html", return_dict)


####################################################################################################
#####   View: hashtags_candidate_index()
####################################################################################################

def hashtags_candidate_index(request, country_slug):
    return render(request, "eu_elections_analytics/hashtags/by_country.html")


####################################################################################################
#####   View: hashtags_by_candidate()
####################################################################################################

def hashtags_by_candidate(request, candidate_slug):
    return render(request, "eu_elections_analytics/hashtags/by_candidate.html")


####################################################################################################
#####   View: hashtags_by_candidate()
####################################################################################################

def hashtags_by_candidate(request, candidate_slug):
    return render(request, "eu_elections_analytics/hashtags/by_candidate.html")
