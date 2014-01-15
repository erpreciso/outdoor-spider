# coding: utf-8
# Copyright 2014 erpreciso
#
#    OUTDOOR-SPIDER app
#

#TODO
#fatto: ottenuta risposta dal server con matrice di città e distanze
#goal: scrivere i risultati sotto forma di lista, o dizionario, in un file di testo
#steps
#1. avendo in JS la risposta, inviarla con aiax al server sotto forma di JSON
#2. processarla con Python, e scrivere il file di testo

#poi... :
#visualizzare matrice delle distanze su richiesta
#visualizzare la ragnatela su Google Maps


import webapp2
import jinja2
import os
import json, urllib
import logging

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

class MainPage(MainHandler):
    def get(self):
        self.render("learn-js.html")

class LearnPage(MainHandler):
    def get(self):
        self.render("learn.html")

class LearnPostPage(MainHandler):
    def post(self):
		t = self.request.body
		js = json.loads(t)	#js is a dict


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/learn', LearnPage),
    ('/learn_post', LearnPostPage),
], debug=True)
