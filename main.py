# coding: utf-8
# Copyright 2014 erpreciso
#
#    OUTDOOR-SPIDER app
#
# TESTS AND NOTES AREA
JSO = """
{
    u'originAddresses': [u'Milan, Italy'],
    u'destinationAddresses': [u'Trento, Italy', u'Genoa, Italy'], 
    u'rows':[
        {u'elements': [
            {u'status': u'OK', u'duration': {u'text': u'2 hours 23 mins', u'value': 8558}, u'distance': {u'text': u'223 km', u'value': 223165}}, 
            {u'status': u'OK', u'duration': {u'text': u'1 hour 46 mins', u'value': 6346}, u'distance': {u'text': u'147 km', u'value': 146658}}
        ]}]
}"""

TODO = """

PRIO 1
TODO per ogni città della lista, inviare la richiesta per il geocoding
     - carica lista di città da txt
     - per ogni città manda richiesta geocoding
     - salva questa risposta in dizionario
     - manda richiesta distanze
     - salva anche questa nel dizionario
     
TODO fai in modo che la lista sia una sola e che le richieste vadano tutti 
     con tutti
     
TODO interfaccia utente per interrogare il blobstore, visualizzando poi la 
     mappa con la ragnatela, la matrice delle distanze etc.
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

mdict = {"distance":{}, "geocoding": {}}

def put_origin_in_dict(origin):
    global mdict
    if origin not in get_origin_list():
        mdict["distance"][origin] = {}

def put_destination_in_dict(origin, destination, travel_info):
    assert type(travel_info) == dict
    global mdict
    assert origin in mdict["distance"]
    mdict["distance"][origin][destination] = travel_info

def get_origin_list():
    """return list of all origins."""
    global mdict
    return mdict["distance"].keys()

def get_destination_list_from(origin):
    """return list all destination from given origin."""
    global mdict
    return mdict["distance"][origin].keys()

def get_destinations_from_origin_given_distance(origin, distance, tolerance):
    """get a dict with destination, distance, duration from here
    recast it to have distance: destinations
    select ones within distance and tolerance provided
    return that.
    
    """
    global mdict
    destinations = get_destination_list_from(origin)
    assert len(destinations) > 0
    # creates the distance dict
    dist = {}
    for destination in destinations:
        d = mdict["distance"][origin][destination]['distance_value']
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

class PostGeocoding(MainHandler):
    def post(self):
        #~ load json object coming from js ajax
        js = json.loads(self.request.body)
        logging.info(str(js))

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
    ('/post_geocoding', PostGeocoding),
    ('/user', UserPage),
    ('/query', QueryPage),
], debug=True)

# ----------------------------------------------------------------------------
