#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import timeit
import requests
import csv

GOOGLE_REVERSE_GEOCODING_BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?address='
SENSOR_MODIFIER = '&sensor=true'

if __name__ == "__main__":

    start = timeit.default_timer()

    locations_txt = open('locations_reverse_geocoding/locations.txt', 'r')
    locations_csv = open('locations_reverse_geocoding/locations.csv', 'w')

    csv_writer = csv.writer(locations_csv, delimiter=',')

    csv_writer.writerow(['city', 'country', 'lat', 'lng'])

    for location in locations_txt:
        location_array = location.split(', ')
        city = location_array[0].encode('utf-8')
        country = location_array[1].encode('utf-8').rstrip()

        r = requests.get('%s%s%s' % (GOOGLE_REVERSE_GEOCODING_BASE_URL, location, SENSOR_MODIFIER))

        if r.status_code == 200:
            json_response = json.loads(r.text)

            geo_coordinates = json_response['results'][0]['geometry']['location']

            lat = geo_coordinates['lat']
            lng = geo_coordinates['lng']

            csv_writer.writerow([city, country, lat, lng])

    locations_txt.close()
    locations_csv.close()

    stop = timeit.default_timer()

    print
    print u'Runtime: %f seconds' % (stop - start)
