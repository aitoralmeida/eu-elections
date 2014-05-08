#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from decimal import *

import mysql.connector


# Create your views here.

config = {
    'user': 'elections',
    'password': 'elections',
    'host': 'thor.deusto.es',
    'database': 'eu_test2',
}

GROUPS = ['AECR', 'ALDE', 'EPP', 'Greens/EFA', 'MELD', 'PEL', 'PES']


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
                'top_hashtag_count': '',
                'parties': [],
                'discourse': '',
                'languages': [],
            }

            cursor.execute("Select initials, slug, name from groups where initials = '%s'" % group)
            for result in cursor:
                group_data['initials'] = result[0]
                group_data['slug'] = result[1]
                group_data['name'] = result[2]

            cursor.execute("Select text, sum(total) from hash_group where group_id = '%s' group by text order by total DESC limit 1" % group)
            for result in cursor:
                group_data['top_hashtag'] = result[0]
                group_data['top_hashtag_count'] = result[1]

            cursor.execute("Select screen_name from twitter_users where id = (select user_id from parties where group_id = '%s' and is_group_party = 1)" % group)
            for result in cursor:
                group_data['twitter_account'] = result[0]

            #cursor.execute("Select twitter_users.screen_name, parties.initials, parties.name from twitter_users, parties where twitter_users.id = parties.user_id and twitter_users.id in (select user_id from parties where group_id = '%s' and is_group_party = 0)" % group)

            cursor.execute("SELECT initials, name, user_id FROM parties WHERE group_id = '%s' and is_group_party = 0" % group)
            for result in cursor:
                party_initials = result[0]
                party_name = result[1]
                party_id = result[2]
                party_data = {
                    'id': party_id,
                    'initials': party_initials,
                    'name': party_name,
                }
                group_data['parties'].append(party_data)

            for party in group_data['parties']:
                if party['id'] == 0:
                    party['screen_name'] = None
                else:
                    cursor.execute("SELECT screen_name FROM twitter_users WHERE id = '%s'" % party['id'])
                    for result in cursor:
                        party['screen_name'] = result[0]

            cursor.execute("Select eu_total, co_total from europe_group where group_id = '%s'" % group)
            for result in cursor:
                europe_mentions = result[0]
                country_mentions = result[1]
                total = europe_mentions + country_mentions

                getcontext().prec = 3

                discourse_data = {
                    'european': (Decimal(europe_mentions) / Decimal(total)) * 100,
                    'national': (Decimal(country_mentions) / Decimal(total)) * 100,
                }

                group_data['discourse'] = discourse_data

            total_lang = 0
            cursor.execute("Select sum(total) from language_group where group_id = '%s'" % group)
            for result in cursor:
                total_lang = result[0]

            cursor.execute("Select lang, total from language_group where group_id = '%s' order by total desc limit 5" % group)
            for result in cursor:
                language = result[0]
                percentage = (Decimal(result[1]) / Decimal(total_lang)) * 100
                group_data['languages'].append({
                    'language': language,
                    'percentage': percentage,
                })

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
#####   View: view_group()
####################################################################################################

def view_group(request, group_slug):
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        group = {
            'initials': '',
            'slug': '',
            'name': '',
            'twitter_account': '',
            'top_hashtag': '',
            'top_hashtag_count': '',
            'parties': [],
            'discourse': '',
            'languages': [],
            'screen_name': None,
        }

        cursor.execute("Select initials, name from groups where slug = '%s'" % group_slug)
        for result in cursor:
            group['initials'] = result[0]
            group['slug'] = group_slug
            group['name'] = result[1]

        cursor.execute("Select text, sum(total) from hash_group where group_id = '%s' group by text order by total DESC limit 1" % group['initials'])
        for result in cursor:
            group['top_hashtag'] = result[0]
            group['top_hashtag_count'] = result[1]

        cursor.execute("Select screen_name from twitter_users where id = (select user_id from parties where group_id = '%s' and is_group_party = 1)" % group['initials'])
        for result in cursor:
            group['twitter_account'] = result[0]

        #cursor.execute("Select twitter_users.screen_name, parties.initials, parties.name from twitter_users, parties where twitter_users.id = parties.user_id and twitter_users.id in (select user_id from parties where group_id = '%s' and is_group_party = 0)" % group)

        cursor.execute("SELECT initials, name, user_id FROM parties WHERE group_id = '%s' and is_group_party = 0" % group['initials'])
        for result in cursor:
            party_initials = result[0]
            party_name = result[1]
            party_id = result[2]
            party_data = {
                'id': party_id,
                'initials': party_initials,
                'name': party_name,
            }
            group['parties'].append(party_data)

        for party in group['parties']:
            if party['id'] == 0:
                party['screen_name'] = None
            else:
                cursor.execute("SELECT screen_name FROM twitter_users WHERE id = '%s'" % party['id'])
                for result in cursor:
                    party['screen_name'] = result[0]

        cursor.execute("Select eu_total, co_total from europe_group where group_id = '%s'" % group['initials'])
        for result in cursor:
            europe_mentions = result[0]
            country_mentions = result[1]
            total = europe_mentions + country_mentions

            getcontext().prec = 3

            discourse_data = {
                'european': (Decimal(europe_mentions) / Decimal(total)) * 100,
                'national': (Decimal(country_mentions) / Decimal(total)) * 100,
            }

            group['discourse'] = discourse_data

        total_lang = 0
        cursor.execute("Select sum(total) from language_group where group_id = '%s'" % group['initials'])
        for result in cursor:
            total_lang = result[0]

        cursor.execute("Select lang, total from language_group where group_id = '%s' order by total desc limit 5" % group['initials'])
        for result in cursor:
            language = result[0]
            percentage = (Decimal(result[1]) / Decimal(total_lang)) * 100
            group['languages'].append({
                'language': language,
                'percentage': percentage,
            })

        cursor.execute("Select screen_name from twitter_users where id = (Select user_id from parties where is_group_party = 1 and group_id = '%s')" % group['initials'])
        for result in cursor:
            group['screen_name'] = result[0]

        cursor.close()
        cnx.close()

    except:
        print "You are not in Deusto's network"

    return_dict = {
        'group': group,
    }

    return render(request, "eu_elections_analytics/group.html", return_dict)


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
#####   View: hashtags_country_index()
####################################################################################################

def hashtags_country_index(request):
    countries = []

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        cursor.execute("Select long_name, slug from countries")

        for result in cursor:
            countries.append({
                'long_name': result[0],
                'slug': result[1],
            })

        cursor.close()
        cnx.close()

    except:
        print "You are not in Deusto's network"

    return_dict = {
        'countries': countries,
    }

    return render(request, "eu_elections_analytics/hashtags/country_index.html", return_dict)


####################################################################################################
#####   View: hashtags_group_index()
####################################################################################################

def hashtags_group_index(request):
    return render(request, "eu_elections_analytics/hashtags/group_index.html")


####################################################################################################
#####   View: hashtags_candidate_index()
####################################################################################################

def hashtags_candidate_index(request):
    return render(request, "eu_elections_analytics/hashtags/candidate_index.html")


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

        cursor.execute("Select text, sum(total) from hash_group where group_id = '%s' group by text" % group['initials'])

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

        cursor.execute("Select text, sum(total) from hash_candidate where candidate_id = '%s' group by text" % candidate['id'])

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

        cursor.execute("Select text, sum(total) from hash_country where country_id = '%s' group by text" % country['long_name'])

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
#####   View: languages_country_index()
####################################################################################################

def languages_country_index(request):
    countries = []

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        cursor.execute("Select long_name, slug from countries")

        for result in cursor:
            countries.append({
                'long_name': result[0],
                'slug': result[1],
            })

        cursor.close()
        cnx.close()

    except:
        print "You are not in Deusto's network"

    return_dict = {
        'countries': countries,
    }

    return render(request, "eu_elections_analytics/languages/country_index.html", return_dict)


####################################################################################################
#####   View: languages_group_index()
####################################################################################################

def languages_group_index(request):
    return render(request, "eu_elections_analytics/languages/group_index.html")


####################################################################################################
#####   View: languages_candidate_index()
####################################################################################################

def languages_candidate_index(request):
    return render(request, "eu_elections_analytics/languages/candidate_index.html")


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
    languages = []
    country = None

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        cursor.execute("Select long_name from countries where slug = '%s'" % country_slug)
        for result in cursor:
            country = {
                'long_name': result[0],
            }

        cursor.execute("Select lang, total from language_country where country_name= '%s' group by lang" % country['long_name'])

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
        'country': country,
        'languages': languages,
        'number': len(languages),
    }

    return render(request, "eu_elections_analytics/languages/by_country.html", return_dict)
