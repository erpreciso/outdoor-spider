# coding: utf-8
# Copyright 2014 erpreciso
#
#    OUTDOOR-SPIDER app
#
# TESTS AND NOTES AREA

TODO = """
     
TODO visualizzando la mappa con la ragnatela, la matrice delle distanze etc.
"""

# ----------------------------------------------------------------------------

import webapp2
import jinja2
import os
import json
import urllib
import logging
import re
import support_function as m
from google.appengine.ext import ndb, blobstore
from google.appengine.ext.webapp import blobstore_handlers

# ----------------------------------------------------------------------------
# DICTIONARY HANDLERS

mdict = {}

def put_origin_in_dict(origin):
    global mdict
    if origin not in get_origin_list():
        mdict[origin] = {}

def put_destination_in_dict(origin, destination, travel_info):
    assert type(travel_info) == dict
    global mdict
    assert origin in mdict
    mdict[origin][destination] = travel_info

def get_origin_list():
    """return list of all origins."""
    return mdict.keys()

def get_destination_list_from(origin):
    """return list all destination from given origin."""
    return mdict[origin].keys()

def get_destinations_from_origin_given_distance(origin, distance, tolerance):
    """get a dict with destination, distance, duration from here
    recast it to have distance: destinations
    select ones within distance and tolerance provided
    return that.
    
    """
    destinations = get_destination_list_from(origin)
    assert len(destinations) > 0
    # creates the distance dict
    dist = {}
    for destination in destinations:
        d = mdict[origin][destination]['distance_value']
        dist[d] = destination
    # return only those in scope
    mn, mx = distance - tolerance, distance + tolerance
    return [(dist[d], d) for d in dist.keys() if d > mn and d < mx] 

# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# OTHER FUNCTIONS

def transform_list_in_json(key, value_list):
    """transform list provided in json format"""
    assert type(key) == str
    assert type(value_list) == list
    return json.dumps({key : value_list})
 
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# PAGES HANDLERS

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
        autoescape = True)

class MainHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

def json_city_lists():
    f = "city-list.txt"
    origins, destinations = m.split_city_list(m.list_from_file(f))
    #~ TODO risistema funzione in modo da caricare unica lista
    cities = origins + destinations
    return json.dumps({"cities" : cities})

class SpiderPage(MainHandler):
    def get(self):
        self.render(
                   "spiderbody.html",
                   json_data = json_city_lists(),
                   js_link = "spider",
                   )

class UserPage(MainHandler):
    def get(self):
        self.render(
                    "userbody.html",
                    json_data = transform_list_in_json("origins", get_origin_list()),
                    js_link = "user",
                    )

class QueryPage(MainHandler):
    def post(self):
        #~ load json object coming from js ajax
        js = json.loads(self.request.body)
        # calculates near cities
        near = get_destinations_from_origin_given_distance(
                js['start'],
                int(js['distance']),
                int(js['tolerance']),
                )
        logging.info(near)
        logging.info(mdict)
        self.response.out.write(transform_list_in_json("near", near))

class PostDistance(MainHandler):
    def post(self):
        #~ load json object coming from js ajax
        js = json.loads(self.request.body)
        #~ put the result in the dict
        global mdict
        origins = len(js['originAddresses'])
        destinations = len(js['destinationAddresses'])
        for i in range(origins):
            origin = js['originAddresses'][i]
            put_origin_in_dict(origin)
            for j in range(destinations):
                destination = js['destinationAddresses'][j]
                travel_info = {
                    "distance_value": js['rows'][i]['elements'][j]['distance']['value'],
                    "distance_text": js['rows'][i]['elements'][j]['distance']['text'],
                    "duration_value": js['rows'][i]['elements'][j]['duration']['value'],
                    "duration_text": js['rows'][i]['elements'][j]['duration']['text'],
                    }
                put_destination_in_dict(origin, destination, travel_info)
        self.response.out.write(transform_list_in_json("distance_result", ["OK"]))

app = webapp2.WSGIApplication([
    ('/spider', SpiderPage),
    ('/post_distance', PostDistance),
    ('/user', UserPage),
    ('/query', QueryPage),
], debug=True)

# ----------------------------------------------------------------------------
