# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 16:37:11 2023

@author: amy
"""

from flask import Flask
from flask_sockets import Sockets
import datetime
import time
import requests

app = Flask(__name__)
sockets = Sockets(app)

from flask_cors import *
CORS(app, supports_credentials=True)

@sockets.route('/echo')
def echo_socket(ws):
    print("hello")
    msg = ws.receive()
    print(msg)
    while True:
        while not ws.closed:
            # now = datetime.datetime.now().isoformat()
            # time.sleep(3)
            if time.localtime().tm_sec == 0:
                re = requests.get(url='https://v1.hitokoto.cn/?encode=text')
                # print(re.text)
                ws.send(re.text)  #发送数据
                # now = datetime.datetime.now().isoformat()
                # print(now)
                time.sleep(1)
            

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('0.0.0.0', 8080), app, handler_class=WebSocketHandler)
    print('server start')
    server.serve_forever()
