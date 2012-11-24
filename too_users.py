#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from too_database import *
from too_base import *
from google.appengine.api import images

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_username(username):
	return USER_RE.match(username)

def valid_passwrod(password):
	return PASS_RE.match(password)

def valid_email(email):
	return EMAIL_RE.match(email)



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

class UserAvatar(UserAccount):
	def get(self):
		if self.user:
			self.response.headers['Content-Type'] = 'image/jpg'
			self.response.out.write(self.user.avatar)

class UserSignup(UserAccount):
	def get(self):
		self.render("signup.html")

	def post(self):
		uerror = perror = merror = eerror = ""
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")
		if not valid_username(username):
			uerror=u"Nombre de usuario no válido"
		if not valid_passwrod(password):
			perror=u"Contraseña de usuario no válida"
		if (cmp(password,verify) != 0):
			merror=u"Las contraseñas no coinciden"
		if not valid_email(email):
			eerror=u"Dirección de correo no válida"
		if (uerror or perror or merror or eerror):
			self.render("signup.html", 
				user_error= uerror,
				pass_error=perror,
				match_error=merror,
				email_error=eerror,
				username=username,
				email=email)
		else:
			if User.by_username(username):
				self.render("signup.html", error=u"El usuario ya existe. Utiliza otro nombre.")
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

class UserProfile(UserAccount):
	def get(self, status=""):
		if self.user:
			if self.user.avatar:
				avatar="/avatar.jpg"
			else:
				avatar="/img/doctor.jpg"
			self.render("profile.html", 
				username=self.user.username, 
				email=self.user.email,
				name=self.user.name,
				surname=self.user.surname,
				avatar=avatar,
				status=status
				)
		else:
			self.redirect("/login")
	def post(self):
		uerror = perror = merror = eerror = ""
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")
		name = self.request.get("name")
		surname = self.request.get("surname")
		if not valid_username(username):
			uerror=u"Nombre de usuario no válido"
		if not valid_passwrod(password):
			perror=u"Contraseña de usuario no válida"
		if (cmp(password,verify) != 0):
			merror=u"Las contraseñas no coinciden"
		if not valid_email(email):
			eerror=u"Dirección de correo no válida"
		if (uerror or perror or merror or eerror):
			self.render("profile.html", 
				user_error= uerror,
				pass_error=perror,
				match_error=merror,
				email_error=eerror,
				username=username,
				email=email,
				name=name,
				surname=surname)
		else:
			if (username!=self.user.username) and User.by_username(username):
				self.get(status=u"El nombre de usuario ya existe. Utiliza otro.")
			else:
				avatar = images.resize(self.request.get("avatar"), 150, 150)
				u = User.register(username, password, email)
				self.user.username = username
				self.user.pwhash = u.pwhash
				self.user.email = email
				self.user.name = name
				self.user.surname = surname
				self.user.avatar = avatar
				self.user.put()
				self.get(status=u"Perfil actualizado correctamente.")