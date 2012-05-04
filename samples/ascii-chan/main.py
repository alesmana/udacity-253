#!/usr/bin/env python
#
# Copyright 2007 Aditya lesmana
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#-------------------------------------------------------------------------------
# Name:        main.py
# Purpose:     ASCII Chan - Sample of GQL for Udacity 253 Unit 3 
#
# Author:      Udacity 253 ???
#
# Created:     ???
# Copyright:   (c) Udacity 2012 ???
# Licence:     ???
#-------------------------------------------------------------------------------


import os
import webapp2
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

# Something to inherit webapp2.RequestHandler
# Essentially wrap webapp2.RequestHandler and jinja2
# TODO find out what are *a and **kw
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
        
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
        
# Creating Art entities 
# Note that it inherits from db.model (which we imported near the top of the app).
class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
        

class MainPage(Handler):
    def render_front(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")
        self.render("front.html", title=title, art=art, error = error, arts = arts)

    def get(self):
        self.render_front()
        
    def post(self):
        title = self.request.get("title") 
        art = self.request.get("art")
        
        if title and art:
            a = Art(title = title, art = art)
            a.put() # save to Google datastore
            self.redirect("/")
        else:
            error = "we need both a title and some artwork!"
            self.render_front(title, art, error)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)