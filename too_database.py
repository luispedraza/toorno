#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import db
from google.appengine.api import memcache
import hashlib
import hmac
import random
import string
import datetime
import time

SECRET = "H8TtLd54HgAAhBdKA2SD"

def make_salt(length=5):
	return ''.join(random.choice(string.letters) for x in range(length))

# hashing of a string
def make_secure_val(val):
	return "%s|%s" % (val, hmac.new(SECRET, val).hexdigest())

# check string and hashing "string|haashing"
def check_secure_val(secure_val):
	val = secure_val.split("|")[0]
	if secure_val == make_secure_val(val):
		return val

def make_pw_hash(name, pw, salt=None):
	if not salt:
		salt = make_salt()
	h = hashlib.sha256(name + pw + salt).hexdigest()
	return '%s|%s' % (h, salt)

# returns True if user's password matches its hash
def valid_pw(name, pw, h):
	values = h.split("|")
	return h == make_pw_hash(name, pw, values[1])

# User info class
class User(db.Model):
	username = db.StringProperty(required=True)
	pwhash = db.StringProperty(required=True)
	email = db.StringProperty(required=True)

	@classmethod
	def by_id(cls, uid):
		return User.get_by_id(uid)

	@classmethod
	def by_username(cls, username):
		return User.all().filter("username =", username).get()

	@classmethod
	def register(cls, username, pw, email=None):
		pwhash = make_pw_hash(username, pw)
		return User(username=username, pwhash=pwhash, email=email)

	@classmethod
	def login(cls, username, pw):
		u = cls.by_username(username)
		if u and valid_pw(username, pw, u.pwhash):
			return u