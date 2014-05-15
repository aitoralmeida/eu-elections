# -*- coding: utf-8 -*-
"""
Created on Thu May 15 14:51:05 2014

@author: aitor
"""

import mysql.connector

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
    
get_candidate_data()

print 'done'