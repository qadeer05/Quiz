import os
import re
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload
import motor
import toredis
import constants
import appmethods

from tornado.options import define, options
from handlers import *


define("port", default=8080, help="run on the given port", type=int)
define("mongo_host", default="127.0.0.1", help="mongodb host ip")
define("redis_host", default="127.0.0.1", help="redis server ip")

class Application(tornado.web.Application):
    def __init__(self):
        
        # Connection to Redis and MongoDB
        #self.redis = toredis.Client()
        #self.redis.connect(options.redis_host)
        motor_client = motor.MotorClient(options.mongo_host, 27017).open_sync()
        #self.mongodb = motor_client.quizdb

        handlers = [
            (r"/", IndexHandler),
            (r"/login", LoginHandler),
            (r"/register", RegisterHandler),
            (r"/logout", LogoutHandler),
            (r"/contact", ContactHandler),
            (r"/about", AboutHandler),
        ]
        settings = dict(
            app_name=constants.APPNAME,
            template_path=constants.TEMPLATES_DIR,
            static_path=constants.ASSETS_DIR,
            xsrf_cookies=True,
            cookie_secret="ncjfuyendkll83slo73knaw2ladksygjbt9j3msksyalw65ksnmd",
            login_url="/login",
            ui_methods=appmethods,
            mongodb = motor_client.quizdb,
            #redispubsub = toredis.Client(),
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    instance = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(instance)
    instance.start()
