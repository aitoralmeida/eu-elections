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
