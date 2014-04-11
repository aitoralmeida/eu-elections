# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Countries(models.Model):
    short_name = models.CharField(primary_key=True, max_length=50)
    long_name = models.CharField(max_length=200, blank=True)
    total = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'countries'

class Groups(models.Model):
    initials = models.CharField(primary_key=True, max_length=20)
    candidate_id = models.IntegerField()
    subcandidate_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=200)
    total_tweets = models.IntegerField(blank=True, null=True)
    user_id = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'groups'

class HashCandidate(models.Model):
    text = models.CharField(max_length=200)
    candidate_id = models.IntegerField()
    day = models.DateField()
    total = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'hash_candidate'

class HashCountry(models.Model):
    text = models.CharField(max_length=200)
    country_id = models.CharField(max_length=50)
    day = models.DateField()
    total = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'hash_country'

class HashGroup(models.Model):
    text = models.CharField(max_length=200)
    group_id = models.CharField(max_length=50)
    day = models.DateField()
    total = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'hash_group'

class Interactions(models.Model):
    user_id = models.CharField(max_length=100)
    day = models.DateField()
    weight = models.IntegerField()
    target_id = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'interactions'

class LanguageCandidate(models.Model):
    lang = models.CharField(max_length=100)
    total = models.IntegerField(blank=True, null=True)
    candidate_id = models.CharField(max_length=200)
    class Meta:
        managed = False
        db_table = 'language_candidate'

class LanguageGroup(models.Model):
    lang = models.CharField(max_length=100)
    group_id = models.CharField(max_length=50)
    total = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'language_group'

class Locations(models.Model):
    city = models.CharField(primary_key=True, max_length=100)
    lat = models.IntegerField()
    lon = models.IntegerField()
    country_id = models.CharField(max_length=50)
    class Meta:
        managed = False
        db_table = 'locations'

class Parties(models.Model):
    initials = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    group_id = models.CharField(max_length=50)
    name = models.CharField(max_length=200, blank=True)
    is_group_party = models.IntegerField(blank=True, null=True)
    user_id = models.CharField(max_length=100, blank=True)
    class Meta:
        managed = False
        db_table = 'parties'

class Tweets(models.Model):
    user_id = models.CharField(max_length=100)
    id_str = models.CharField(max_length=100, blank=True)
    text = models.CharField(max_length=200, blank=True)
    created_at = models.DateField()
    lang = models.CharField(max_length=50)
    retweeted = models.IntegerField(blank=True, null=True)
    id = models.CharField(primary_key=True, max_length=200)
    class Meta:
        managed = False
        db_table = 'tweets'

class Users(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    screen_name = models.CharField(max_length=100)
    total_tweets = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'users'

