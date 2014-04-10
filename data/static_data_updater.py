# -*- coding: utf-8 -*-
"""
Created on Wed Apr 09 10:35:28 2014

@author: aitor
"""

import mysql.connector

config = {
    'user': 'elections',
    'password': 'elections',
    'host': 'thor.deusto.es',
    'database': 'eu_test',
}

def load_locations():
    locs = {}
    countries = set()
    country_cities = {}
    with open('./locations_reverse_geocoding/locations.csv', 'r') as infile:
        
        for line in infile:
            if not 'city' in line:
                tokens = line.split(',')
                city = tokens[0]
                country = tokens[1]
                lat = tokens[2]
                lon= tokens[3]
                
                countries.add(country)                
                if country in country_cities.keys():
                    country_cities[country].append(city)
                else:
                    country_cities[country] = [city]
                locs[city] = (lat, lon)
     
    print 'Total countries', len(countries)    
    print 'Total cities', len(locs)                
                
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    
    for country in countries:
        print 'Adding', country
        query = "INSERT INTO countries (short_name, long_name) VALUES ('" + country  + "', '" + country + "')"

        cursor.execute(query)
        for city in country_cities[country]:
            print 'Adding', city
            query = "INSERT INTO locations (city, lat, lon, country_id) VALUES ('" + city +"', " + lat + ", " + lon + ", '" + country +"')"
            cursor.execute(query)

    
    cursor.close()
    cnx.close()
    
def get_party_ids():
    ids = {}
    with open('twitter_ids.csv', 'r') as infile:
        for line in infile:
            screen_name, twitter_id = line.split(',')
            ids[screen_name] = twitter_id
            
    return ids
    
def load_parties():
    ids = get_party_ids()
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    with open('parties.csv', 'r') as infile:
        for line in infile:
            #GUE/NGL,Bloco de esquerda,Left block,GPBloco,Lisbon, Portugal
            if len(line.split(',')) == 6:
                group, initials, name, screen_name, city, country = line.split(',')
                is_group_party = 0
            elif len(line.split(',')) == 5:
                group, initials, name, screen_name, __ = line.split(',')
                city = "none"
                is_group_party = 1
            else:
                print line
            
            if screen_name == '':
                screen_name = "NO"
                
            if screen_name != "NO": 
                twitter_id = ids[screen_name]
            else:
                twitter_id = 0

            query = "INSERT INTO parties (initials, location, group_id, name, is_group_party, user_id) VALUES ('" + initials  + "', '" + city + "', '" + group + "', '" + name + "', " + str(is_group_party) + ", " + str(twitter_id) +");"
            try:            
             cursor.execute(query)
            except:
                print line
                break

    cnx.commit()    
    cursor.close()
    cnx.close()  
    
    
def load_groups():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    ids = get_party_ids()
    with open('groups.csv', 'r') as infile:
        for line in infile:
            #GUE/NGL,European Left ,GUENGL,tsipras_eu,
            group, name, screename, candidate, subcandidate = line.split(',')
            try:            
                candidate_id = ids[candidate]
            except KeyError:
                print candidate
                candidate_id = 0
            try:            
                subcandidate_id = ids[subcandidate]
            except KeyError:
                print subcandidate
                subcandidate_id = 0
            try:
                user_id = ids[screename]
            except KeyError:
                print screename
                user_id = 0
            query = "INSERT INTO groups (initials, candidate_id, subcandidate_id, name, total_tweets, user_id) VALUES ('" + group  + "', " + str(candidate_id) + ", " +  str(subcandidate_id) + ", '" + name + "', 0, " + str(user_id)  + ");"
            print query                     
            cursor.execute(query)
            

    cnx.commit()
    cursor.close()
    cnx.close()  
       
        

    
load_parties()

print 'done'
        
        
