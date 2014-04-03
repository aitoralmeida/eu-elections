#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from slugify import slugify

import os
import sys

lib_path = os.path.abspath('../')
sys.path.append(lib_path)

# from data.cache import codes_descriptor, university_locations


#   http://flask.pocoo.org/snippets/35/
class ReverseProxied(object):
    '''Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001; # where Flask app runs
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    '''
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

app = Flask(__name__)
app.config.from_object(__name__)
# app.wsgi_app = ReverseProxied(app.wsgi_app)
app.debug = True


###########################################################################
#####   Template filters
###########################################################################

@app.template_filter('slugify')
def _jinja2_filter_slugify(string):
    return slugify(unicode(string))


@app.template_filter('divisibleby')
def _jinja2_filter_divisibleby(dividend, divisor):
    return ((dividend % divisor) == 0)


###########################################################################
#####   Views
###########################################################################


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/topic_evolution/')
@app.route('/topic_evolution/<topic>')
def topic_evolution(topic="antropologia"):
    topics = []

    for key, value in codes_descriptor.items():
        if str(key)[2:6] == '0000':
            topics.append(value)

    topic_slug = topic

    if topic:
        topic = topic.upper().replace("-", " ")

    low_level_topic = False

    if (topic and topic not in topics):
        low_level_topic = True

    return render_template("topic_analysis/single_evolution.html", topic=topic, topic_slug=topic_slug, low_level_topic=low_level_topic, topics=sorted(topics))


###########################################################################
#####   Main
###########################################################################


if __name__ == '__main__':
    app.run(debug=True)
