# -*- coding: utf-8 -*-
"""
Created on Thu Apr 03 14:44:00 2014

@author: aitor
"""

import networkx as nx

import json



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
            name = party['party']
            party_list.append(name)
            G.add_node(name, group_id = i, group = group, group_name = party['data']['group_name'], city = party['data']['city'], lat = float(party['data']['lat']), lng = float(party['data']['lon']))
        
        for i in range(0, len(party_list)):
            for j in range(i+1, len(party_list)):
                G.add_edge(party_list[i], party_list[j])
                
    print 'Nodes:', len(G.nodes())
    print 'Edges:', len(G.edges())
    
    nx.write_gexf(G, './sna/party_group_geo.gexf')
    
            
            
                    
build_party_group_geo()   
          
                
                
                
                
    
