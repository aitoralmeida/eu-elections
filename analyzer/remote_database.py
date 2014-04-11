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


    def insert(self,tweet):
        try:
            self.con = mysql.connector.connect(**config)
            tweet = json.loads(tweet)
            self.insert_users(tweet)
            #self.insert_tweets(tweet)
            self.insert_mention(tweet)
            #self.insert_language_group(tweet)
            #self.insert_language_candidate(tweet)
            #self.insert_hash_country(tweet)
            #self.insert_hash_group(tweet)
            #self.insert_hash_candidate(tweet)
            self.con.commit()
            self.con.close()

        except Exception, e:
            print colored("Insertion error "+ e.message, "red")


    def insert_users(self,tweet):
        #id TEXT, screen_name TEXT, total_tweets INT
        keys = [tweet['user']['id'], tweet['user']['screen_name'],1]
        try:
            cursor = self.con.cursor()
            select = "SELECT id, total_tweets from twitter_users where id="+str(keys[0])
            cursor.execute(select)
            node = cursor.fetchone()
            if node:
                total = node[1]+1
                update = "UPDATE twitter_users set total_tweets = "+str(total)+" where id = "+str(keys[0])
                cursor.execute(update)
            else:
                insert = "INSERT INTO twitter_users(id, screen_name, total_tweets) VALUES (" + str(keys[0]) + ",'" + keys[1] + "', 1)"
                cursor.execute(insert)
        except Exception, e:
            print "DB Error - insert_user: ", e

    def insert_tweets(self,tweet):
        # id TEXT, user_id TEXT, text  TEXT, created_at  DATE, lang  TEXT, retweeted  BOOL
        date=  time.strftime('%Y-%m-%d', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
        keys = [tweet['id'], tweet['user']['id'], tweet['text'], date, tweet['lang'], tweet['retweeted']]
        try:
            cursor = self.con.cursor()
            insert = "INSERT INTO tweets(id, user_id, id_str, text, created_at, lang, retweeted) VALUES ('"+str(keys[0])+"','"+str(keys[1])+"','"+str(keys[0])+"','"+keys[2]+"','"+keys[3]+"','"+keys[4]+"','"+str(bool(keys[5]))+"')"
            cursor.execute(insert)
        except Exception, e:
            print "DB Error - insert_tweet: ", e

    def insert_mention(self,tweet):
        #user_id INT, target_id INT, day DATE, weight INT
        replies = tweet['in_reply_to_user_id']
        replies_screen_name = tweet['in_reply_to_screen_name']
        date=  time.strftime('%Y-%m-%d', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
        if replies:
            keys = [tweet['user']['id'], replies, date, 1]
            try:
                    cursor = self.con.cursor()
                    cursor.execute("SELECT * from interactions where (user_id = '"+str(tweet['user']['id'])+"' AND target_id = '"+str(replies)+"' AND day = '"+str(date)+"')")
                    node = cursor.fetchone()
                    if node:
                        total = node[3]+1
                        cursor.execute("UPDATE interactions set weight = '"+str(total)+"' WHERE (user_id = '"+str(tweet['user']['id'])+"' AND target_id = '"+str(replies)+"' AND day = '"+str(date)+"')")
                    else:
                        insert = "INSERT INTO interactions(user_id, target_id, day, weight) VALUES ('"+str(keys[0])+"','"+str(keys[1])+"','"+str(keys[2])+"','"+str(keys[3])+"') "
                        cursor.execute(insert)
            except Exception, e:
                print "DB Error - insert_mention: ", e

            try:
                cursor = self.con.cursor()                        ################
                select = "SELECT id from twitter_users WHERE id="+str(replies)+";"
                print select
                cursor.execute(select)
                node = cursor.fetchone()
                if node:
                    print node
                else:
                    insert = "INSERT INTO twitter_users(id, screen_name, total_tweets) VALUES (" + str(replies) + ",'" + replies_screen_name + "', 1)"
                    cursor.execute(insert)
                    print "added"
                    ################
            except Exception, e:
                print "DB Error - insert_mentionAA: ", e


    def insert_language_group(self,tweet):
        #lang TEXT, group_id TEXT, total INT
        keys = [tweet['lang'], "ALDE", 1]
        try:
                cursor = self.con.cursor()
                cursor.execute("SELECT total from language_group WHERE ( lang='"+tweet['lang']+"' AND group_id ='"+"ALDE"+"')")
                node = cursor.fetchone()
                if node:
                    total = node[0]+1
                    cursor.execute("UPDATE language_group set total = "+str(total)+" WHERE  ( lang='"+tweet['lang']+"' AND group_id ='"+"ALDE"+"')")
                else:
                    cursor.execute("INSERT INTO language_group(lang,group_id,total) VALUES ('"+keys[0]+"','"+keys[1]+"','"+str(keys[2])+"')")
        except Exception, e:
            print "DB Error - language_group: ", e

    def insert_language_candidate(self,tweet):
        #lang TEXT, candidate_id INT, total INT
        keys = [tweet['lang'], 44101578, 1]
        try:
                cursor = self.con.cursor()
                cursor.execute("SELECT total from language_candidate WHERE ( lang='"+tweet['lang']+"' AND candidate_id ='"+str(44101578)+"')")
                node = cursor.fetchone()
                if node:
                    total = node[0]+1
                    cursor.execute("UPDATE language_candidate set total = "+str(total)+" WHERE  ( lang='"+tweet['lang']+"' AND candidate_id ='"+str(44101578)+"')")
                else:
                    cursor.execute("INSERT INTO language_candidate(lang,candidate_id,total) VALUES ('"+keys[0]+"','"+str(keys[1])+"','"+str(keys[2])+"')")
        except Exception, e:
            print "DB Error - language_candidate: ", e

    def insert_hash_country(self,tweet):
        #text TEXT, country_id TEXT, day DATE, total INT
        hashtags = tweet['entities']['hashtags']
        date=  time.strftime('%Y-%m-%d', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
        for h in hashtags:
            hashtag = h['text']
            keys = [hashtag, tweet['lang'], date, 1]
            try:
                    cursor = self.con.cursor()
                    cursor.execute("SELECT text, total from hash_country WHERE ( text='"+hashtag+"' AND country_id = '"+tweet['lang']+"' AND day = '"+str(date)+"')")
                    node = cursor.fetchone()
                    if node:
                        total = node[1]+1
                        cursor.execute("UPDATE hash_country set total = "+str(total)+"  WHERE ( text='"+hashtag+"' AND country_id = '"+tweet['lang']+"' AND day = '"+str(date)+"')")
                    else:
                        insert = "INSERT INTO hash_country(text, country_id, day, total) VALUES ('"+hashtag+"','"+tweet['lang']+"','"+str(date)+"','"+str(1)+"' )"
                        cursor.execute(insert)
            except Exception, e:
                print "DB Error - insert_hash_country: ", e

    def insert_hash_group(self,tweet):
        #text TEXT, group_id TEXT, day DATE, total INT
        hashtags = tweet['entities']['hashtags']
        date=  time.strftime('%Y-%m-%d', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
        for h in hashtags:
            hashtag = h['text']
            try:
                    cursor = self.con.cursor()
                    cursor.execute("SELECT text, total from hash_group WHERE ( text='"+hashtag+"' AND group_id = 'ALDE' AND day = '"+str(date)+"')")
                    node = cursor.fetchone()
                    if node:
                        total = node[1]+1
                        cursor.execute("UPDATE hash_group set total = "+str(total)+"  WHERE ( text='"+hashtag+"' AND group_id = 'ALDE' AND day = '"+str(date)+"')")
                    else:
                        insert = "INSERT INTO hash_group(text, group_id, day, total) VALUES ('"+hashtag+"','"+"ALDE"+"','"+str(date)+"','"+str(1)+"' )"
                        cursor.execute(insert)
            except Exception, e:
                print "DB Error - insert_hash_group: ", e

    def insert_hash_candidate(self,tweet):
        #text TEXT, candidate_id INT, day DATE, total INT
        hashtags = tweet['entities']['hashtags']
        date=  time.strftime('%Y-%m-%d', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
        for h in hashtags:
            hashtag = h['text']
            try:
                    cursor = self.con.cursor()
                    cursor.execute("SELECT text, total from hash_candidate WHERE ( text='"+hashtag+"' AND candidate_id = "+str(44101578)+" AND day = '"+str(date)+"')")
                    node = cursor.fetchone()
                    if node:
                        total = node[1]+1
                        cursor.execute("UPDATE hash_candidate set total = "+str(total)+"  WHERE ( text='"+hashtag+"' AND candidate_id = "+str(44101578)+" AND day = '"+str(date)+"')")
                    else:
                        insert = "INSERT INTO hash_candidate(text, candidate_id, day, total) VALUES ('"+hashtag+"','"+str(44101578)+"','"+str(date)+"','"+str(1)+"' )"
                        cursor.execute(insert)
            except Exception, e:
                print "DB Error - insert_hash_group: ", e
