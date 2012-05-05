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
# Purpose:     Homework 3 of Udacity 253 Class April 2012, a mini blog engine
#
# Author:      Aditya Lesmana
#
# Created:     04/05/2012
# Copyright:   (c) Aditya Lesmana 2012
# Licence:     Apache License 2.0
#-------------------------------------------------------------------------------

# Homework 3: Buld a blog
#   Main requirements
#     - Front page that lists entries. 10 most recent
#     - Form to submit new entries. Check validation here
#     - Permalink page for entries

#   Notes: 
#     - We assume your form to create new blog entries is at a path of 
#       '/newpost' from your blog's front page. 
#     - The form method must be POST, not GET.
#     - The form input boxes must have the names 'subject' and 'content' 
#     - Don't forget to escape your output!

#   Routing used: 
#     - /blog
#     - /blog/newpost
#     - /blog/<post-id> 

#   Resources: 
#     - A couple helpful links for HW 3
#       http://forums.udacity.com/cs253-april2012/questions/14750/a-couple-helpful-links-for-hw-3

import os
import webapp2
import jinja2
import logging
from google.appengine.ext import db


# Template related stuff
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

# TODO see http://jinja.pocoo.org/docs/api/#custom-filters for modifying data


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
        
# Creating Post entities 
# Note that it inherits from db.model (which we imported near the top of the app).
class Post(db.Model):
    """Models an individual Post entry with an subject, content, and date of creation."""
    subject = db.StringProperty(required = True)
    content= db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
        
# dealing with '/'
# redirecting to /blog in case user forgot to type '/blog'
class MainPage(Handler):
    def get(self):
        self.redirect("/blog") 
        
# rendering the index page of the blog
# remember 'Front page that lists entries. 10 most recent'
class BlogIndexPage(Handler):
    def render_index(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 10")
        self.render("index.html", posts=posts)
        
    def get(self):
        self.render_index()  

class BlogPostPage(Handler):
    def render_post(self, id=""):
        #post = db.GqlQuery("SELECT * FROM Post WHERE __key__ = KEY('Post', '_3'")
        post = Post.get_by_id(int(id))
        if post:
            self.render("post.html", post=post)
        else:
            self.redirect("/blog")
        
    def get(self, post_id):
        self.render_post(post_id)
        
        
class BlogNewPostPage(Handler):
    def render_new_post_form(self, subject="",content="", error=""):
        self.render("new_post.html", subject=subject, content=content, error=error)
        
    def get(self):
        self.render_new_post_form()  
        
    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        
        if subject and content:
            p = Post(subject = subject, content = content)
            p.put() # save to datastore
            self.redirect("/blog/%s" % str(p.key().id()) )
        else: 
            error = "Need subject and content to be filled"
            # apparently both notation below are correct
            # self.render_new_post_form(subject=subject, content=content, error=error)
            self.render_new_post_form(subject, content, error)

# TODO see http://webapp-improved.appspot.com/guide/routing.html for more explanation about routing
app = webapp2.WSGIApplication([ ('/', MainPage),
                                ('/blog', BlogIndexPage),
                                ('/blog/(\d+)', BlogPostPage),
                                ('/blog/newpost', BlogNewPostPage)
                              ],
                              debug=True)                              