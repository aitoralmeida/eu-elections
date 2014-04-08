__author__ = 'juan'

import sqlite3 as lite

class database:

    def create(self):
        try:
            self.con = lite.connect("database.db")
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
