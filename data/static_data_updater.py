# -*- coding: utf-8 -*-
"""
Created on Wed Apr 09 10:35:28 2014

@author: aitor
"""

import mysql.connector
from slugify import slugify
import json

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
    
def create_parties_json():
    with open('export_parties_with_wiki.csv', 'r') as infile:
        parties = []
        for line in infile:
            working_line = line.replace('\n', '')
            if len(working_line.split(',')) == 7:
                group, name, screen_name, country, wiki, lat, lon = working_line.split(',')
                group = group.strip()
                country = country.strip()
                screen_name = screen_name.strip().replace('@', '')
                lat = lat.strip()
                lon = lon.strip()
                
                party_data = {}
                party_data['name'] = name
                party_data['country'] = country
                party_data['group'] = group
                party_data['wikipedia_site'] = wiki
                party_data['lat'] = lat
                party_data['lng'] = lon
                
                parties.append(party_data)
                
        json.dump(parties, open('all_parties_data.json', 'w'), indent=4)
            

def test():
    languages = []
    group = None

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        cursor.execute("Select initials, user_id from groups where slug = '%s'" % 'ALDE')
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
    
    print return_dict
    
    languages = []
    country = None

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        cursor.execute("Select long_name from countries where slug = '%s'" % 'belgium')
        for result in cursor:
            country = {
                'long_name': result[0],
            }

        cursor.execute("Select lang, total from language_country where country_name= '%s' group by lang" % country['long_name'])

        for result in cursor:
            languages.append({
                'text': result[0],
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
    
    print 
    print
    print return_dict

        



    cursor.close()
    cnx.close()

 
def clean_party_names():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    
    bad_names = []
    cursor.execute("Select name from parties")
    for result in cursor:
        name = result[0]
        if '"' in name:
            bad_names.append(name)
            
    print bad_names
    
    for n in bad_names:
        new_name = n.replace('"', '')
        query = "UPDATE parties SET name = '%s' WHERE name = '%s'" % (new_name, n)
        cursor.execute(query)
        
    cnx.commit()
    cursor.close()
    cnx.close()
    
def get_data():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    
    result = []
    result.append([])
    result[0].append('Day')
    
    big_5 = []
    cursor.execute('SELECT text, SUM(total) FROM hash_group GROUP BY text ORDER BY sum(total) DESC limit 5;')
    for r in cursor:
        big_5.append(r[0])
        
    days = []
    times = 1
    cursor.execute('SELECT DISTINCT(day) FROM hash_group ORDER BY day;')
    for r in cursor:
        days.append(r[0])
        result.append([])
        result[times].append(str(r[0]))
        times += 1

    
    
    for hashtag in big_5:
        result[0].append('#' +hashtag)
        tot = 1
        for day in days:
            
            cursor.execute("Select day,text,total from hash_group WHERE text='%s'AND day ='%s' GROUP BY day" % (hashtag, str(day)))
            has_data = False
            for r in cursor:
                print r
                result[tot].append(r[0][2])
                has_data = True
                
            if not has_data:
                result[tot].append(0)
                
            tot+=1

    
    return_dict = {
        'result': result,
    }
    print return_dict
    
    cursor.close()        
    cnx.close()
        

    
get_data()

print 'done'
        
        
