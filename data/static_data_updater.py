# -*- coding: utf-8 -*-
"""
Created on Wed Apr 09 10:35:28 2014

@author: aitor
"""

import mysql.connector
from slugify import slugify

config = {
    'user': 'elections',
    'password': 'elections',
    'host': 'thor.deusto.es',
    'database': 'eu_test2',
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
        slug_country = slugify(country)
        query = "INSERT INTO countries (long_name, slug) VALUES ('" + country  + "', '" + slug_country + "')"

        cursor.execute(query)
        for city in country_cities[country]:
            print 'Adding', city
            slug_city = slugify(city)
            query = "INSERT INTO locations (city, lat, lon, country_id, slug) VALUES ('" + city +"', " + lat + ", " + lon + ", '" + country +"', '" + slug_city + "')"
            cursor.execute(query)

    
    cnx.commit()     
    cursor.close()
    cnx.close()
    
def get_party_ids():
    ids = {}
    with open('export_twitter_accounts.csv', 'r') as infile:
        for line in infile:
            screen_name, twitter_id = line.split(',')
            screen_name = screen_name.replace('@', '')
            ids[screen_name] = twitter_id
            
    return ids
    
def get_cities():
    geo_cod = {}    
    
    with open('./locations_reverse_geocoding/locations.csv', 'r') as infile:
        
        for line in infile:
            if not 'city' in line:
                tokens = line.split(',')
                city = tokens[0]
                country = tokens[1]

                geo_cod[country] = city
    
    return geo_cod
    
    
def load_parties():
    ids = get_party_ids()
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    
    geo_cod = get_cities()
    with open('export_party_info.csv', 'r') as infile:
        for line in infile:
            working_line = line.replace('\n', '')
            #GUE/NGL,Bloco de esquerda, GPBloco,Lisbon, Portugal
            print line
            print len(working_line.split(','))
            if len(working_line.split(',')) == 6:
                group, name, screen_name, country, lat, lon = working_line.split(',')
                name = name.strip().replace("'", "")
                group = group.strip()
                country = country.strip()
                screen_name = screen_name.strip().replace('@', '')
                lat = lat.strip()
                lon = lon.strip()
                try:
                    is_group_party = 0
                    city = geo_cod[country]
                except:
                    city = "none"
                    is_group_party = 1
                    lat = 0
                    lon = 0
                
                
            elif len(working_line.split(',')) == 3:
                group, name, screen_name = working_line.split(',')
                city = "none"
                is_group_party = 1
            else:
                print 'Unexpected number of tokens'
                print line
                break
            
            if screen_name == '' or screen_name == '"NO':
                screen_name = "NO"
                
            if screen_name != '"NO"' and screen_name != 'NO': 
                twitter_id = ids[screen_name]
            else:
                twitter_id = 0
                

            slug = slugify(name)
            query = "INSERT INTO parties (initials, location, group_id, name, is_group_party, user_id, slug, lat, lon) VALUES ('" + slug  + "', '" + city + "', '" + group + "', '" + name + "', " + str(is_group_party) + ", " + str(twitter_id) +", '" + slug + "', " + str(lat)+ ", " + str(lon) + ");"
            print query
            cursor.execute(query)            
#            try:            
#             cursor.execute(query)
#            except:
#                print 'error'
#                break

    cnx.commit()    
    cursor.close()
    cnx.close()  
    
    
def load_groups():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    ids = get_party_ids()
    with open('export_groups.csv', 'r') as infile:
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
                
            slug = slugify(group)
            query = "INSERT INTO groups (initials, candidate_id, subcandidate_id, name, total_tweets, user_id, slug) VALUES ('" + group  + "', " + str(candidate_id) + ", " +  str(subcandidate_id) + ", '" + name + "', 0, " + str(user_id)  +", '" + slug + "');"
            print query   
            try:                  
                cursor.execute(query)
            except mysql.connector.errors.IntegrityError:
                print 'Duplicated key'
            

    cnx.commit()
    cursor.close()
    cnx.close()  
       
        

    
load_parties()

print 'done'
        
        
