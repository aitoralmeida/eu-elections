#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render

import mysql.connector


# Create your views here.

config = {
    'user': 'elections',
    'password': 'elections',
    'host': 'thor.deusto.es',
    'database': 'eu_test2',
}


####################################################################################################
#####   View: home()
####################################################################################################

def home(request):
    groups = []

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    cursor.execute("Select initials, slug from groups")

    for result in cursor:
        groups.append({
            'initials': result[0],
            'slug': result[1]
        })

    cursor.close()
    cnx.close()

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
#####   View: hashtags()
####################################################################################################

def hashtags(request):
    candidates = []
    countries = []
    groups = []

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    cursor.execute("Select initials, slug from groups")

    for result in cursor:
        groups.append({
            'initials': result[0],
            'slug': result[1],
        })

    cursor.execute("Select long_name, slug from countries")

    for result in cursor:
        countries.append({
            'long_name': result[0],
            'slug': result[1],
        })

    cursor.execute("SELECT screen_name FROM twitter_users WHERE id IN (SELECT CONVERT(candidate_id, CHAR(100)) FROM groups)")

    for result in cursor:
        candidates.append({
            'screen_name': result[0],
        })

    cursor.execute("SELECT screen_name FROM twitter_users WHERE id IN (SELECT CONVERT(subcandidate_id, CHAR(100)) FROM groups)")

    for result in cursor:
        candidates.append({
            'screen_name': result[0],
        })

    cursor.close()
    cnx.close()

    return_dict = {
        'candidates': candidates,
        'countries': countries,
        'groups': groups,
    }

    return render(request, "eu_elections_analytics/hashtags/index.html", return_dict)


####################################################################################################
#####   View: hashtags_by_group()
####################################################################################################

def hashtags_by_group(request, group_slug):
    hashtags = []
    group = None

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    cursor.execute("Select initials, user_id from groups where slug = '%s'" % group_slug)
    for result in cursor:
        group = {
            'initials': result[0],
            'user_id': result[1],
        }

    cursor.execute("Select text, total from hash_group where group_id = '%s'" % group['initials'])

    for result in cursor:
        hashtags.append({
            'text': result[0],
            'total': result[1],
        })

    cursor.close()
    cnx.close()

    return_dict = {
        'group': group,
        'hashtags': hashtags,
        'number': len(hashtags),
    }

    return render(request, "eu_elections_analytics/hashtags/by_group.html", return_dict)


####################################################################################################
#####   View: hashtags_by_candidate()
####################################################################################################

def hashtags_by_candidate(request, candidate_screen_name):
    hashtags = []
    candidate = None

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    cursor.execute("Select id, screen_name from twitter_users where screen_name = '%s'" % candidate_screen_name)
    for result in cursor:
        candidate = {
            'id': result[0],
            'screen_name': result[1],
        }

    cursor.execute("Select text, total from hash_candidate where candidate_id = '%s'" % candidate['id'])

    for result in cursor:
        hashtags.append({
            'text': result[0],
            'total': result[1],
        })

    cursor.close()
    cnx.close()

    return_dict = {
        'candidate': candidate,
        'hashtags': hashtags,
        'number': len(hashtags),
    }
    return render(request, "eu_elections_analytics/hashtags/by_candidate.html", return_dict)


####################################################################################################
#####   View: hashtags_by_country()
####################################################################################################

def hashtags_by_country(request, country_slug):
    hashtags = []
    country = None

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    cursor.execute("Select long_name from countries where slug = '%s'" % country_slug)
    for result in cursor:
        country = {
            'long_name': result[0],
        }

    cursor.execute("Select text, total from hash_country where country_id = '%s'" % country['long_name'])

    for result in cursor:
        hashtags.append({
            'text': result[0],
            'total': result[1],
        })

    cursor.close()
    cnx.close()

    return_dict = {
        'country': country,
        'hashtags': hashtags,
        'number': len(hashtags),
    }

    return render(request, "eu_elections_analytics/hashtags/by_country.html", return_dict)


####################################################################################################
####################################################################################################
#####   LANGUAGES
####################################################################################################
####################################################################################################

####################################################################################################
#####   View: languages()
####################################################################################################

def languages(request):
    candidates = []
    countries = []
    groups = []

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    cursor.execute("Select initials, slug from groups")

    for result in cursor:
        groups.append({
            'initials': result[0],
            'slug': result[1],
        })

    cursor.execute("Select long_name, slug from countries")

    for result in cursor:
        countries.append({
            'long_name': result[0],
            'slug': result[1],
        })

    cursor.execute("SELECT screen_name FROM twitter_users WHERE id IN (SELECT CONVERT(candidate_id, CHAR(100)) FROM groups)")

    for result in cursor:
        candidates.append({
            'screen_name': result[0],
        })

    cursor.execute("SELECT screen_name FROM twitter_users WHERE id IN (SELECT CONVERT(subcandidate_id, CHAR(100)) FROM groups)")

    for result in cursor:
        candidates.append({
            'screen_name': result[0],
        })

    cursor.close()
    cnx.close()

    return_dict = {
        'candidates': candidates,
        'countries': countries,
        'groups': groups,
    }

    return render(request, "eu_elections_analytics/languages/index.html", return_dict)


####################################################################################################
#####   View: languages_by_group()
####################################################################################################

def languages_by_group(request, group_slug):
    languages = []
    group = None

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    cursor.execute("Select initials, user_id from groups where slug = '%s'" % group_slug)
    for result in cursor:
        group = {
            'initials': result[0],
            'user_id': result[1],
        }

    cursor.execute("Select lang, total from language_group where group_id = '%s'" % group['initials'])

    for result in cursor:
        languages.append({
            'lang': result[0],
            'total': result[1],
        })

    cursor.close()
    cnx.close()

    return_dict = {
        'group': group,
        'languages': languages,
        'number': len(languages),
    }

    return render(request, "eu_elections_analytics/languages/by_group.html", return_dict)


####################################################################################################
#####   View: languages_by_candidate()
####################################################################################################

def languages_by_candidate(request, candidate_screen_name):
    languages = []
    candidate = None

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    cursor.execute("Select id, screen_name from twitter_users where screen_name = '%s'" % candidate_screen_name)
    for result in cursor:
        candidate = {
            'id': result[0],
            'screen_name': result[1],
        }

    cursor.execute("Select lang, total from language_candidate where candidate_id = '%s'" % candidate['id'])

    for result in cursor:
        languages.append({
            'lang': result[0],
            'total': result[1],
        })

    cursor.close()
    cnx.close()

    return_dict = {
        'candidate': candidate,
        'languages': languages,
        'number': len(languages),
    }
    return render(request, "eu_elections_analytics/languages/by_candidate.html", return_dict)


####################################################################################################
#####   View: languages_by_country()
####################################################################################################

def languages_by_country(request, country_slug):
    return render(request, "eu_elections_analytics/languages/by_country.html")
