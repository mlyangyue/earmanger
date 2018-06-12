#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

from app import app
from gevent import monkey
from gevent.pywsgi import WSGIServer
import sys
monkey.patch_all()
# from flask.ext.script import Manager
# manager = Manager(app)

if __name__ == "__main__":
    # manager.run()
    # app.run(host="0.0.0.0")
    host = '0.0.0.0'
    port = 5001
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = sys.argv[2]
    print host,port,sys.argv
    http_server = WSGIServer((host, int(port)), app)
    http_server.serve_forever()