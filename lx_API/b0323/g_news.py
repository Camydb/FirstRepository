# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 14:09:48 2023

@author: amy
"""

import pymysql
import flask, json
from flask import request
import json
import shortuuid
import re
'''
flask： web框架，通过flask提供的装饰器@server.route()将普通函数转换为服务
pip3 install flask -i https://pypi.doubanio.com/simple

'''
# 创建一个服务，把当前这个python文件当做一个服务
server = flask.Flask(__name__)

Pattern1 = re.compile(r'^1[34578]\d{9}$')

HOST="120.48.49.157"
# HOST="127.0.0.1"


# server.config['JSON_AS_ASCII'] = False
# @server.route()可以将普通函数转变为服务 的路径、请求方式


# sql = "select app_ID from personal_information" 
# sql = 'UPDATE personal_information SET Following = "{}" WHERE app_ID = "{}"'.format(wd,appid)




@server.route('/topic_today', methods=['get'])#'get',
def G_topic_today():
    '''
        http://127.0.0.1:5000/topic_today
    http://120.48.49.157:5000/topic_today
    '''
    
    db = pymysql.connect(
        host=HOST, 
        port=3306,
        user='root',    #在这里输入用户名
        password='root123321',     #在这里输入密码
        charset='utf8mb4' ,
        database='GOOGLE'
        ) #连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # SQL 查询语句，查询user表
    sql = "select THEME,GPT3_TITLE from GL_NEWS" 
    # sql = "select * from user where name = '李四'"
    cursor.execute(sql)
    #这是查询表中所有的数据
    rest=cursor.fetchall()
    news_list = []
    for r in rest:
        b = r[0].replace('Google News -','').replace('- Overview','')
        news = {
            "theme":b,
            "sum_title":r[1]
            }
        if news not in news_list:
            news_list.append(news)
        # print(b,r[1])
        # print('-----------')
    # print(news_list)
    # print(len(news_list))
    cursor.close()  
    db.close()
    project = {
       "code": "OK",
       "msg": "谷歌新闻主题",
       "result":random.sample(news_list, 10)
    }
    response = json.dumps(project)  # 将python的字典转换为json字符串
    return response,200,{"Content-Type":"application/json"}

@server.route('/news_list', methods=['get'])#'get',
def G_news_lists():
    '''
        http://127.0.0.1:5000/news_list?word= Diablo 4's early access beta 
    http://120.48.49.157:5000/news_list?word= Diablo 4's early access beta 
    '''
    word = request.values.get('word')
    print(word)
    db = pymysql.connect(
        host=HOST, 
        port=3306,
        user='root',    #在这里输入用户名
        password='root123321',     #在这里输入密码
        charset='utf8mb4' ,
        database='GOOGLE'
        ) #连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # SQL 查询语句，查询user表
    sql = '''select GPT3_TEXT,TIME from GL_NEWS WHERE THEME like "%{}%"  '''.format(word)
    # sql = "select * from user where name = '李四'"
    cursor.execute(sql)
    #这是查询表中所有的数据
    rest=cursor.fetchall()
    # print(rest)
    news_list = []
    for r in rest:
        news = {
            "news":r[0],
            "Z_time":r[1]
            }
        if news not in news_list:
            news_list.append(news)
        # print(b,r[1])
        # print('-----------')
    # print(news_list)
    # print(len(news_list))
    cursor.close()  
    db.close()
    
    if len(news_list)!=0:
        project = {
           "code": "OK",
           "msg": "谷歌新闻列表",
           "result":random.choice(news_list)
        }
        response = json.dumps(project)  # 将python的字典转换为json字符串
        return response,200,{"Content-Type":"application/json"}
    else:
        project = {
           "code": "False",
           "msg": "谷歌新闻列表",
           "result":"可能不存在"
        }
        response = json.dumps(project)  # 将python的字典转换为json字符串
        return response,400,{"Content-Type":"application/json"}


@server.route('/twitter', methods=['get'])#'get',
def G_twitter():
    '''
        http://127.0.0.1:5000/twitter?word= Diablo 4's early access beta 
    http://120.48.49.157:5000/twitter?word= Diablo 4's early access beta 
    '''
    word = request.values.get('word')
    print(word)
    db = pymysql.connect(
        host=HOST, 
        port=3306,
        user='root',    #在这里输入用户名
        password='root123321',     #在这里输入密码
        charset='utf8mb4' ,
        database='GOOGLE'
        ) #连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # SQL 查询语句，查询user表
    sql = '''select PEOPLE,PINGL,TIME from Twitter WHERE CLASS like "%{}%"  '''.format(word)
    # sql = "select * from user where name = '李四'"
    cursor.execute(sql)
    #这是查询表中所有的数据
    rest=cursor.fetchall()
    # print(rest)
    news_list = []
    for r in rest:
        news = {
            "from":r[0],
            "talk":r[1],
            "Z_time":r[2]
            }
        if news not in news_list:
            news_list.append(news)
        # print(b,r[1])
        # print('-----------')
    # print(news_list)
    # print(len(news_list))
    cursor.close()  
    db.close()
    
    if len(news_list)!=0:
        project = {
           "code": "OK",
           "msg": "Twitter各方观点",
           "result":news_list
        }
        response = json.dumps(project)  # 将python的字典转换为json字符串
        return response,200,{"Content-Type":"application/json"}
    else:
        project = {
           "code": "False",
           "msg": "Twitter各方观点",
           "result":"可能不存在"
        }
        response = json.dumps(project)  # 将python的字典转换为json字符串
        return response,400,{"Content-Type":"application/json"}






if __name__ == "__main__":
    server.run()
    # server.run(host="192.168.0.4", port=5000, debug=True)
    #server.run(host="192.168.0.4", port=5000, debug=True,ssl_context=('server.crt','server.key'))