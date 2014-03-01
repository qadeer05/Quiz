from tornado import gen
from appmethods import *
import tornado.web
import motor
import datetime
from bson.objectid import ObjectId
import pwdhash

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("useremail")

class IndexHandler(BaseHandler):
    """Handler to serve the home page"""
    @tornado.web.authenticated
    def get(self):
        self.render('index.html', page="Home")


class LoginHandler(BaseHandler):
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


class LogoutHandler(BaseHandler):
    """Handler to logout the logged in user and then server the login page"""
    def get(self):
        self.render('login.html', page="Login")


class RegisterHandler(BaseHandler):
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

class ContactHandler(BaseHandler):
    """Handler to serve the contact us page"""
    def get(self):
        self.render('contact.html', page="Contact")


class AboutHandler(BaseHandler):
    """Handler to serve the about page"""
    def get(self):
        self.render('about.html', page="About")