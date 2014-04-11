__author__ = 'juan'

import json
from termcolor import colored
import mysql.connector
import time

config = {
    'user': 'elec',
    'password': 'elec',
    'host': 'thor.deusto.es',
    'database': 'eu_test2',
}

class database:
    def __init__(self):
        self.con = mysql.connector.connect(**config)
        self.parties = []
        self.groups ={}
        self.twitter_users = {}             # Usuarios id : total_tweets
        self.twitter_users_mods = {}        # usuarios modificados id : total_tweets, screen_name
        self.interactions = {}
        self.language_group = {}
        self.language_candidate = {}
        self.hash_country = {}
        self.hash_group = {}
        self.hash_candidate = {}
        self.read()

    def read(self):
        try:
            self.con = mysql.connector.connect(**config)
            self.read_parties()
            self.read_groups()
            self.read_twitter_users()
            self.read_interactions()
            self.read_language_group()
            self.read_language_candidate()
            self.read_hash_country()
            self.read_hash_group()
            self.read_hash_candidate()
            self.con.commit()
            self.con.close()
        except Exception, e:
            print colored("Read error "+ e.message, "red")

    def insert(self, lines):
        for line in lines:
            tweet = json.loads(line)
            self.load_twitter_user(tweet)

        try:
            self.con = mysql.connector.connect(**config)
            self.write_twitter_users()
            self.con.commit()
            self.con.close()
        except Exception, e:
            print colored("Write error "+ e.message, "red")

        ##########################################################
        ##                  READ FUNCTIONS                      ##
        ##########################################################
    def read_parties(self):
        try:
            cursor = self.con.cursor()
            select = "SELECT user_id FROM parties;"
            cursor.execute(select)
            nodes = cursor.fetchall()
            for node in nodes:
                self.parties.append(node[0])
        except Exception, e:
            print "DB Error - read_parties: ", e.message

    def read_groups(self):
        try:
            cursor = self.con.cursor()
            select = "SELECT * FROM groups;"
            cursor.execute(select)
            nodes = cursor.fetchall()
            for node in nodes:
                self.groups[node[0]] = [node[0], node[4],node[5]]
        except Exception, e:
            print "DB Error - read_parties: ", e.message

    def read_twitter_users(self):
        try:
            cursor = self.con.cursor()
            select = "SELECT id, total_tweets FROM twitter_users;"
            cursor.execute(select)
            nodes = cursor.fetchall()
            for node in nodes:
                self.twitter_users[node[0]] = node[1]
        except Exception, e:
            print "DB Error - read_users: ", e.message

    def read_interactions(self):
        try:
            cursor = self.con.cursor()
            select = "SELECT * FROM interactions;"
            cursor.execute(select)
            nodes = cursor.fetchall()
            for node in nodes:
                self.interactions[(node[0], node[1], node[2])] = [node[3]]
        except Exception, e:
            print "DB Error - read_interactions: ", e.message

    def read_language_group(self):
        try:
            cursor = self.con.cursor()
            select = "SELECT * FROM language_group;"
            cursor.execute(select)
            nodes = cursor.fetchall()
            for node in nodes:
                self.language_group[(node[0], node[1])] = [node[2]]
        except Exception, e:
            print "DB Error - read_language_group: ", e.message

    def read_language_candidate(self):
        try:
            cursor = self.con.cursor()
            select = "SELECT * FROM language_candidate;"
            cursor.execute(select)
            nodes = cursor.fetchall()
            for node in nodes:
                self.language_candidate[(node[0], node[1])] = [node[2]]
        except Exception, e:
            print "DB Error - read_language_candidate: ", e.message

    def read_hash_country(self):
        try:
            cursor = self.con.cursor()
            select = "SELECT * FROM hash_country;"
            cursor.execute(select)
            nodes = cursor.fetchall()
            for node in nodes:
                self.hash_country[(node[0], node[1], node[2])] = [node[3]]
        except Exception, e:
            print "DB Error - read_hash_country: ", e.message

    def read_hash_group(self):
        try:
            cursor = self.con.cursor()
            select = "SELECT * FROM hash_group;"
            cursor.execute(select)
            nodes = cursor.fetchall()
            for node in nodes:
                self.hash_group[(node[0], node[1], node[2])] = [node[3]]
        except Exception, e:
            print "DB Error - read_hash_group: ", e.message

    def read_hash_candidate(self):
        try:
            cursor = self.con.cursor()
            select = "SELECT * FROM hash_candidate;"
            cursor.execute(select)
            nodes = cursor.fetchall()
            for node in nodes:
                self.hash_candidate[(node[0], node[1], node[2])] = [node[3]]
        except Exception, e:
            print "DB Error - read_hash_candidate: ", e.message

        ##########################################################
        ##                  LOAD FUNCTIONS                      ##
        ##########################################################

    def load_twitter_user(self,tweet):
        id = str(tweet['user']['id'])
        try:
            if id in self.twitter_users_mods.keys():
                self.twitter_users_mods[id][0] += 1
            elif id in self.twitter_users.keys():
                self.twitter_users_mods[id] = [(self.twitter_users[id]+1), tweet['user']['screen_name']]
            else:
                self.twitter_users_mods[id] = [1, tweet['user']['screen_name']]
        except Exception, e:
            print "Load User Exception: ", e.message , " tweet: ", tweet


        ##########################################################
        ##                  WRITE FUNCTIONS                     ##
        ##########################################################

    def write_twitter_users(self):
        #print self.twitter_users
        #print self.twitter_users_mods
        for id in self.twitter_users_mods:
            if str(id) in self.twitter_users.keys():
                try:
                    cursor = self.con.cursor()
                    update = "UPDATE twitter_users set total_tweets = "+str(self.twitter_users_mods[id][0])+" WHERE id = "+str(id)+" ;"
                    print update
                    cursor.execute(update)
                except Exception, e:
                    print "DB Error - write_user: ", e
            else:
                try:
                    cursor = self.con.cursor()
                    insert = "INSERT INTO twitter_users (id, total_tweets, screen_name) VALUES ("+str(id)+","+str(self.twitter_users_mods[id][0])+",'"+self.twitter_users_mods[id][1]+"');"
                    print insert
                    cursor.execute(insert)
                except Exception, e:
                    print "DB Error - update_user: ", e