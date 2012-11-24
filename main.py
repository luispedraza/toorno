#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

# https://github.com/rutherford/nltk-gae NLTK
# http://www.ibm.com/developerworks/linux/library/l-cpnltk/index.html

from too_base import *
from too_users import *
from too_calendar import *

import logging

class MainPage(BaseHandler):
	def get(self):
		self.render("main.html")


class UserProfile(UserAccount):
	def get(self):
		if self.user:
			username = self.user.username
			email = self.user.email
			self.render("profile.html", 
				user=username, 
				email=email)
		else:
			self.redirect("/")
	def post(self):
		self.render("profile.html")

class Calendar(UserAccount):
	def get(self):
		if self.user:
			calendar = get_calendar()
			username = self.user.username
			self.render("calendar.html", user=username, calendar=calendar)
		else:
			self.redirect("/")

app = webapp2.WSGIApplication([
	('/', MainPage),
    ('/signup/?', UserSignup),
    ('/login/?', UserLogin),
    ('/logout/?', UserLogout),
    ('/calendar/?', Calendar),
    ('/profile/?', UserProfile)
], debug=True)