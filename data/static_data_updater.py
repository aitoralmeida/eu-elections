# -*- coding: utf-8 -*-
"""
Created on Wed Apr 09 10:35:28 2014

@author: aitor
"""

from slugify import slugify
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
    
load_locations()
        
        
