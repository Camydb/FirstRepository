# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 01:31:42 2023

@author: amy
"""
import pymysql
import flask,json
from flask import request,send_file,jsonify,make_response,Flask
import shortuuid
import re
import random
import pandas as pd
import string
import time
from datetime import datetime
import urllib.parse

# from sqlalchemy import create_engine
'''
flask： web框架，通过flask提供的装饰器@server.route()将普通函数转换为服务
pip3 install flask -i https://pypi.doubanio.com/simple
'''
# 创建一个服务，把当前这个python文件当做一个服务

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    # app.run()
    app.run(host="172.31.82.161", port=5000, debug=True)
    #app.run(host="192.168.0.4", port=5000, debug=True,ssl_context=('server.crt','server.key'))