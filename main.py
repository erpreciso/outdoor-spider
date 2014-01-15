# coding: utf-8
# Copyright 2014 erpreciso
#
#    OUTDOOR-SPIDER app
#

TODO = """
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
   memoria
   a. se è il primo, lo scrive nel blobstore
   b. altrimenti, scarica da blobstore (o da memcache), aggiunge i nuovi dati 
      e risalva in memoria

TODO interfaccia utente per interrogare il blobstore, visualizzando poi la 
     mappa con la ragnatela, la matrice delle distanze etc.
"""

import webapp2
import jinja2
import os
import json, urllib
import logging
from google.appengine.ext import ndb, blobstore
from google.appengine.ext.webapp import blobstore_handlers

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
		autoescape = True)

class JsonObj(ndb.Model):
	data = ndb.JsonProperty()

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
        self.render("pagebody.html")

class LearnPage(MainHandler):
    def get(self):
        self.render("learn.html")

class LearnPostPage(MainHandler):
    def post(self):
		t = self.request.body
		js = json.loads(t)	#js is a dict
		obj = JsonObj(data=js)
		obj.put()
		q = JsonObj.query()
		estr = q.get()
		logging.info(type(estr.data))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/learn', LearnPage),
    ('/learn_post', LearnPostPage),
], debug=True)
