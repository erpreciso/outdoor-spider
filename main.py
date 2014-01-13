# coding: utf-8
# Copyright 2014 erpreciso
#
#    OUTDOOR-SPIDER app
#
# TODO list
# a) crea file di testo con elenco città di partenza
# b) main page --> GET visualizza pulsante "importa"
# c) metodo POST:
#    1. importa il file di testo
#    2. stampa ancora il Main ma con la lista in html
#    3. visualizza tasto "Invia a Maps"
# d) JavaScript per richiesta a Maps


import webapp2
import jinja2
import os
import json, urllib

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
        self.render("test-js.html")

    def post(self):
        pairs = self.request.get("pairs")
        pairs = pairs[2:-2]
        pairs_list = pairs.split('],[')
        self.write("Hai inserito: " + pairs + " e la lista " + str(pairs_list))

def dict_from_list(input_list):
	"""return a dict from a parsed list.
	'input_list' is a fixed and repetitive structure: 
	[origin, destination, distance, origin, destination, distance, ...]
	
	"""
	
	
	
	
app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
