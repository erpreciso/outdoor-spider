# coding: utf-8
# Copyright 2014 erpreciso
#
#    OUTDOOR-SPIDER app
#

TODO = """

DONE
    GET '/'
    1. PY carica text file - "START" e poi lista di città, "END" e poi 
       lista di città
      a. funzione che importa la lista, e poi la splitta nelle due usando la 
         parola chiave
    2. stampa la pagina web inserendo un oggetto json nell'html tramite 
       l'attributo 'data-', trasformando le liste in liste html leggibili e con 
       un pulsante "GO"
       a. funzione che trasforma la lista in oggetto json
       b. funzione che crea il codice html contenente l'attributo 'data'
       c. jinja2 templates struttura, intestazioni, dati
    3. JS carica l'oggetto json (o la lista html) e manda la richiesta a Google 
       Maps
       a. Google ritorna un oggetto json come risposta
       b. l'oggetto viene inviato come POST a '/get_distance_matrix', e stampato 
          in html come conoscenza
    POST '/get_distance_matrix'
    4. PY carica il dato arrivato col POST in un oggetto json, e lo carica in 
       memoria nel blobstore

TODO per ogni città della lista, inviare la richiesta per il geocoding e 
     salvare anche questi in blobstore
TODO interfaccia utente per interrogare il blobstore, visualizzando poi la 
     mappa con la ragnatela, la matrice delle distanze etc.
"""

import webapp2
import jinja2
import os
import json
import urllib
import logging
import support_function as m
from google.appengine.ext import ndb, blobstore
from google.appengine.ext.webapp import blobstore_handlers

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
        autoescape = True)

class PointPair(ndb.Model):
    blob = ndb.BlobKeyProperty()
    start_point = ndb.StringProperty()
    end_point = ndb.StringProperty()
    status = ndb.StringProperty()
    distance_value = ndb.IntegerProperty()
    distance_text = ndb.StringProperty()
    duration_value = ndb.IntegerProperty()
    duration_text = ndb.StringProperty()
    
def json_city_lists():
    f = "city-list.txt"
    origins, destinations = m.split_city_list(m.list_from_file(f))
    return json.dumps({"origins" : origins, "destinations" : destinations})
    
class MainHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(MainHandler):
    def get(self):
        self.render("pagebody.html", json_data = json_city_lists())

class PostDistance(MainHandler):
    def post(self):
        
        #~ load json object coming from js ajax
        js = json.loads(self.request.body)
        
        #~ put the results in the blobstore
        origin = len(js['originAddresses'])
        destination = len(js['destinationAddresses'])
        for i in range(origin):
            for j in range(destination):
                p = PointPair()
                p.start_point = js['originAddresses'][i]
                p.end_point = js['destinationAddresses'][j]
                p.status = js['rows'][i]['elements'][j]['status']
                p.distance_value = js['rows'][i]['elements'][j]['distance']['value']
                p.distance_text = js['rows'][i]['elements'][j]['distance']['text']
                p.duration_value = js['rows'][i]['elements'][j]['duration']['value']
                p.duration_text = js['rows'][i]['elements'][j]['duration']['text']
                p.put()

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
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/post_distance', PostDistance),
], debug=True)
