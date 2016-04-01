# coding:utf-8
# Web server config
HOST = '0.0.0.0'
PORT = 8808

DEBUG = False

TEMPLATE_ROOT = 'templates'
STATIC_ROOT = 'statics'

# redis
REDIS_CONF = {
    "host": "localhost",
    "port": 6379,
    "db": 0,
}
