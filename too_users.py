#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from too_database import *
from too_base import *

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

class UserAccount(BaseHandler):
	def set_secure_cookie(self, name, val):
		cookie_val = make_secure_val(val)
		self.response.headers.add_header(
			"Set-Cookie", "%s=%s" % (name, cookie_val))

	def get_secure_cookie(self, name):
		cookie_val = self.request.cookies.get(name)
		return cookie_val and check_secure_val(cookie_val)

	def login(self, uid):
		self.set_secure_cookie('user_id', str(uid))

	def logout(self):
		self.response.headers.add_header("Set-Cookie", "user_id=; Path=/")

	def initialize(self, *a, **kw):
		webapp2.RequestHandler.initialize(self, *a, **kw)
		uid = self.get_secure_cookie("user_id")
		self.user = uid and User.by_id(int(uid))

class UserSignup(UserAccount):
	def valid_username(self, username):
		return USER_RE.match(username)

	def valid_passwrod(self, password):
		return PASS_RE.match(password)

	def valid_email(self, email):
		return EMAIL_RE.match(email)

	def write_form(self, user_error=False, pass_error=False, match_error=False, email_error=False,
						username="", email="", error=""):
		uerror=""
		perror=""
		merror=""
		eerror=""
		if user_error:
			uerror=u"Nombre de usuario no válido"
		if pass_error:
			perror=u"Contraseña de usuario no válida"
		if match_error:
			merror=u"Las contraseñas no coinciden"
		if email_error:
			eerror=u"Dirección de correo no válida"
		self.render("signup.html", 
			user_error= uerror,
			pass_error=perror,
			match_error=merror,
			email_error=eerror,
			username=username,
			email=email,
			error=error)

	def get(self):
		self.write_form()

	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")
		uerror = not self.valid_username(username)
		perror = not self.valid_passwrod(password)
		verror = (cmp(password,verify) != 0)
		eerror = not self.valid_email(email)
		if (uerror or perror or verror or eerror):
			self.write_form(uerror, perror, verror, eerror, username, email)
		else:
			if User.by_username(username):
				self.write_form(error=u"El usuario ya existe. Utiliza otro nombre.")
			else:
				u = User.register(username, password, email)
				u.put()
				self.login(u.key().id())
				self.redirect("/calendar")

class UserLogin(UserAccount):
	def write_form(self, error=""):
		self.render("login.html", 
			error=error)
	def get(self):
		self.write_form()
	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")	
		u = User.login(username, password)	
		if u:
			self.set_secure_cookie("user_id", str(u.key().id()))
			self.redirect("/calendar")
		else:
			self.write_form(u"No válido")

class UserLogout(UserAccount):
	def get(self):
		self.logout()
		self.redirect("/login")