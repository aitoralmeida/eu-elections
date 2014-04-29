__author__ = 'juan'
# -*- coding: utf-8 -*-

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
        self.parties = {}                   # Parties user_id : group_id
        self.parties_by_location = {}       # Parties user_id : location_id
        self.locations = {}                 # city : country_id
        self.groups ={}                     # Grupos initials : initials , total_tweets, user_id
        self.candidates = {}                # candidate : initials
        self.groups_mods = {}
        self.twitter_users = {}             # Usuarios id : total_tweets
        self.twitter_users_mods = {}        # usuarios modificados id : total_tweets, screen_name
        self.tweets = {}                    # Tweets recibidos id : user_id, id_str, text, created_at, lang, retweeted
        self.interactions = {}
        self.interactions_mod = {}
        self.language_group = {}
        self.language_group_mods = {}
        self.language_candidate = {}        # lang, candidate_id : total
        self.language_candidate_mods = {}
        self.language_country = {}
        self.language_country_mods = {}
        self.hash_country = {}
        self.hash_country_mods = {}
        self.hash_group = {}
        self.hash_group_mods = {}
        self.hash_candidate = {}
        self.hash_candidate_mods = {}
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
            self.read_language_country()
            self.read_hash_country()
            self.read_hash_group()
            self.read_hash_candidate()
            self.read_locations()
            self.con.commit()
            self.con.close()
        except Exception, e:
            print colored("Read error "+ e.message, "red")

    def insert(self, lines):
        for line in lines:
            tweet = json.loads(line)
            if 'user' in tweet:
                self.load_twitter_user(tweet)
                self.load_tweets(tweet)
                self.load_language_group(tweet)
                self.load_language_candidate(tweet)
                self.load_language_country(tweet)
                hashtags = tweet['entities']['hashtags']
                if hashtags:
                    for h in hashtags:
                        self.load_hash_country(h,tweet['created_at'],tweet['user']['id'])
                        self.load_hash_group(h,tweet['created_at'], tweet['user']['id'])
                        self.load_hash_candidate(h,tweet['created_at'], tweet['user']['id'])

                mentions = tweet['entities']['user_mentions']
                for m in mentions:
                    self.load_interaction(tweet['user']['id'],m['id'], m['screen_name'], tweet['created_at'])
                if 'retweeted_status' in tweet:
                    retweets = tweet['retweeted_status']
                    self.load_interaction(tweet['user']['id'],retweets['user']['id'],retweets['user']['screen_name'],tweet['created_at'])
                reply_id = tweet['in_reply_to_user_id']
                reply_screen_name = tweet['in_reply_to_screen_name']
                if reply_id != None:
                    self.load_interaction(tweet['user']['id'],reply_id, reply_screen_name,tweet['created_at'])

        try:
            self.con = mysql.connector.connect(**config)
            self.write_twitter_users()
            self.write_tweets()
            self.write_groups()
            self.write_language_group()
            self.write_language_candidate()
            self.write_language_country()
            self.write_hash_country()
            self.write_hash_group()
            self.write_hash_candidate()
            self.write_interactions()
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
            select = "SELECT user_id, group_id, location FROM parties;"
            cursor.execute(select)
            nodes = cursor.fetchall()
            for node in nodes:
                self.parties[node[0]] = node[1]
                self.parties_by_location[node[0]] = node[2]
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
                self.candidates[node[1]] = node[0]
                if node[2] > 0:
                    self.candidates[node[2]] = node[0]
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
                self.interactions[(node[0], node[1],str(node[2]))] = [node[3]]
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

    def read_language_country(self):
        try:
            cursor = self.con.cursor()
            select = "SELECT * FROM language_country;"
            cursor.execute(select)
            nodes = cursor.fetchall()
            for node in nodes:
                self.language_country[(node[0], node[1])] = [node[2]]
        except Exception, e:
            print "DB Error - read_language_country: ", e.message

    def read_language_candidate(self):
        try:
            cursor = self.con.cursor()
            select = "SELECT * FROM language_candidate;"
            cursor.execute(select)
            nodes = cursor.fetchall()
            for node in nodes:
                self.language_candidate[(node[0], node[1].encode('utf-8'))] = [node[2]]
        except Exception, e:
            print "DB Error - read_language_candidate: ", e.message

    def read_hash_country(self):
        try:
            cursor = self.con.cursor()
            select = "SELECT * FROM hash_country;"
            cursor.execute(select)
            nodes = cursor.fetchall()
            for node in nodes:
                self.hash_country[(node[0], node[1], str(node[2]))] = [node[3]]
        except Exception, e:
            print "DB Error - read_hash_country: ", e.message

    def read_hash_group(self):
        try:
            cursor = self.con.cursor()
            select = "SELECT * FROM hash_group;"
            cursor.execute(select)
            nodes = cursor.fetchall()
            for node in nodes:
                self.hash_group[(node[0], node[1], str(node[2]))] = [node[3]]
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

    def read_locations(self):
        try:
            cursor = self.con.cursor()
            select = "SELECT city, country_id FROM locations;"
            cursor.execute(select)
            nodes = cursor.fetchall()
            for node in nodes:
                self.locations[node[0]] = node[1]
        except Exception, e:
            print "DB Error - read_locations: ", e.message



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
        try:
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
        except:
            pass

    def load_language_group(self,tweet):
        lang = tweet['lang']
        tid = str(tweet['user']['id'])
        if tid in self.parties.keys():
            initials =  self.parties[tid]
            if (lang,initials) in self.language_group_mods:
                self.language_group_mods[(lang,initials)] += 1
            elif (lang,initials) in self.language_group:
                self.language_group_mods[(lang,initials)]  = self.language_group[(lang,initials)][0]+1
            else:
                self.language_group_mods[(lang,initials)]  = 1

    def load_language_candidate(self,tweet):
        lang = tweet['lang']
        tid = str(tweet['user']['id'])
        key = (lang,str(tid))
        if tid in self.parties.keys():
            if key in self.language_candidate_mods:
                self.language_candidate_mods[key] += 1
            elif key in self.language_candidate:
                self.language_candidate_mods[key] = self.language_candidate[key][0]+1
            else:
                self.language_candidate_mods[key] = 1

    def load_language_country(self,tweet):
        if str(tweet['user']['id']) in self.parties.keys():
            lang = tweet['lang']
            country_id = self.parties_by_location[str(tweet['user']['id'])]
            tid = str(tweet['user']['id'])
            key = (lang,str(country_id))
            if tid in self.parties.keys():
                if key in self.language_country_mods:
                    self.language_country_mods[key] += 1
                elif key in self.language_country:
                    self.language_country_mods[key] = self.language_country[key][0]+1
                else:
                    self.language_country_mods[key] = 1

    def load_hash_country(self,hashtag, created_at, user_id):
        if str(user_id) in self.parties.keys():
            country_id = self.parties_by_location[str(user_id)]
            if country_id != "none":
                location = self.locations[country_id]
                text = hashtag['text'].lower()
                date=  time.strftime('%Y-%m-%d', time.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y'))
                key = (text, location, date)
                if key in self.hash_country_mods:
                    self.hash_country_mods[key] += 1
                elif key in self.hash_country:
                    self.hash_country_mods[key] = self.hash_country[key][0]+1
                else:
                    self.hash_country_mods[key] = 1

    def load_hash_group(self,hashtag, created_at, user_id):
         if str(user_id) in self.parties.keys():
            group_id = self.parties[str(user_id)]
            text = hashtag['text'].lower()
            date=  time.strftime('%Y-%m-%d', time.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y'))
            key = (text, group_id, date)
            if key in self.hash_group_mods:
                self.hash_group_mods[key] += 1
            elif key in self.hash_group:
                self.hash_group_mods[key] = self.hash_group[key][0]+1
            else:
                self.hash_group_mods[key] = 1

    def load_hash_candidate(self,hashtag, created_at, candidate_id):
        if str(candidate_id) in self.candidates:
            id = str(candidate_id)
            text = hashtag['text'].lower()
            date=  time.strftime('%Y-%m-%d', time.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y'))
            key = (text, id, date)
            if key in self.hash_candidate_mods:
                self.hash_candidate_mods[key] += 1
            elif key in self.hash_candidate:
                self.hash_candidate_mods[key] = self.hash_candidate[key][0]+1
            else:
                self.hash_candidate_mods[key] = 1

    def load_interaction(self,user_id, target_id, target_screen_name, created_at):
        date=  time.strftime('%Y-%m-%d', time.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y'))
        key = (str(user_id), str(target_id), date)
        ##################### Check User #######################################
        if target_id not in self.twitter_users.keys():
            if target_id not in self.twitter_users_mods.keys():
                self.twitter_users_mods[target_id] = (0, target_screen_name)
        if key in self.interactions_mod:
            self.interactions_mod[key] += 1
        elif key in self.interactions:
            self.interactions_mod[key] = self.interactions[key][0]+1
        else:
            self.interactions_mod[key] = 1


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

    def write_language_candidate(self):
        for l in self.language_candidate_mods:
            if l in self.language_candidate.keys():
                try:
                    cursor = self.con.cursor()
                    update = "UPDATE language_candidate set total = "+str(self.language_candidate_mods[l])+" WHERE lang = '"+str(l[0])+"' AND candidate_id = '"+str(l[1])+"';"
                    cursor.execute(update)
                except Exception, e:
                    print "DB Error - write_language_candidate: ", e
            else:
                try:
                    cursor = self.con.cursor()
                    insert = "INSERT into language_candidate (lang, candidate_id, total) VALUES ('"+str(l[0])+"','"+str(l[1])+"',"+str(self.language_candidate_mods[l])+");"
                    cursor.execute(insert)
                except Exception, e:
                    print "DB Error - write_language_candidate: ", e

    def write_language_country(self):
        for l in self.language_country_mods:
            if l in self.language_country.keys():
                try:
                    cursor = self.con.cursor()
                    update = "UPDATE language_country set total = "+str(self.language_country_mods[l])+" WHERE lang = '"+str(l[0])+"' AND country_name = '"+str(l[1])+"';"
                    cursor.execute(update)
                except Exception, e:
                    print "DB Error - write_language_country: ", e
            else:
                try:
                    cursor = self.con.cursor()
                    insert = "INSERT into language_country (lang, country_name, total) VALUES ('"+str(l[0])+"','"+str(l[1])+"',"+str(self.language_country_mods[l])+");"
                    cursor.execute(insert)
                except Exception, e:
                    print "DB Error - write_language_country: ", e

    def write_hash_country(self):
        for l in self.hash_country_mods:
            if l in self.hash_country.keys():
                try:
                    cursor = self.con.cursor()
                    #update = "UPDATE hash_country set total = "+str(self.hash_country_mods[l])+" WHERE text = '"+l[0]+"' AND country_id = '"+str(l[1])+"' AND day = '"+l[2]+"';"
                    cursor.execute("UPDATE hash_country set total = "+str(self.hash_country_mods[l])+" WHERE text = %s AND country_id = %s AND day = %s;",(l[0],l[1],l[2]))
                except Exception, e:
                    print "DB Error - write_hash_country: ", e
            else:
                try:
                    cursor = self.con.cursor()
                    #insert = "INSERT into hash_country (text, country_id, day,  total) VALUES ('"+l[0]+"','"+str(l[1])+"','"+l[2]+"',"+str(self.hash_country_mods[l])+");"
                    cursor.execute("INSERT into hash_country (text, country_id, day,  total) VALUES (%s, %s, %s, %s)", (l[0], l[1], l[2], str(self.hash_country_mods[l])))
                except Exception, e:
                    print "DB Error - write_hash_country: ", e

    def write_hash_group(self):
        for l in self.hash_group_mods:
            if l in self.hash_group.keys():
                try:
                    cursor = self.con.cursor()
                    #update = "UPDATE hash_country set total = "+str(self.hash_country_mods[l])+" WHERE text = '"+l[0]+"' AND country_id = '"+str(l[1])+"' AND day = '"+l[2]+"';"
                    cursor.execute("UPDATE hash_group set total = "+str(self.hash_group_mods[l])+" WHERE text = %s AND group_id = %s AND day = %s;",(l[0].encode('utf-8'),l[1],l[2]))
                except Exception, e:
                    print "DB Error - write_hash_group: ", e
            else:
                try:
                    cursor = self.con.cursor()
                    #insert = "INSERT into hash_country (text, country_id, day,  total) VALUES ('"+l[0]+"','"+str(l[1])+"','"+l[2]+"',"+str(self.hash_country_mods[l])+");"
                    cursor.execute("INSERT into hash_group (text, group_id, day,  total) VALUES (%s, %s, %s, %s)", (l[0], l[1], l[2], str(self.hash_group_mods[l])))
                except Exception, e:
                    print "DB Error - write_hash_group: ", e

    def write_hash_candidate(self):
        for l in self.hash_candidate_mods:
            if l in self.hash_candidate.keys():
                try:
                    cursor = self.con.cursor()
                    #update = "UPDATE hash_country set total = "+str(self.hash_country_mods[l])+" WHERE text = '"+l[0]+"' AND country_id = '"+str(l[1])+"' AND day = '"+l[2]+"';"
                    cursor.execute("UPDATE hash_candidate set total = "+str(self.hash_candidate_mods[l])+" WHERE text = %s AND candidate_id = %s AND day = %s;",(l[0],l[1],l[2]))
                except Exception, e:
                    print "DB Error - write_hash_candidate: ", e
            else:
                try:
                    cursor = self.con.cursor()
                    #insert = "INSERT into hash_country (text, country_id, day,  total) VALUES ('"+l[0]+"','"+str(l[1])+"','"+l[2]+"',"+str(self.hash_country_mods[l])+");"
                    cursor.execute("INSERT into hash_candidate (text, candidate_id, day,  total) VALUES (%s, %s, %s, %s)", (l[0], l[1], l[2], str(self.hash_candidate_mods[l])))
                except Exception, e:
                    print "DB Error - write_hash_candidate: ", e

    def write_interactions(self):
        for l in self.interactions_mod:
            if l in self.interactions.keys():
                try:
                    cursor = self.con.cursor()
                    update = "UPDATE interactions set weight = "+str(self.interactions_mod[l])+" WHERE ( user_id = '"+str(l[0])+"' AND target_id = '"+str(l[1])+"' AND day = '"+(l[2])+"');"
                    cursor.execute(update)
                except Exception, e:
                    print "DB Error - write_interactions: ", e
            else:
                try:
                    cursor = self.con.cursor()
                    insert = "INSERT into interactions (user_id, target_id, day, weight) VALUES ('"+str(l[0])+"','"+str(l[1])+"','"+str(l[2])+"',"+str(self.interactions_mod[l])+");"
                    cursor.execute(insert)
                except Exception, e:
                    print "DB Error - write_interactions: ", e