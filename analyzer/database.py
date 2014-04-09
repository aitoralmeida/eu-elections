__author__ = 'juan'

import sqlite3 as lite
import json
from termcolor import colored

class database:
    def __init__(self, db):
        self.db = db

    def create(self):
        try:
            self.con = lite.connect(self.db)
            with self.con:
                cursor = self.con.cursor()
                comm = "CREATE TABLE users (id INT, id_str TEXT, screen_name TEXT, total_tweets INT);"
                cursor.execute(comm)
                comm = "CREATE TABLE tweets (id INT, user_id INT, id_str  TEXT ,text  TEXT, created_at  TEXT, lang  TEXT, retweeted  BOOL);"
                cursor.execute(comm)
                comm = "CREATE TABLE interactions (user_id INT, target_id INT, day DATE, weight INT);"
                cursor.execute(comm)
                comm = "CREATE TABLE language_group (lang TEXT, group_id TEXT, total INT);"
                cursor.execute(comm)
                comm = "CREATE TABLE language_candidate (lang TEXT, candidate_id INT, total INT);"
                cursor.execute(comm)
                comm = "CREATE TABLE hash_country (text TEXT, country_id TEXT, day DATE, total INT);"
                cursor.execute(comm)
                comm = "CREATE TABLE hash_group (text TEXT, group_id TEXT, day DATE, total INT);"
                cursor.execute(comm)
                comm = "CREATE TABLE hash_candidate (text TEXT, candidate_id INT, day DATE, total INT);"
                cursor.execute(comm)
                comm = "CREATE TABLE parties (initials TEXT, location_id TEXT, group_id TEXT, name TEXT, is_group_party BOOL, user_id INT);"
                cursor.execute(comm)
                comm = "CREATE TABLE groups (candidate_id INT, initials TEXT, subcandidate_id INT, name TEXT, total_tweets INT, user_id INT);"
                cursor.execute(comm)
                comm = "CREATE TABLE locations (city TEXT, lat INT, lon INT, country_id TEXT);"
                cursor.execute(comm)
                comm = "CREATE TABLE countries (short_name TEXT, long_name TEXT, total INT);"
                cursor.execute(comm)

        except Exception, e:
             print "DB Error", e

    def insert(self,tweet):
        try:
            tweet = json.loads(tweet)
            self.insert_users(tweet)
            self.insert_tweets(tweet)
            self.insert_interacions(tweet)
            self.insert_language_group(tweet)
            self.insert_hash_country(tweet)
            self.insert_hash_group(tweet)
            self.insert_hash_candidate(tweet)
            self.insert_parties(tweet)
            self.insert_groups(tweet)
            self.insert_locations(tweet)
            self.insert_countries(tweet)
        except Exception, e:
            print colored("Insertion error "+ e.message, "red")
            print tweet
            print "__________"

    def insert_users(self,tweet):
        #id INT, id_str TEXT, screen_name TEXT, total_tweets INT
        keys = [tweet['user']['id'], tweet['user']['id_str'], tweet['user']['screen_name'],1]
        try:
            self.con = lite.connect(self.db)
            with self.con:
                cursor = self.con.cursor()
                cursor.execute("SELECT id, total_tweets from users where id='"+str(tweet['user']['id'])+"'")
                node = cursor.fetchone()
                if node:
                    total = node[1]+1
                    cursor.execute("UPDATE users set total_tweets = "+str(total)+" where id = "+str(node[0]))
                else:
                    cursor.execute("INSERT INTO users VALUES (?,?,?,?)",keys)
            self.con.close()
        except Exception, e:
            print "DB Error", e


    def insert_tweets(self,tweet):

    def insert_interacions(self,tweet):
        pass

    def insert_language_group(self,tweet):
        pass

    def insert_hash_country(self,tweet):
        pass

    def insert_hash_group(self,tweet):
        pass

    def insert_hash_candidate(self,tweet):
        pass

    def insert_parties(self,tweet):
        pass

    def insert_groups(self,tweet):
        pass

    def insert_locations(self,tweet):
        pass

    def insert_countries(self,tweet):
        pass

