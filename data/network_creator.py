# -*- coding: utf-8 -*-
"""
Created on Thu Apr 03 14:44:00 2014

@author: aitor
"""

import networkx as nx
import random
import json
from slugify import slugify
import mysql.connector

config = {
    'user': 'elections',
    'password': 'elections',
    'host': 'thor.deusto.es',
    'database': 'eu_test2',
}



def load_locations():
    locs = {}
    with open('./locations_reverse_geocoding/locations.csv', 'r') as infile:
        for line in infile:
            if line != "city,country,lat,lng":
                tokens = line.split(',')
                locs[tokens[0]] = (tokens[2], tokens[3]) #lat, long
                
    return locs
                
locations = load_locations()


def create_party_group_geo():
    groups = json.load(open('european_parliament_groups.json', 'r'))
    group_parties = {}
    for group in groups:
        group_parties[group] = []
    
    with open('Group_Party_Country.csv', 'r') as infile:
        for line in infile:       
            if 'Group in the EP' not in line:
                #GUE/NGL,AKEL,Nicosia, Cyprus
                tokens = line.split(',')
                if len(tokens) < 4:
                    continue
                
                current_group = tokens[0]
                group_name = groups[current_group]
                party = tokens[1]
                city = tokens[2]
                country = tokens[3]
                location = locations[city]
                
                

                group_parties[current_group].append({'party':party , 'data':{'group':current_group, 'group_name':group_name, 'city':city, 'country':country, 'lat':location[0], 'lon': location[1]}})

                    
    json.dump(group_parties, open('group_parties.json', 'w'), indent=4)
    

def build_party_group_geo():
    groups = json.load(open('group_parties.json', 'r'))
    G = nx.Graph()
    for i, group in enumerate(groups):
        parties = groups[group]
        party_list = []
        for party in parties:
            name = slugify.slugify(party['party'])
            party_list.append(name)
            lat = float(party['data']['lat'])
            lng = float(party['data']['lon'])
            lat, lng = scatter(lat, lng)             
            
            G.add_node(name, party_name = party['party'], group_id = i, group = group, group_name = party['data']['group_name'], city = party['data']['city'], lat = lat, lng = lng)
        
        for i in range(0, len(party_list)):
            for j in range(i+1, len(party_list)):
                G.add_edge(party_list[i], party_list[j])
                
    print 'Nodes:', len(G.nodes())
    print 'Edges:', len(G.edges())
    
    nx.write_gexf(G, './sna/party_group_geo.gexf')
    
def build_party_interaction():
    _, inverse_ids = get_party_ids()
    G = nx.DiGraph()
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()    
    query = "SELECT user_id, target_id, weight FROM interactions"
    cursor.execute(query)
    for relation in cursor:
        if relation[0] in inverse_ids.keys() and relation[1] in inverse_ids.keys():
            source = inverse_ids[relation[0]]
            target = inverse_ids[relation[1]]
            weight = relation[2]
            G.add_edge(source, target, weight = weight)
            
    cnx.close()
    
    print 'Nodes:', len(G.nodes())
    print 'Edges:', len(G.edges())
    
    nx.write_gexf(G, './sna/party_twitter.gexf')
    
def build_interaction():
    ids, inverse_ids = get_all_ids()
    G = nx.DiGraph()
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()    
    query = "SELECT user_id, target_id, weight FROM interactions"
    cursor.execute(query)
    for relation in cursor:
        source = inverse_ids[relation[0]]
        target = inverse_ids[relation[1]]
        weight = relation[2]
        G.add_edge(source, target, weight = weight)
            
    cnx.close()
    
    print 'Nodes:', len(G.nodes())
    print 'Edges:', len(G.edges())
    
    filter_weight(G, weight_limit = 3, degree_limit = 1)
    
    print 'Nodes:', len(G.nodes())
    print 'Edges:', len(G.edges())

    
    nx.write_gexf(G, './sna/interactions.gexf')
    
    
def get_all_ids():
    ids = {}
    inverse_ids = {}
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()    
    query = "SELECT id, screen_name FROM twitter_users"
    cursor.execute(query)
    for result in cursor:

        user_id = result[0]
        screen_name = result[1]
        ids[screen_name] = user_id
        inverse_ids[user_id] = screen_name
        
    cnx.close()
    
    return ids, inverse_ids 
                    
def get_party_ids():
    ids = {}
    inverse_ids = {}
    with open('twitter_ids.csv', 'r') as infile:
        for line in infile:
            screen_name, twitter_id = line.split(',')
            ids[screen_name] = twitter_id
            inverse_ids[twitter_id] = screen_name
            
    return ids, inverse_ids
    
def scatter(lat, lon):
    lat = lat + generate_variation()
    lon = lon + generate_variation() 
    return lat, lon
    
def generate_variation():
    variation = random.random()
    sign = random.random()
    if sign < 0.50:
        sign = -1
    else:
        sign = 1
    
    variation = variation * sign
    
    return variation
    
def filter_weight(G, weight_limit = 3, degree_limit = 1):
    
    removed = ['a']    
    
    while len(removed) > 0:
        removed = []
        for edge in G.edges(data=True):
            if edge[2]['weight'] <= weight_limit:
                G.remove_edge(edge[0], edge[1])
                
        degrees = G.degree()
        for node in degrees:
            if degrees[node] <= degree_limit:
                G.remove_node(node)
                removed.append(node)
            
build_interaction() 
print 'done'      
                
                
                
                
    
