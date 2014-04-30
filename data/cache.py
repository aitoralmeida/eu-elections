# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 09:16:17 2014

@author: aitor
"""

import mysql.connector
import json


config = {
    'user': 'elections',
    'password': 'elections',
    'host': 'thor.deusto.es',
    'database': 'eu_test2',
}


def _create_locations_cache():
    print
    print 'CACHING LOCATIONS'
    print
    locs = {}
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()    
    query = "SELECT city, country_id FROM locations"
    cursor.execute(query)
    
    for result in cursor:
        city = result[0]
        country = result[1]
        locs[city] = country  
        
    cnx.close()
    
    json.dump(locs, open('./cache/locations.json', 'w'))
    
def _load_locations_cache():
    try:
        res =json.load(open('./cache/locations.json', 'r'))
    except:
        print 'Error loading groups'
        
    return res 
    
    
def _create_groups_cache():
    print
    print 'CACHING GROUPS'
    print
    gs = {}
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()    
    query = "SELECT initials, name, slug, candidate_id, subcandidate_id FROM groups"
    cursor.execute(query)
    
    for result in cursor:
        initials = result[0]
        name = result[1]
        slug = result[2]
        candidate_id = result[3]
        subcandidate_id = result[4]

        gs[initials] = {
                        'name': name,
                        'slug': slug,
                        'candidate_id': candidate_id,
                        'subcandidate_id' : subcandidate_id
        }  
        
    cnx.close()
    
    json.dump(gs, open('./cache/groups.json', 'w'))
    
def _load_groups_cache():
    try:
        res =json.load(open('./cache/groups.json', 'r'))
    except:
        print 'Error loading groups'
        
    return res   
    
def _create_parties_cache():
    print
    print 'CACHING PARTIES'
    print
    ps = {}
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()    
    query = "SELECT initials, name, location, group_id, user_id, slug FROM parties"
    cursor.execute(query)
    
    for result in cursor:
        initials = result[0]
        name = result[1]
        location = result[2]
        group_id = result[3]
        user_id = result[4]
        slug = result[5]
        
        ps[slug] = {
                        'initials': initials,
                        'name': name,
                        'location': location,
                        'group_id' : group_id,
                        'user_id' : user_id,
        }  
        
    cnx.close()
    
    json.dump(ps, open('./cache/parties.json', 'w'))
    
def _load_parties_cache():
    try:
        res =json.load(open('./cache/parties.json', 'r'))
    except:
        print 'Error loading groups'
        
    return res 
    
def _create_ids_cache():
    print
    print 'CACHING TWITTER IDS'
    print
    ids = {}
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()    
    query = "SELECT id, screen_name FROM twitter_users"
    cursor.execute(query)
    
    for result in cursor:
        twitter_id = result[0]
        screen_name = result[1]
       
        
        ids[twitter_id] = screen_name
        
    cnx.close()
    
    json.dump(ids, open('./cache/ids.json', 'w'))
    
def _load_ids_cache():
    try:
        res =json.load(open('./cache/ids.json', 'r'))
    except:
        print 'Error loading groups'
        
    return res     
    
    
def regenerate_cache():
    _create_locations_cache()
    _create_groups_cache()
    _create_parties_cache()
    _create_ids_cache()
    
regenerate_cache()

#******************CACHE VARIABLES*******************************    
    
locations = _load_locations_cache()
groups = _load_groups_cache()
parties = _load_parties_cache()
twitter_ids = _load_ids_cache()

