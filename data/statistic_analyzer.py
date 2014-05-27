# -*- coding: utf-8 -*-
"""
Created on Thu May 15 14:51:05 2014

@author: aitor
"""

import mysql.connector
import cache
import networkx as nx
import scipy.stats
import csv
import pandas as pd
from pandas import DataFrame
import numpy as np
import matplotlib as plt

config = {
    'user': 'elections',
    'password': 'elections',
    'host': 'thor.deusto.es',
    'database': 'eu_test2',
}

def get_candidate_data():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    
    candidates = ['JunckerEU', 'tsipras_eu', 'GuyVerhofstadt', 'josebove', 'SkaKeller', 'MartinSchulz']
    for candidate in candidates:
        
        print '*******************************************'
        print candidate
        c_id = ''
        query = "SELECT id from twitter_users WHERE screen_name='%s';" % (candidate)
        cursor.execute(query)
        for result in cursor:
            c_id = result[0]
        print c_id
        
        print
        print 'LANGUAGES'
        query = "SELECT lang, total FROM language_candidate WHERE candidate_id='%s' ORDER BY total DESC;" % (c_id)
        cursor.execute(query)
        for result in cursor:
            print result[0], result[1]
        
        print
        print 'MENTIONS'
        query = "SELECT eu_total, co_total FROM europe_candidate WHERE candidate_id='%s';" % (c_id)
        cursor.execute(query)
        for result in cursor:
            print 'Europe', result[0], 'Country', result[1]
         
        print
        print 'HASHTAGS'
        query = "SELECT text, SUM(total) FROM hash_candidate WHERE candidate_id='%s' GROUP BY text ORDER BY sum(total) DESC;" % (c_id)
        cursor.execute(query)
        i = 0
        for result in cursor:
            if i < 6:
                print result[0], result[1]
                i +=1
        print
        print 
            

    cursor.close()        
    cnx.close()
    
def get_total_tweets_by_date_country():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    
    tweets_country_day = {}
    countries = set()   
    day_names = set()

    for i, party in enumerate(cache.parties):
        print '%i of %i' % (i, len(cache.parties))
        try:
            if cache.parties[party]['group_id'] == 'NI - SPAIN':
                continue
            
            country = cache.locations[cache.parties[party]['location']]
            countries.add(country)
            if not tweets_country_day.has_key(country):
                tweets_country_day[country] = {}
        except:
            continue

        cursor.execute("SELECT created_at, count(*) FROM tweets WHERE user_id='%s' GROUP BY created_at" % cache.parties[party]['user_id']) 
          
        for result in  cursor:
            day = result[0]
            day_names.add(str(day))
            total = result[1]
            if tweets_country_day[country].has_key(str(day)):
                tweets_country_day[country][str(day)] += total
            else: 
                tweets_country_day[country][str(day)] = total
   
            
    countries = list(countries)
    countries.sort()
    day_names = list(day_names)
    day_names.sort()
    days = {}
    for country in countries:   
        for day in day_names:
            if not days.has_key(day):
                days[day] = []
               
            try:
                days[day].append(tweets_country_day[country][day])
            except:
                days[day].append(0)           
           
           
#    print days
#    print countries   

    frame = DataFrame(days, index = countries)
    
    return frame    


def get_total_tweets_by_date_group():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    
    tweets_group_day = {}
    groups = set()   
    day_names = set()

    for i, party in enumerate(cache.parties):
        print '%i of %i' % (i, len(cache.parties))
        try:
            if cache.parties[party]['group_id'] == 'NI - SPAIN':
                continue
            
            group = cache.parties[party]['group_id']
            groups.add(group)
            if not tweets_group_day.has_key(group):
                tweets_group_day[group] = {}
        except:
             continue

        cursor.execute("SELECT created_at, count(*) FROM tweets WHERE user_id='%s' GROUP BY created_at" % cache.parties[party]['user_id']) 
          
        for result in  cursor:
            day = result[0]
            day_names.add(str(day))
            total = result[1]
            if tweets_group_day[group].has_key(str(day)):
                tweets_group_day[group][str(day)] += total
            else: 
                tweets_group_day[group][str(day)] = total
   
            
    groups = list(groups)
    groups.sort()
    day_names = list(day_names)
    day_names.sort()
    days = {}
    for group in groups:   
        for day in day_names:
            if not days.has_key(day):
                days[day] = []
               
            try:
                days[day].append(tweets_group_day[group][day])
            except:
                days[day].append(0)           
           
           
    print days
    print groups   

    frame = DataFrame(days, index = groups)
    
    return frame             
             
   
    
def get_country_relations():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    G = nx.Graph()
    country_tweets = {}
    
    for party1 in cache.parties:
        try:
            if cache.parties[party1]['group_id'] == 'NI - SPAIN':
                continue
            
            country1 = cache.locations[cache.parties[party1]['location']]
            if not G.has_node(country1):
                G.add_node(country1)
        except:
            continue
        
        
        
#        
#        cursor.execute("SELECT count(*) FROM tweets where user_id = '%s' " % cache.parties[party1]['user_id']) 
#        for result in cursor:
#            total_tweets = result[0]
#            
#        if country_tweets.has_key(country1):
#            country_tweets[country1] += total_tweets
#        else:
#            country_tweets[country1] = total_tweets
                
        for party2 in cache.parties:
            if cache.parties[party2]['group_id'] == 'NI - SPAIN':
                continue
            
            if party1 != party2:     
                try:
                    country2 = cache.locations[cache.parties[party2]['location']]
                    if not G.has_node(country2):
                        G.add_node(country2)
                except:
                    continue
                cursor.execute("SELECT sum(weight) FROM interactions WHERE user_id='%s' AND target_id='%s'" % (cache.parties[party1]['user_id'], cache.parties[party2]['user_id']))
                weight = 0                
                for result in cursor:
                    try:
                        weight = int(result[0])
                    except:
                        pass
                if weight != 0:
                    if G.has_edge(country1, country2):
                        G.edge[country1][country2]['weight'] += weight
                    else:
                        G.add_edge(country1, country2, weight = weight)
                                    
    cursor.close()        
    cnx.close()
    
    print country_tweets
    nx.write_gexf(G, open('./sna/country_relations.gexf', 'w'))   
    return G
    
def get_party_relations(): 
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    G = nx.Graph()

    for party1 in cache.parties:    
        if cache.parties[party1]['group_id'] == 'NI - SPAIN':
                continue
        for party2 in cache.parties:
            if cache.parties[party2]['group_id'] == 'NI - SPAIN':
                continue
            
            if party1 == party2:
                continue
            
            if not G.has_node(party1):
                G.add_node(party1)
                
            if not G.has_node(party2):
                G.add_node(party2)
  
            cursor.execute("SELECT sum(weight) FROM interactions WHERE user_id='%s' AND target_id='%s'" % (cache.parties[party1]['user_id'], cache.parties[party2]['user_id']))
            weight = 0                
            for result in cursor:
                try:
                    weight = int(result[0])
                except:
                    pass  
                
            if weight != 0:
                if G.has_edge(party1, party2):
                    G.edge[party1][party2]['weight'] += weight
                else:
                    G.add_edge(party1, party2, weight = weight)
              
    cursor.close()        
    cnx.close()
    
    print len(G.nodes())
    print len(G.edges())
    
    nx.write_gexf(G, open('./sna/party_relations.gexf', 'w'))  
    return G
    
def get_countries_sna():
    country_data = {}
    print 'Building relations graph'
    G = nx.read_gexf('./sna/country_relations.gexf')
        
    print 'Calculating centralities'
    degrees = G.degree()
    for c in degrees:
        country_data[c] = { 'degree':degrees[c],
                            'betweenness':0,
                            'closeness':0,
                            'eigenvector':0}
        
    betweenness = nx.betweenness_centrality(G)
    for c in betweenness:
        country_data[c]['betweenness'] = betweenness[c]
        
    closeness = nx.closeness_centrality(G)
    for c in closeness:
        country_data[c]['closeness'] = closeness[c]
        
    eigenvector = nx.eigenvector_centrality(G)
    for c in eigenvector:
        country_data[c]['eigenvector'] = eigenvector[c]
        
    return country_data

def get_countries_activity():
    print 'Recovering countries twitter activity'
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    country_data = {}
    
    for i, party in enumerate(cache.parties):
        print '%i of %i' % (i, len(cache.parties))
        if cache.parties[party]['group_id'] == 'NI - SPAIN':
                continue
        try:
            country = cache.locations[cache.parties[party]['location']]
        except:
            continue
        
        cursor.execute("select count(*) FROM tweets WHERE user_id = '%s'" % cache.parties[party]['user_id'])
        activity = 0
        for r in cursor:
            activity = r[0]
        if country_data.has_key(country):
            country_data[country] += activity
        else:
            country_data[country] = activity
        
    cursor.close()        
    cnx.close() 
    
    return country_data
    
  
def get_countries_discourse():
    print 'Recovering discourse info'
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('SELECT country_name, eu_total, co_total FROM europe_country')
    country_data = {}
    
    for r in cursor:
        country_name = r[0]
        europe = r[1]
        country = r[2]
                
        country_data[country_name] = {  'europe':europe,
                                        'country':country}
                                        
    return country_data
    
def get_countries_party_num():
    country_data = {}
    for party in cache.parties:
        if cache.parties[party]['group_id'] == 'NI - SPAIN':
            continue
        try:
            country = cache.locations[cache.parties[party]['location']]        
            if country in country_data.keys():
                country_data[country] += 1
            else:
                country_data[country] = 1  
        except:
            continue

        
    return country_data
    
    
def load_eurobarometer():
    country_data = {}
    with open('eurobarometer.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            country_data[row[1]] = {    'voice': row[2],
                                        'future': row[3],
                                        'economic': row[4],
                                        'citizen': row[5]      
            }
    return country_data
    


def get_country_metrics():
    sna = get_countries_sna()
    discourse = get_countries_discourse()
    eurobarometer = load_eurobarometer()
    activity = get_countries_activity()
    num_parties = get_countries_party_num()
    
    
    countries = []
    country_parties = []     
    degrees = []
    betweenness = []
    closeness = []
    eigenvector = []
    total_tweets = []
    discourse_europe_per = []
    discourse_europe_uses = []
    discourse_country_per = []
    discourse_country_uses = []
    voice_positive = []
    future_europe = []
    economic_union = []
    be_citizen = []
    
    for country in sna:
        countries.append(country)
        country_parties.append(num_parties[country])
        degrees.append(sna[country]['degree'])
        betweenness.append(sna[country]['betweenness'])
        closeness.append(sna[country]['closeness'])
        eigenvector.append(sna[country]['eigenvector'])
        
        total_tweets.append(activity[country])
        
        try:
            europe_use = float(discourse[country]['europe'])
            country_use = float(discourse[country]['country'])
            tweets_num = activity[country]
            
            discourse_europe_per.append(europe_use/tweets_num)
            discourse_europe_uses.append(europe_use/(europe_use + country_use))
            discourse_country_per.append(country_use/tweets_num)
            discourse_country_uses.append(country_use/(europe_use + country_use))
        
        except:
            discourse_europe_per.append(0)
            discourse_europe_uses.append(0)
            discourse_country_per.append(0)
            discourse_country_uses.append(0)
        
        
        try:
            voice_positive.append(float(eurobarometer[country]['voice'])/100)
            future_europe.append(float(eurobarometer[country]['future'])/100)
            economic_union.append(float(eurobarometer[country]['economic'])/100)
            be_citizen.append(float(eurobarometer[country]['citizen'])/100)
        except:
            print 'Error', country
            
    tweet_per_party = list(np.array(total_tweets)/np.array(country_parties))
    
    data = { 'degrees': degrees,
             'betweenness': betweenness,
             'closeness': closeness,
             'eigenvector': eigenvector,
             'total_tweets': total_tweets,
             'voice_positive': voice_positive,
             'future_europe': future_europe,
             'economic_union': economic_union,
             'be_citizen': be_citizen,
             'discourse_europe_per': discourse_europe_per,
             'discourse_europe_uses': discourse_europe_uses,
             'discourse_country_per': discourse_country_per,
             'discourse_country_uses': discourse_country_uses,
             'country_parties' : country_parties,
             'tweet_per_party' : tweet_per_party
    }
    
    print data
    print countries
    data_frame = DataFrame(data, index = countries)
            
    sna_metrics = { 'degrees': degrees,
                    'betweenness': betweenness,
                    'closeness': closeness,
                    'eigenvector': eigenvector,
                    'total_tweets': total_tweets,
                    'country_parties' : country_parties,
                    'tweet-per-party': tweet_per_party
    }
    
    eurobarometer_metrics = { 'voice_positive': voice_positive,
                              'future_europe': future_europe,
                              'economic_union': economic_union,
                              'be_citizen': be_citizen    
    }
    
    discourse_metrics = {'discourse_europe_per': discourse_europe_per,
                         'discourse_europe_uses': discourse_europe_uses,
                         'discourse_country_per': discourse_country_per,
                         'discourse_country_uses': discourse_country_uses
    }
    
    metrics = [sna_metrics, eurobarometer_metrics, discourse_metrics]
    
    return data_frame, metrics
    
    
def get_metrics_correlations(metrics): 
    for i in range(0, len(metrics)):
        for j in range(i+1, len(metrics)):
            metric_group_1 = metrics[i]
            metric_group_2 = metrics[j]
            for m1 in metric_group_1:
                for m2 in metric_group_2:
 
                    print '*', m1, '-',  m2
                   
                    spearman = scipy.stats.spearmanr(metric_group_1[m1], metric_group_2[m2])
                    pearson = scipy.stats.pearsonr(metric_group_1[m1], metric_group_2[m2])
                    correlation = False
                    if spearman[0] > 0.3 or spearman[0] < -0.3:                    
                        print 'spearman:', spearman 
                        correlation = True
                    if pearson[0] > 0.3 or pearson[0] < -0.3: 
                        print 'pearson:', pearson
                        correlation = True
                    if correlation == False:
                        print 'No correlation'
                        

                        
def get_summary_statistics(frame):    
    print '\n-Tweets:' 
    print frame.sort_index(by='total_tweets', ascending=False)['total_tweets']
    print '\n-Total tweets:'
    print frame.sum()['total_tweets']
    print '\n-Max Countries:'
    print frame.idxmax()
    print '\n-Min  Countries:'
    print frame.idxmin()
    print '\n-Mean:'
    print frame.mean()
    print '\n-Median:'
    print frame.median()
    print '\n-std:'
    print frame.std()


print ("\n*************ANALYZE COUNTRY METRICS*************************")
        
data_frame, metrics = get_country_metrics()

#Tweets per party group by country graph
ax = data_frame.sort_index(by='tweet_per_party', ascending=False)['tweet_per_party'].plot(kind='bar')
ax.set_xticklabels([x.get_text() for x in ax.get_xticklabels()], fontsize=6, rotation=60)
fig = ax.get_figure()
fig.savefig('tweet_per_party_by_country.png')

print '\n****SUMMARY STATISTICS****'
get_summary_statistics(data_frame)
print '\n****METRIC CORRELATIONS****'
get_metrics_correlations(metrics)


print ("\n\n\n*************ANALYZE TIMELINE BY COUNTRY************************")

t_country_day = get_total_tweets_by_date_country()
tweet_metrics = []
for c in t_country_day.T:
    tweet_metrics.append( {c:list(t_country_day.T[c])} )
    
    
print '\n****COUNTRY PER DAY TWEETS CORRELATIONS****'
get_metrics_correlations(tweet_metrics) 


print ("\n\n\n*************ANALYZE TIMELINE BY GROUP************************")

t_group_day = get_total_tweets_by_date_group()
tweet_metrics = []
for c in t_group_day.T:
    tweet_metrics.append( {c:list(t_group_day.T[c])} )
    
    
print '\n****GROUP PER DAY TWEETS CORRELATIONS****'
get_metrics_correlations(tweet_metrics) 

#Tweets per party group by country graph
ax = t_group_day.T.plot()
ax.set_xticklabels([x.get_text() for x in ax.get_xticklabels()], fontsize=6, rotation=60)
fig = ax.get_figure()
fig.savefig('tweet_per_day_bygroup.png')


print 'done'