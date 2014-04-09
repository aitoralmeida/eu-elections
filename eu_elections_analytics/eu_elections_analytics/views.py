#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render


# Create your views here.


####################################################################################################
#####   View: home()
####################################################################################################

def home(request):
    return render(request, "eu_elections_analytics/index.html")


####################################################################################################
#####   View: group_representation_by_country()
####################################################################################################

def group_representation_by_country(request):
    return render(request, "eu_elections_analytics/group_representation_by_country.html")


####################################################################################################
#####   View: party_representation_on_map()
####################################################################################################

def party_representation_on_map(request):
    return render(request, "eu_elections_analytics/party_representation_on_map.html")


####################################################################################################
#####   View: map1()
####################################################################################################

def map1(request):
    return render(request, "eu_elections_analytics/map1.html")


####################################################################################################
#####   View: map2()
####################################################################################################

def map2(request):
    return render(request, "eu_elections_analytics/map2.html")
