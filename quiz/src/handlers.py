from tornado import gen
from appmethods import *
import tornado.web
import motor
import datetime
from bson.objectid import ObjectId
import pwdhash

class IndexHandler(tornado.web.RequestHandler):
    """Handler to serve the home page"""
    @tornado.web.authenticated
    def get(self):
        #self.render('index.html', page="Home")
        self.write('index')


class LoginHandler(tornado.web.RequestHandler):
    """Handler to serve the login page"""
    def get(self):
        self.render('login.html', page="Login")

    @tornado.web.asynchronous
    @gen.engine
    def post(self):
        email = self.get_argument('email')
        pwd = self.get_argument('pwd')

        db = self.settings["mongodb"]
        user = yield motor.Op(db.users.find_one, {'email': email})
        if user is not None:
            if pwdhash.check_hash(pwd, user['pwd']):
                #create login cookie 
                self.set_secure_cookie("useremail", email)
                self.redirect('/')


class LogoutHandler(tornado.web.RequestHandler):
    """Handler to logout the logged in user and then server the login page"""
    def get(self):
        self.render('login.html', page="Login")


class RegisterHandler(tornado.web.RequestHandler):
    """Handler to serve the new user registration page"""
    def get(self):
        self.render('register.html', page="Register")
    
    @tornado.web.asynchronous
    @gen.engine
    def post(self):
        name = self.get_argument('name')
        email = self.get_argument('email')
        pwd = self.get_argument('pwd')

        db = self.settings["mongodb"]
        user = yield motor.Op(db.users.find_one, {'email': email})
        if user is not None:
            raise Exception("Email already exists")

        yield motor.Op(db.users.insert, {
                'name': name,
                'email': email,
                'pwd': pwdhash.make_hash(pwd),
                'ts': datetime.datetime.utcnow(),
                '_id': ObjectId()})
        
        #create login cookie 
        self.set_secure_cookie("useremail", email)
        #self.finish()
        self.redirect('/')

class ContactHandler(tornado.web.RequestHandler):
    """Handler to serve the contact us page"""
    def get(self):
        self.render('contact.html', page="Contact")


class AboutHandler(tornado.web.RequestHandler):
    """Handler to serve the about page"""
    def get(self):
        self.render('about.html', page="About")