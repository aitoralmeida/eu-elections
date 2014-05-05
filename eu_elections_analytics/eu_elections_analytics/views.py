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

GROUPS = ['ALDE', 'EAF', 'ECR', 'EFD', 'EPP', 'GUE/NGL', 'Greens', 'S&D']


####################################################################################################
#####   View: home()
####################################################################################################

def home(request):
    groups = []

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        for group in GROUPS:
            group_data = {
                'initials': '',
                'slug': '',
                'name': '',
                'twitter_account': '',
                'top_hashtag': '',
                'parties': [],
            }

            cursor.execute("Select initials, slug, name from groups where initials = '%s'" % group)
            for result in cursor:
                group_data['initials'] = result[0]
                group_data['slug'] = result[1]
                group_data['name'] = result[2]

            cursor.execute("Select text from hash_group where group_id = '%s' and total = (SELECT MAX(total) from hash_group where group_id = '%s')" % (group, group))
            for result in cursor:
                group_data['top_hashtag'] = result[0]

            cursor.execute("Select screen_name from twitter_users where id = (select user_id from parties where group_id = '%s' and is_group_party = 1)" % group)
            for result in cursor:
                group_data['twitter_account'] = result[0]

            cursor.execute("Select twitter_users.screen_name, parties.initials, parties.name from twitter_users, parties where twitter_users.id = parties.user_id and twitter_users.id in (select user_id from parties where group_id = '%s' and is_group_party = 0)" % group)
            for result in cursor:
                party_data = {
                    'screen_name': result[0],
                    'initials': result[1],
                    'name': result[2]
                }

            # twitter_id = None;
            # cursor.execute("Select initials, name, user_id from parties where group_id = '%s' and is_group_party = 0" % group)
            # for result in cursor:
            #     party_data = {
            #         'screen_name': None,
            #         'initials': result[0],
            #         'name': result[1]
            #     }

            #     twitter_id = result[2]
            #     # twitter_id = int(result[2])

            # if twitter_id != '0':
            #     try:
            #         cursor.execute("Select screen_name from twitter_users where id = %s" % twitter_id)
            #         for r in cursor:
            #             party_data['screen_name'] = r[0]
            #             print party_data
            #     except:
            #         pass

                group_data['parties'].append(party_data)

            groups.append(group_data)

        cursor.close()
        cnx.close()

    except:
        print "You are not in Deusto's network"

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
#####   View: interaction_communities()
####################################################################################################

def interaction_communities(request):
    return render(request, "eu_elections_analytics/interaction_communities.html")


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

    try:
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

    except:
        print "You are not in Deusto's network"

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

    try:
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

    except:
        print "You are not in Deusto's network"

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

    try:
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

    except:
        print "You are not in Deusto's network"

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

    try:
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

    except:
        print "You are not in Deusto's network"

    return_dict = {
        'country': country,
        'hashtags': hashtags,
        'number': len(hashtags),
    }

    return render(request, "eu_elections_analytics/hashtags/by_country.html", return_dict)


####################################################################################################
#####   View: hashtag_evolution()
####################################################################################################

def hashtag_evolution(request):
    return render(request, "eu_elections_analytics/hashtags/evolution.html")


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

    try:
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

    except:
        print "You are not in Deusto's network"

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

    try:
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

    except:
        print "You are not in Deusto's network"

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

    try:
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

    except:
        print "You are not in Deusto's network"

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
