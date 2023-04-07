# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 14:55:07 2023

@author: Administrator
"""

from flask import Flask
from flask_sockets import Sockets
import datetime
import time
import random

app = Flask(__name__)
sockets = Sockets(app)

@sockets.route('/echo')
def echo_socket(ws):
    while not ws.closed:
        now = datetime.datetime.now().isoformat() + 'Z'
        ws.send(now)  #发送数据
        time.sleep(1)

@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    print('server start')
    server.serve_forever()
