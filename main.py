#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
import jinja2
import os
import webapp2
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from models import *

jinja=jinja2.Environment(loader=jinja2.FileSystemLoader('pageFiles'))

def authUser(template):
    user = users.get_current_user()
    logout_url= users.create_logout_url('/')
    login_url= users.create_login_url('/')
    var={}
    var['home'] = 'home'#before user verification so it does not depend on login status
    if user:
        email=users.get_current_user().email()
        try:
            User.query(User.email==email).fetch()
        except:
            user= User(
                name=users.get_current_user().nickname(),
                email=users.get_current_user().email()
                )
            user.put()
        var['login_status'] = ('<a href="%s" id="login" class="siteLinks">Sign out</a>' % logout_url)
        if users.is_current_user_admin():
            var['home']= 'adminHome'
            var['admin']=('<a href="/admin" id="admin" class="siteLinks">Admin</a>')
    else:
        var['login_status'] = ('<a href="%s" id="login" class="siteLinks">Sign in</a>' % login_url)
    return var;

class MainHandler(webapp2.RequestHandler):
    def get(self):
        page = jinja.get_template('index.html')
        var = authUser(self)

        self.response.write(page.render(var))
class ContactHandler(webapp2.RequestHandler):
    def get(self):
        contact = jinja.get_template('contact.html')
        var = authUser(self)
        self.response.write(contact.render(var))
class AboutHandler(webapp2.RequestHandler):
    def get(self):
        about = jinja.get_template('about.html')
        var = authUser(self)
        self.response.write(about.render(var))

class AdminHandler(webapp2.RequestHandler):
    def get(self):
        admin = jinja.get_template('admin.html')
        var = authUser(self)
        var['upload_url'] = blobstore.create_upload_url('/upload_photo')
        if users.is_current_user_admin():
            self.response.write(admin.render(var))
        else:
            template.response.write('Not an administrator')
            self.redirect("/")


class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        name = self.request.get('title')
        media_type = self.request.get('media_type')
        category = self.request.get('category')
        upload = self.get_uploads()[0]
        user_photo = Photo(
            blob_key = upload.key(),
            name = name,
            media_type = media_type,
            category = category,
            likes = 0,
            comments = 0,
        )
        user_photo.put()
        self.redirect('/media/%s' % upload.key())


class MediaHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, photo_key):
        if not blobstore.get(photo_key):
            self.error(404)
        else:
            self.send_blob(photo_key)



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/contact',ContactHandler),
    ('/admin', AdminHandler),
    ('/about', AboutHandler),
    ('/upload_photo', PhotoUploadHandler),
    ('/media/([^/]+)?', MediaHandler),
], debug=True)
