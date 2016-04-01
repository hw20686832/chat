# coding:utf-8
import json
import time
import uuid

from tornado.web import RequestHandler, authenticated
from tornado.escape import to_basestring
from tornado.websocket import WebSocketHandler


class BaseHandler(RequestHandler):
    @property
    def redis(self):
        return self.application.redis

    def get_current_user(self):
        return self.get_secure_cookie("user")


class IndexHandler(BaseHandler):
    @authenticated
    def get(self):
        users = self.redis.smembers("users")
        if self.current_user in users:
            users.remove(self.current_user)
        self.render("index.html", users=users)


class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        uid = self.get_argument("uid")
        self.set_secure_cookie("user", uid, expires_days=None)
        self.redis.sadd("users", uid)
        self.redirect("/")


class ChatHandler(BaseHandler):
    @authenticated
    def get(self):
        obj = {
            'src': self.current_user,
            'dst': self.get_argument('dst'),
            'messages': []
        }
        self.render("chat.html", obj=obj)


class Tunnel(object):
    msg_from = None
    msg_to = None

    def __init__(self, msg_from=None, msg_to=None):
        self.msg_from = msg_from
        self.msg_to = msg_to

    def reverse(self):
        return Tunnel(msg_from=self.msg_to, msg_to=self.msg_from)


class PipHandler(WebSocketHandler):
    user_pool = {}

    @property
    def redis(self):
        return self.application.redis

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def open(self):
        dst = self.get_argument('dst')
        self.tunnel = (self.current_user, dst)
        print("User joined with tunnel %s->%s" % self.tunnel)
        self.load_unread()
        PipHandler.user_pool["%s->%s" % self.tunnel] = self

    def load_unread(self):
        key = "message:%s->%s" % self.tunnel[::-1]
        for message in self.redis.zrevrange(key, 0, -1):
            PipHandler.send(self, json.loads(message))
            self.redis.zrem(key, message)

    def on_message(self, message):
        # Message construct
        # {'src': 'david', 'dst': 'allen', 'body': 'hello world!'}
        msg = json.loads(message)
        dst = PipHandler.user_pool.get("%s->%s" % self.tunnel[::-1])
        msg['id'] = str(uuid.uuid4())

        PipHandler.send(self, msg)
        if dst:
            PipHandler.send(dst, msg)
        else:
            self.redis.zadd("message:%s->%s" % self.tunnel,
                            json.dumps(msg), time.time())

    @staticmethod
    def send(obj, msg):
        msg["html"] = to_basestring(
            obj.render_string("message.html", message=msg)
        )

        obj.write_message(msg)

    def on_close(self):
        del PipHandler.user_pool["%s->%s" % self.tunnel]
        print("User quit with tunnel %s->%s" % self.tunnel)
