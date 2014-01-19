# coding: utf-8
# Copyright 2014 erpreciso
#
#    OUTDOOR-SPIDER app
#
# TESTS AND NOTES AREA

TODO = """
     
TODO all'inserimento della città di partenza e dei km:
     - disegna la mappa centrata
     - disegna le direzioni sulla mappa
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

mdict = {u'Trento, Italy': {u'Trento, Italy': {'distance_text': u'1 m', 'duration_text': u'1 min', 'duration_value': 0, 'distance_value': 0}, u'Aosta Aosta Valley, Italy': {'distance_text': u'401 km', 'duration_text': u'3 hours 57 mins', 'duration_value': 14209, 'distance_value': 400830}, u'Turin, Italy': {'distance_text': u'359 km', 'duration_text': u'3 hours 35 mins', 'duration_value': 12901, 'distance_value': 359268}, u'Genoa, Italy': {'distance_text': u'357 km', 'duration_text': u'3 hours 37 mins', 'duration_value': 13020, 'distance_value': 357437}, u'Milan, Italy': {'distance_text': u'226 km', 'duration_text': u'2 hours 25 mins', 'duration_value': 8688, 'distance_value': 225936}, u'28861 Baceno Verbano-Cusio-Ossola, Italy': {'distance_text': u'362 km', 'duration_text': u'3 hours 43 mins', 'duration_value': 13380, 'distance_value': 362327}, u'Rome, Italy': {'distance_text': u'592 km', 'duration_text': u'5 hours 35 mins', 'duration_value': 20074, 'distance_value': 591678}, u'Como, Italy': {'distance_text': u'266 km', 'duration_text': u'2 hours 47 mins', 'duration_value': 9997, 'distance_value': 266348}, u'Bari, Italy': {'distance_text': u'898 km', 'duration_text': u'7 hours 56 mins', 'duration_value': 28585, 'distance_value': 898331}, u'Lecco, Italy': {'distance_text': u'259 km', 'duration_text': u'2 hours 39 mins', 'duration_value': 9560, 'distance_value': 258760}}, u'Aosta Aosta Valley, Italy': {u'Trento, Italy': {'distance_text': u'400 km', 'duration_text': u'3 hours 56 mins', 'duration_value': 14149, 'distance_value': 399567}, u'Aosta Aosta Valley, Italy': {'distance_text': u'1 m', 'duration_text': u'1 min', 'duration_value': 0, 'distance_value': 0}, u'Turin, Italy': {'distance_text': u'116 km', 'duration_text': u'1 hour 22 mins', 'duration_value': 4893, 'distance_value': 115650}, u'Genoa, Italy': {'distance_text': u'249 km', 'duration_text': u'2 hours 30 mins', 'duration_value': 9029, 'distance_value': 248685}, u'Milan, Italy': {'distance_text': u'186 km', 'duration_text': u'2 hours 0 mins', 'duration_value': 7222, 'distance_value': 186383}, u'28861 Baceno Verbano-Cusio-Ossola, Italy': {'distance_text': u'239 km', 'duration_text': u'2 hours 31 mins', 'duration_value': 9067, 'distance_value': 238920}, u'Rome, Italy': {'distance_text': u'761 km', 'duration_text': u'7 hours 9 mins', 'duration_value': 25740, 'distance_value': 760805}, u'Como, Italy': {'distance_text': u'211 km', 'duration_text': u'2 hours 13 mins', 'duration_value': 8003, 'distance_value': 210991}, u'Bari, Italy': {'distance_text': u'1,067 km', 'duration_text': u'9 hours 31 mins', 'duration_value': 34251, 'distance_value': 1067458}, u'Lecco, Italy': {'distance_text': u'231 km', 'duration_text': u'2 hours 25 mins', 'duration_value': 8686, 'distance_value': 230984}}, u'Turin, Italy': {u'Trento, Italy': {'distance_text': u'357 km', 'duration_text': u'3 hours 34 mins', 'duration_value': 12812, 'distance_value': 356812}, u'Aosta Aosta Valley, Italy': {'distance_text': u'115 km', 'duration_text': u'1 hour 21 mins', 'duration_value': 4850, 'distance_value': 115328}, u'Turin, Italy': {'distance_text': u'1 m', 'duration_text': u'1 min', 'duration_value': 0, 'distance_value': 0}, u'Genoa, Italy': {'distance_text': u'172 km', 'duration_text': u'1 hour 53 mins', 'duration_value': 6787, 'distance_value': 172439}, u'Milan, Italy': {'distance_text': u'144 km', 'duration_text': u'1 hour 38 mins', 'duration_value': 5885, 'distance_value': 143628}, u'28861 Baceno Verbano-Cusio-Ossola, Italy': {'distance_text': u'196 km', 'duration_text': u'2 hours 9 mins', 'duration_value': 7730, 'distance_value': 196165}, u'Rome, Italy': {'distance_text': u'695 km', 'duration_text': u'6 hours 32 mins', 'duration_value': 23516, 'distance_value': 695170}, u'Como, Italy': {'distance_text': u'168 km', 'duration_text': u'1 hour 51 mins', 'duration_value': 6666, 'distance_value': 168236}, u'Bari, Italy': {'distance_text': u'1,002 km', 'duration_text': u'8 hours 54 mins', 'duration_value': 32027, 'distance_value': 1001821}, u'Lecco, Italy': {'distance_text': u'188 km', 'duration_text': u'2 hours 2 mins', 'duration_value': 7349, 'distance_value': 188229}}, u'Genoa, Italy': {u'Trento, Italy': {'distance_text': u'350 km', 'duration_text': u'3 hours 27 mins', 'duration_value': 12400, 'distance_value': 349608}, u'Aosta Aosta Valley, Italy': {'distance_text': u'248 km', 'duration_text': u'2 hours 27 mins', 'duration_value': 8842, 'distance_value': 247776}, u'Turin, Italy': {'distance_text': u'171 km', 'duration_text': u'1 hour 51 mins', 'duration_value': 6663, 'distance_value': 171287}, u'Genoa, Italy': {'distance_text': u'1 m', 'duration_text': u'1 min', 'duration_value': 0, 'distance_value': 0}, u'Milan, Italy': {'distance_text': u'143 km', 'duration_text': u'1 hour 39 mins', 'duration_value': 5936, 'distance_value': 143331}, u'28861 Baceno Verbano-Cusio-Ossola, Italy': {'distance_text': u'265 km', 'duration_text': u'2 hours 41 mins', 'duration_value': 9688, 'distance_value': 264546}, u'Rome, Italy': {'distance_text': u'502 km', 'duration_text': u'4 hours 53 mins', 'duration_value': 17561, 'distance_value': 502283}, u'Como, Italy': {'distance_text': u'187 km', 'duration_text': u'2 hours 4 mins', 'duration_value': 7439, 'distance_value': 187398}, u'Bari, Italy': {'distance_text': u'905 km', 'duration_text': u'8 hours 27 mins', 'duration_value': 30425, 'distance_value': 904855}, u'Lecco, Italy': {'distance_text': u'208 km', 'duration_text': u'2 hours 15 mins', 'duration_value': 8119, 'distance_value': 207709}}, u'Milan, Italy': {u'Trento, Italy': {'distance_text': u'223 km', 'duration_text': u'2 hours 23 mins', 'duration_value': 8558, 'distance_value': 223165}, u'Aosta Aosta Valley, Italy': {'distance_text': u'185 km', 'duration_text': u'2 hours 0 mins', 'duration_value': 7184, 'distance_value': 184626}, u'Turin, Italy': {'distance_text': u'143 km', 'duration_text': u'1 hour 38 mins', 'duration_value': 5877, 'distance_value': 143064}, u'Genoa, Italy': {'distance_text': u'147 km', 'duration_text': u'1 hour 46 mins', 'duration_value': 6346, 'distance_value': 146658}, u'Milan, Italy': {'distance_text': u'1 m', 'duration_text': u'1 min', 'duration_value': 0, 'distance_value': 0}, u'28861 Baceno Verbano-Cusio-Ossola, Italy': {'distance_text': u'146 km', 'duration_text': u'1 hour 46 mins', 'duration_value': 6347, 'distance_value': 146146}, u'Rome, Italy': {'distance_text': u'579 km', 'duration_text': u'5 hours 32 mins', 'duration_value': 19947, 'distance_value': 578890}, u'Como, Italy': {'distance_text': u'50.2 km', 'duration_text': u'49 mins', 'duration_value': 2964, 'distance_value': 50168}, u'Bari, Italy': {'distance_text': u'886 km', 'duration_text': u'7 hours 54 mins', 'duration_value': 28458, 'distance_value': 885542}, u'Lecco, Italy': {'distance_text': u'55.4 km', 'duration_text': u'52 mins', 'duration_value': 3109, 'distance_value': 55389}}, u'28861 Baceno Verbano-Cusio-Ossola, Italy': {u'Trento, Italy': {'distance_text': u'360 km', 'duration_text': u'3 hours 37 mins', 'duration_value': 13029, 'distance_value': 359602}, u'Aosta Aosta Valley, Italy': {'distance_text': u'237 km', 'duration_text': u'2 hours 25 mins', 'duration_value': 8696, 'distance_value': 237105}, u'Turin, Italy': {'distance_text': u'196 km', 'duration_text': u'2 hours 3 mins', 'duration_value': 7389, 'distance_value': 195543}, u'Genoa, Italy': {'distance_text': u'265 km', 'duration_text': u'2 hours 39 mins', 'duration_value': 9551, 'distance_value': 264565}, u'Milan, Italy': {'distance_text': u'146 km', 'duration_text': u'1 hour 42 mins', 'duration_value': 6099, 'distance_value': 146411}, u'28861 Baceno Verbano-Cusio-Ossola, Italy': {'distance_text': u'1 m', 'duration_text': u'1 min', 'duration_value': 0, 'distance_value': 0}, u'Rome, Italy': {'distance_text': u'724 km', 'duration_text': u'6 hours 52 mins', 'duration_value': 24744, 'distance_value': 723599}, u'Como, Italy': {'distance_text': u'155 km', 'duration_text': u'1 hour 44 mins', 'duration_value': 6256, 'distance_value': 154949}, u'Bari, Italy': {'distance_text': u'1,030 km', 'duration_text': u'9 hours 14 mins', 'duration_value': 33255, 'distance_value': 1030250}, u'Lecco, Italy': {'distance_text': u'191 km', 'duration_text': u'2 hours 6 mins', 'duration_value': 7566, 'distance_value': 191019}}, u'Rome, Italy': {u'Trento, Italy': {'distance_text': u'589 km', 'duration_text': u'5 hours 31 mins', 'duration_value': 19833, 'distance_value': 589350}, u'Aosta Aosta Valley, Italy': {'distance_text': u'760 km', 'duration_text': u'7 hours 6 mins', 'duration_value': 25544, 'distance_value': 760164}, u'Turin, Italy': {'distance_text': u'695 km', 'duration_text': u'6 hours 30 mins', 'duration_value': 23405, 'distance_value': 695010}, u'Genoa, Italy': {'distance_text': u'503 km', 'duration_text': u'4 hours 54 mins', 'duration_value': 17645, 'distance_value': 503175}, u'Milan, Italy': {'distance_text': u'577 km', 'duration_text': u'5 hours 28 mins', 'duration_value': 19658, 'distance_value': 576540}, u'28861 Baceno Verbano-Cusio-Ossola, Italy': {'distance_text': u'724 km', 'duration_text': u'6 hours 54 mins', 'duration_value': 24839, 'distance_value': 724272}, u'Rome, Italy': {'distance_text': u'1 m', 'duration_text': u'1 min', 'duration_value': 0, 'distance_value': 0}, u'Como, Italy': {'distance_text': u'628 km', 'duration_text': u'5 hours 58 mins', 'duration_value': 21455, 'distance_value': 628294}, u'Bari, Italy': {'distance_text': u'432 km', 'duration_text': u'4 hours 18 mins', 'duration_value': 15490, 'distance_value': 431856}, u'Lecco, Italy': {'distance_text': u'628 km', 'duration_text': u'5 hours 56 mins', 'duration_value': 21388, 'distance_value': 628222}}, u'Como, Italy': {u'Trento, Italy': {'distance_text': u'264 km', 'duration_text': u'2 hours 43 mins', 'duration_value': 9791, 'distance_value': 264157}, u'Aosta Aosta Valley, Italy': {'distance_text': u'209 km', 'duration_text': u'2 hours 10 mins', 'duration_value': 7819, 'distance_value': 209315}, u'Turin, Italy': {'distance_text': u'168 km', 'duration_text': u'1 hour 49 mins', 'duration_value': 6511, 'distance_value': 167753}, u'Genoa, Italy': {'distance_text': u'189 km', 'duration_text': u'2 hours 7 mins', 'duration_value': 7646, 'distance_value': 189428}, u'Milan, Italy': {'distance_text': u'51.0 km', 'duration_text': u'48 mins', 'duration_value': 2861, 'distance_value': 50966}, u'28861 Baceno Verbano-Cusio-Ossola, Italy': {'distance_text': u'155 km', 'duration_text': u'1 hour 46 mins', 'duration_value': 6377, 'distance_value': 155205}, u'Rome, Italy': {'distance_text': u'628 km', 'duration_text': u'5 hours 58 mins', 'duration_value': 21506, 'distance_value': 628154}, u'Como, Italy': {'distance_text': u'1 m', 'duration_text': u'1 min', 'duration_value': 0, 'distance_value': 0}, u'Bari, Italy': {'distance_text': u'935 km', 'duration_text': u'8 hours 20 mins', 'duration_value': 30017, 'distance_value': 934805}, u'Lecco, Italy': {'distance_text': u'31.4 km', 'duration_text': u'43 mins', 'duration_value': 2588, 'distance_value': 31434}}, u'Bari, Italy': {u'Trento, Italy': {'distance_text': u'896 km', 'duration_text': u'7 hours 55 mins', 'duration_value': 28495, 'distance_value': 895513}, u'Aosta Aosta Valley, Italy': {'distance_text': u'1,066 km', 'duration_text': u'9 hours 30 mins', 'duration_value': 34206, 'distance_value': 1066325}, u'Turin, Italy': {'distance_text': u'1,001 km', 'duration_text': u'8 hours 54 mins', 'duration_value': 32067, 'distance_value': 1001172}, u'Genoa, Italy': {'distance_text': u'906 km', 'duration_text': u'8 hours 28 mins', 'duration_value': 30479, 'distance_value': 905544}, u'Milan, Italy': {'distance_text': u'883 km', 'duration_text': u'7 hours 52 mins', 'duration_value': 28320, 'distance_value': 882702}, u'28861 Baceno Verbano-Cusio-Ossola, Italy': {'distance_text': u'1,030 km', 'duration_text': u'9 hours 18 mins', 'duration_value': 33501, 'distance_value': 1030434}, u'Rome, Italy': {'distance_text': u'432 km', 'duration_text': u'4 hours 21 mins', 'duration_value': 15672, 'distance_value': 432473}, u'Como, Italy': {'distance_text': u'934 km', 'duration_text': u'8 hours 22 mins', 'duration_value': 30118, 'distance_value': 934455}, u'Bari, Italy': {'distance_text': u'1 m', 'duration_text': u'1 min', 'duration_value': 0, 'distance_value': 0}, u'Lecco, Italy': {'distance_text': u'934 km', 'duration_text': u'8 hours 21 mins', 'duration_value': 30050, 'distance_value': 934384}}, u'Lecco, Italy': {u'Trento, Italy': {'distance_text': u'214 km', 'duration_text': u'2 hours 36 mins', 'duration_value': 9383, 'distance_value': 214270}, u'Aosta Aosta Valley, Italy': {'distance_text': u'229 km', 'duration_text': u'2 hours 24 mins', 'duration_value': 8637, 'distance_value': 229142}, u'Turin, Italy': {'distance_text': u'188 km', 'duration_text': u'2 hours 2 mins', 'duration_value': 7330, 'distance_value': 187580}, u'Genoa, Italy': {'distance_text': u'209 km', 'duration_text': u'2 hours 22 mins', 'duration_value': 8521, 'distance_value': 209491}, u'Milan, Italy': {'distance_text': u'55.1 km', 'duration_text': u'53 mins', 'duration_value': 3189, 'distance_value': 55101}, u'28861 Baceno Verbano-Cusio-Ossola, Italy': {'distance_text': u'191 km', 'duration_text': u'2 hours 10 mins', 'duration_value': 7809, 'distance_value': 190639}, u'Rome, Italy': {'distance_text': u'628 km', 'duration_text': u'5 hours 59 mins', 'duration_value': 21565, 'distance_value': 627958}, u'Como, Italy': {'distance_text': u'30.9 km', 'duration_text': u'44 mins', 'duration_value': 2646, 'distance_value': 30887}, u'Bari, Italy': {'distance_text': u'935 km', 'duration_text': u'8 hours 21 mins', 'duration_value': 30076, 'distance_value': 934610}, u'Lecco, Italy': {'distance_text': u'1 m', 'duration_text': u'1 min', 'duration_value': 0, 'distance_value': 0}}}

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

class ExportPage(MainHandler):
    def get(self):
        self.write(mdict)

app = webapp2.WSGIApplication([
    ("/spider", SpiderPage),
    ("/post_distance", PostDistance),
    ("/user", UserPage),
    ("/query", QueryPage),
    ("/print_mdict", ExportPage),
], debug=True)

# ----------------------------------------------------------------------------
