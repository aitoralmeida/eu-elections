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
        self.parties = {}                   # Parties group_id : initials
        self.groups ={}                     # Grupos initials : initials , total_tweets, user_id
        self.groups_mods = {}
        self.twitter_users = {}             # Usuarios id : total_tweets
        self.twitter_users_mods = {}        # usuarios modificados id : total_tweets, screen_name
        self.tweets = {}                    # Tweets recibidos id : user_id, id_str, text, created_at, lang, retweeted
        self.interactions = {}
        self.language_group = {}
        self.language_group_mods = {}
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
            self.load_tweets(tweet)
            self.load_language_group(tweet)

        try:
            self.con = mysql.connector.connect(**config)
            self.write_twitter_users()
            self.write_tweets()
            self.write_groups()
            self.write_language_group()
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
            select = "SELECT user_id, group_id FROM parties;"
            cursor.execute(select)
            nodes = cursor.fetchall()
            for node in nodes:
                self.parties[node[0]] = node[1]
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

    def load_tweets(self,tweet):
        date = time.strftime('%Y-%m-%d', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
        self.tweets[str(tweet['id'])] = [tweet['user']['id'],str(tweet['user']['id']), tweet['text'], date, tweet['lang'], bool(tweet['retweeted'])]
        ##############################
        ### Load parties and groups ##
        ##############################
        if str(tweet['user']['id']) in self.parties.keys():
            initials = self.parties[str(tweet['user']['id'])]
            if initials in self.groups_mods.keys():
                self.groups_mods[initials][1] += 1
            else:
                group = self.groups[initials]
                self.groups_mods[initials] = [initials, group[1]+1, group[2]]

    def load_language_group(self,tweet):
        lang = tweet['lang']
        tid = str(tweet['user']['id'])
        if tid in self.parties.keys():
            initials =  self.parties[tid]
            if (lang,initials) in self.language_group:
                self.language_group_mods[(lang,initials)]  = self.language_group[(lang,initials)][0]+1
            else:
                self.language_group_mods[(lang,initials)]  = 1



        ##########################################################
        ##                  WRITE FUNCTIONS                     ##
        ##########################################################

    def write_twitter_users(self):
        for id in self.twitter_users_mods:
            if str(id) in self.twitter_users.keys():
                try:
                    cursor = self.con.cursor()
                    update = "UPDATE twitter_users set total_tweets = "+str(self.twitter_users_mods[id][0])+" WHERE id = "+str(id)+" ;"
                    cursor.execute(update)
                except Exception, e:
                    print "DB Error - write_user: ", e
            else:
                try:
                    cursor = self.con.cursor()
                    insert = "INSERT INTO twitter_users (id, total_tweets, screen_name) VALUES ("+str(id)+","+str(self.twitter_users_mods[id][0])+",'"+self.twitter_users_mods[id][1]+"');"
                    cursor.execute(insert)
                except Exception, e:
                    print "DB Error - update_user: ", e

    def write_tweets(self):
        for tid in self.tweets:
            try:
                tweet =  self.tweets[tid]
                cursor = self.con.cursor()
                insert = "INSERT INTO tweets (id, user_id, id_str, text, created_at, lang, retweeted) VALUES ('"+str(tid)+"','"+str(tweet[0])+"','"+str(tweet[1])+"','"+tweet[2].replace("\'","")+"',"+tweet[3]+",'"+tweet[4]+"',"+str(tweet[5])+");"
                cursor.execute(insert)
            except Exception, e:
                    #print "DB Error - write_tweets: ", e
                    pass

    def write_groups(self):
        for g in self.groups_mods:
            if str(g) in self.groups.keys():
                try:
                    cursor = self.con.cursor()
                    update = "UPDATE groups set total_tweets = "+str(self.groups_mods[g][1])+" WHERE initials = '"+str(g)+"' ;"
                    cursor.execute(update)
                except Exception, e:
                    print "DB Error - write_groups: ", e
            else:
                try:
                    cursor = self.con.cursor()
                    insert = "INSERT into groups (initials, total_tweets, user_id) VALUES ('"+str(g)+"',"+str(self.groups_mods[g][1])+",'"+str(self.groups_mods[g][2])+"');"
                    cursor.execute(insert)
                except Exception, e:
                    print "DB Error - write_groups: ", e

    def write_language_group(self):
        for l in self.language_group_mods:
            if l in self.language_group.keys():
                try:
                    cursor = self.con.cursor()
                    update = "UPDATE language_group set total = "+str(self.language_group_mods[l])+" WHERE lang = '"+str(l[0])+"' AND group_id = '"+str(l[1])+"' ;"
                    cursor.execute(update)
                except Exception, e:
                    print "DB Error - write_language_groups: ", e
            else:
                try:
                    cursor = self.con.cursor()
                    insert = "INSERT into language_group (lang, group_id, total) VALUES ('"+str(l[0])+"','"+str(l[1])+"',"+str(self.language_group_mods[l])+");"
                    cursor.execute(insert)
                except Exception, e:
                    print "DB Error - write_language_groups: ", e