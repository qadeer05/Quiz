import os
import re
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload
import asyncmongo
import toredis
import constants

from tornado.options import define, options
from handlers import *


define("port", default=8080, help="run on the given port", type=int)
define("mongo_host", default="127.0.0.1", help="mongodb host ip")
define("redis_host", default="127.0.0.1", help="redis server ip")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/login", LoginHandler),
            (r"/register", RegisterHandler),
            (r"/logout", LogoutHandler),
        ]
        settings = dict(
            app_name=u"Quiz",
            template_path=constants.TEMPLATES_DIR,
            static_path=constants.ASSETS_DIR,
            xsrf_cookies=True,
            cookie_secret="ncjfuyendkll83slo73knaw2ladksygjbt9j3msksyalw65ksnmd",
            login_url="/login"
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        # Connection to Redis and MongoDB
        #self.redis = toredis.Client()
        #self.redis.connect(options.redis_host)
        #self.mongodb = asyncmongo.Client(pool_id='quizdbpool', host=options.mongo_host, dbname='quiz')

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    instance = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(instance)
    instance.start()
