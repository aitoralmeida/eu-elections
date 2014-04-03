#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import timeit
import requests
import csv

EUROPEAN_PARLIAMENT_GROUPS = ['GUE/NGL', 'S&D', 'ALDE', 'Greens', 'EPP', 'ECR', 'EFD', 'EAF']
COUNTRIES = ['Austria', 'Belgium', 'Bulgaria', 'Country', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'England', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Northern Ireland', 'Poland', 'Portugal', 'Romania', 'Scotland', 'Slovak Republic', 'Slovenia', 'Spain', 'Sweden', 'UK', 'Wales']

if __name__ == "__main__":

    start = timeit.default_timer()

    group_party_city_country_file = open('Group_Party_City_Country.csv', 'rb')
    csv_reader = csv.reader(group_party_city_country_file, delimiter=',')

    groups_per_country_count_file = open('group_representation_per_country/counts.csv', 'w')
    csv_writer = csv.writer(groups_per_country_count_file, delimiter=',')

    csv_header = []

    csv_header.append('Country')
    for party in EUROPEAN_PARLIAMENT_GROUPS:
        csv_header.append(party)

    csv_writer.writerow(csv_header)

    count = {}

    for country in COUNTRIES:
        count[country] = {}
        for group in EUROPEAN_PARLIAMENT_GROUPS:
            count[str(country)][str(group)] = 0

    next(csv_reader, None)

    for row in csv_reader:
        group = row[0]
        country = row[3]
        count[str(country)][str(group)] = count[str(country)][str(group)] + 1

    for item in count:
        country_list = []

        country_list.append(item)

        for party in EUROPEAN_PARLIAMENT_GROUPS:
            actual_count = count[item][party]
            country_list.append(actual_count)

        csv_writer.writerow(country_list)

    group_party_city_country_file.close()
    groups_per_country_count_file.close()

    stop = timeit.default_timer()

    print
    print u'Runtime: %f seconds' % (stop - start)
