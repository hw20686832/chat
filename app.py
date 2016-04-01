# coding:utf-8
import os

import redis
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application

import settings
from handlers import *


class MyApplication(Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/login", LoginHandler),
            (r"/chat", ChatHandler),
            (r"/update", MainSockHandler)
            (r"/pip", PipHandler),
        ]
        config = dict(
            template_path=os.path.join(os.path.dirname(__file__), settings.TEMPLATE_ROOT),
            static_path=os.path.join(os.path.dirname(__file__), settings.STATIC_ROOT),
            xsrf_cookies=True,
            login_url="/login",
            cookie_secret="__E72013ADSDWIJODIE@(!)E@$*(5A1F2957AFD8EC0E7B51275EA7__",
            autoescape=None,
            debug=settings.DEBUG
        )
        Application.__init__(self, handlers, **config)

        self.redis = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )


def run():
    http_server = HTTPServer(MyApplication())
    http_server.listen(port=settings.PORT, address=settings.HOST)

    IOLoop.instance().start()


if __name__ == '__main__':
    run()
