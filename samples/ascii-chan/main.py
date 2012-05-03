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
# Purpose:     Homework 1 and Homework 2 of Udacity 253 Class April 2012
#
# Author:      Aditya Lesmana
#
# Created:     26/04/2012
# Copyright:   (c) Aditya Lesmana 2012
# Licence:     Apache License 2.0
#-------------------------------------------------------------------------------

import webapp2

import cgi # Unit2
import string # Unit2
import re # Unit2

# Unit 1 Homework 1
class HelloUdacityHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Hello, Udacity!")

# Unit 2 Homework 1

unit2_rot13_form ="""
<html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>

  <body>

    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"
                style="height: 100px; width: 400px;">%(textarea_text)s</textarea>
      <br>
      <input type="submit">
    </form>

  </body>

</html>
"""

class Rot13Handler(webapp2.RequestHandler):
    def write_form(self, textarea_text=''):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(unit2_rot13_form % {'textarea_text': textarea_text})

    # this function comes with escaping special character and such
    # sadly this does not work in python 3 :(
    def rot13_deprecated(self, s):
        return s.encode('rot13')

    def rot13(self, s):
        substitute_table = string.maketrans(
          "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
          "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm") # just whack it
        return s.translate(substitute_table)

    def get(self):
        self.write_form()

    def post(self):
        xcripted_text = self.request.get('text')
        xcripted_text = xcripted_text.encode('ascii') # half assed solution http://j.mp/I1tnrq
        xcripted_text = self.rot13(xcripted_text)
        self.write_form(xcripted_text)

# Unit 2 Homework 2

unit2_signup_success = """
<html>
  <head>
    <title>Unit 2 Signup</title>
  </head>

  <body>
    <h2>Welcome %(username)s</h2>
  </body>
</html>
"""
unit2_signup_form ="""
<html>
  <head>
    <title>Sign Up</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>

  </head>

  <body>
    <h2>Signup</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(username)s">
          </td>
          <td class="error">
            %(username_error)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="%(password)s">
          </td>
          <td class="error">
            %(password_error)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value="%(verify_password)s">
          </td>
          <td class="error">
            %(verify_password_error)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(email)s">
          </td>
          <td class="error">
            %(email_error)s
          </td>
        </tr>
      </table>

      <input type="submit">
    </form>
  </body>

</html>
"""


class UserSignupHandler(webapp2.RequestHandler):
    # In java I would treat this as final (and maybe static)
    # not sure how to do this kind of stuff in python
    ERROR_MSG_USERNAME        = "That's not a valid username."
    ERROR_MSG_PASSWORD        = "That wasn't a valid password."
    ERROR_MSG_VERIFY_PASSWORD = "Your passwords didn't match."
    ERROR_MSG_EMAIL           = "That's not a valid email."

    VALIDATION_USERNAME       = re.compile("^[a-zA-Z0-9_-]{3,20}$")
    VALIDATION_PASSWORD       = re.compile("^.{3,20}$")
    VALIDATION_EMAIL          = re.compile("^[\S]+@[\S]+\.[\S]+$")

    # TODO use array/list to handle this one
    def write_signup_form(self,
                    username='', password='', verify_password='', email='',
                    username_error='', password_error='', verify_password_error='', email_error=''):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(unit2_signup_form % {'username':username,
                                                     'password':password,
                                                     'verify_password':verify_password,
                                                     'email':email,
                                                     'username_error':username_error,
                                                     'password_error':password_error,
                                                     'verify_password_error':verify_password_error,
                                                     'email_error':email_error })

    def valid_username(self, username):
        # check if the username is good
        return self.VALIDATION_USERNAME.match(username)

    def valid_password(self, password):
        # check if the password follow the pattern
        return self.VALIDATION_PASSWORD.match(password)

    def valid_verify_password(self, password, verify_password):
        # check if password is not empty
        # and password == verify password
        if self.VALIDATION_PASSWORD.match(password):
            return password == verify_password
        else:
            return True

    def valid_email(self, email):
        # check if email is filled
        # if not, return true else run against regex
        if email:
            return self.VALIDATION_EMAIL.match(email)
        else:
            return True


    def get(self):
        self.write_signup_form()

    def post(self):
        username=self.request.get('username')
        password=self.request.get('password')
        verify_password=self.request.get('verify')
        email=self.request.get('email')

        username_error = password_error = verify_password_error = email_error = ""

        error = 0

        if not self.valid_username(username):
            username_error = self.ERROR_MSG_USERNAME
            error += 1
        if not self.valid_password(password):
            password_error = self.ERROR_MSG_PASSWORD
            error += 1
        if not self.valid_verify_password(password, verify_password):
            verify_password_error = self.ERROR_MSG_VERIFY_PASSWORD
            error += 1
        if not self.valid_email(email):
            email_error = self.ERROR_MSG_EMAIL
            error += 1

        if error == 0:
            # note that this is how to do redirection in webapp2
            # find ways to make it cleaner i.e. POST / array of param
            self.redirect("/unit2/welcome?username=%s" % username)
        else:
            # note that I omit password and verify_password field
            self.write_signup_form(username, '', '', email,
                                    username_error, password_error, verify_password_error, email_error)

class UserWelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username=self.request.get('username')
        self.response.out.write(unit2_signup_success % {'username':username})

# App controller
app = webapp2.WSGIApplication([ ('/', HelloUdacityHandler),
                                ('/unit1/hello', HelloUdacityHandler),
                                ('/unit2/signup', UserSignupHandler),
                                ('/unit2/welcome', UserWelcomeHandler),
                                ('/unit2/rot13', Rot13Handler)
                              ],
                              debug=True)