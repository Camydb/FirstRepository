# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 17:36:33 2023

@author: Administrator
"""
import pymysql
import flask, json
from flask import request
# import json
import shortuuid
import re
import random
import pandas as pd
import string
import time
from datetime import datetime
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

def get_now_time():
    SAVE_TIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date1 = datetime.strptime(str(SAVE_TIME), "%Y-%m-%d %H:%M:%S")
    s_t=time.strptime(str(date1),"%Y-%m-%d %H:%M:%S")
    S_TIME=int(time.mktime(s_t))
    return(SAVE_TIME,S_TIME)

def get_like(userID):
    db = pymysql.connect(
        host=HOST, 
        port=3306,
        user='root',    #在这里输入用户名
        password='root123321',     #在这里输入密码
        charset='utf8mb4' ,
        database='USER'
        ) #连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    # cursor = db.cursor()
    # 使用pandas的read_sql函数读取数据
    df = pd.read_sql('''SELECT news_ID,class_n FROM user_like WHERE user_ID= "{}"  '''.format(userID), db)
    # '''select PEOPLE,PINGL,TIME,ZH_CN from Twitter WHERE CLASS like "%{}%"  '''.format(word)
    # 关闭连接
    db.close()
    # ((df.loc[df['class_n'] == 'news'])['news_ID'])
    return(tuple((df.loc[df['class_n'] == 'news'])['news_ID']),tuple((df.loc[df['class_n'] == 'talk'])['news_ID']))

def get_username():
    vowels = "aeiou"
    consonants = "".join(set(string.ascii_lowercase) - set(vowels))
    username = ""
    for i in range(8):
        if i % 2 == 0:
            username += random.choice(consonants)
        else:
            username += random.choice(vowels)
    return ("User_"+username)


def get_max_time(like):
    db = pymysql.connect(
        host=HOST, 
        port=3306,
        user='root',    #在这里输入用户名
        password='root123321',     #在这里输入密码
        charset='utf8mb4' ,
        database='GOOGLE'
        ) #连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    # cursor = db.cursor()
    # 使用pandas的read_sql函数读取数据
    df = pd.read_sql('''SELECT NEWS_ID,TIME,S_TIME FROM GL_NEWS WHERE THEME LIKE "%{}%" '''.format(like), db)
    # '''select PEOPLE,PINGL,TIME,ZH_CN from Twitter WHERE CLASS like "%{}%"  '''.format(word)
    # 关闭连接
    db.close()

    # 输出数据框
    # print(df)
    return(max(df['S_TIME']))


def get_act(search_id,class_n):
    db = pymysql.connect(
        host=HOST, 
        port=3306,
        user='root',    #在这里输入用户名
        password='root123321',     #在这里输入密码
        charset='utf8mb4' ,
        database='USER'
        ) #连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    # cursor = db.cursor()
    # 使用pandas的read_sql函数读取数据
    if class_n == 'news' or class_n == 'talk':
        df = pd.read_sql('''SELECT user_ID,class_n FROM user_like WHERE news_ID= "{}"  '''.format(search_id), db)
        db.close()
        df = df.drop_duplicates('user_ID')#.sort_index()
        return(len(df))
    
    elif class_n == 'discuss':
        df = pd.read_sql('''SELECT user_ID,discuss_ID,class_n FROM user_discuss WHERE news_ID= "{}"  '''.format(search_id), db)
        db.close()
        df = df.drop_duplicates('discuss_ID')#.sort_index()
        return(len(df))
    
    else:
        print('False')
        db.close()
        return 0



@server.route('/discuss_list', methods=['get'])
def Projectlist_10():
    '''
        http://127.0.0.1:5000/discuss_list?newsID=8T4AZAkd5t9bBXG3kFuAUP&class_n=news
    http://120.48.49.157:5000/discuss_list?newsID=8T4AZAkd5t9bBXG3kFuAUP&class_n=talk
    '''
    
    newsID = request.values.get('newsID')
    
    
    db = pymysql.connect(
        host=HOST, 
        port=3306,
        user='root',    #在这里输入用户名
        password='root123321',     #在这里输入密码
        charset='utf8mb4' ,
        database='USER'
        ) #连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    # cursor = db.cursor()
    # SQL 查询语句，查询user表
    # sql = "select THEME,GPT3_TITLE,KEY_WORD from GL_NEWS" 
    try:
        df = pd.read_sql('''select * from user_discuss where news_ID = "{}" '''.format(newsID) , db)
        db.close()
        df = df.sort_values('S_time', ascending=False).drop_duplicates('discuss_ID')#.sort_index()
        
        discuss_list = []
        
        for index, row in df.iterrows():
            
            # b = row['THEME'].replace('Google News -','').replace('- Overview','')
            # st = get_max_time(b)
            news = {
                "user_ID":row['user_ID'],
                "news_ID":row['news_ID'],
                "discuss_ID":row['discuss_ID'],
                "discuss_text":row['discuss_text'],
                "username":row['username'],
                "time":row['time'],
                "S_time":row['S_time']
                
                }
            if news not in discuss_list:
                discuss_list.append(news)
        
        project = {
           "code": "OK",
           "msg": '评论列表',
           "result":{
           "discuss_list":discuss_list
            }
        }
        response = json.dumps(project)  # 将python的字典转换为json字符串
        return response,200,{"Content-Type":"application/json"}
    except Exception as e:
        db.rollback()
        print(e)
        project = {
           "code": "False",
           "msg": '错误！',
           "result":{
            "Error": str(e)
            }
        }
        response = json.dumps(project)  # 将python的字典转换为json字符串
        return response,400,{"Content-Type":"application/json"}
    



@server.route('/del_discuss', methods=['post'])
def Projectlist11():
    '''
        http://127.0.0.1:5000/del_discuss?userID=3FtPAHrhhveJGNzC5FaBWv&discussID=VSDV&class_n=news
    http://120.48.49.157:5000/del_discuss?userID=3FtPAHrhhveJGNzC5FaBWv&discussID=VSDV&class_n=talk
    '''
    userID = request.values.get('userID')
    discussID = request.values.get('discussID')
    try:
        conn = pymysql.connect(
            host=HOST, 
            port=3306,
            user='root',    #在这里输入用户名
            password='root123321',     #在这里输入密码
            charset='utf8mb4' ,
            database='USER'
            ) #连接数据库
        cur = conn.cursor()
        sql = '''delete from user_discuss where user_ID="{}" and discuss_ID="{}" '''.format(userID,discussID)
        cur.execute(sql)
        conn.commit()
        conn.close()
        
        project = {
           "code": "OK",
           "msg": '删除评论',
           "result":{
               "userID":userID,
               "discussID":discussID
           
            }
        }
        response = json.dumps(project)  # 将python的字典转换为json字符串
        return response,200,{"Content-Type":"application/json"}
    except Exception as e:
        print(e)
        project = {
           "code": "False",
           "msg": "no message",
           "result":str(e)
        }
        response = json.dumps(project)  # 将python的字典转换为json字符串
        return response,400,{"Content-Type":"application/json"}


@server.route('/user_discuss', methods=['post'])
def Projectlist9():
    '''
        http://127.0.0.1:5000/user_discuss?userID=3FtPAHrhhveJGNzC5FaBWv&newsID=VSDV&text=Gwyneth Paltrow denied a man’s accusation&username=User_dadsd&class_n=news
        http://127.0.0.1:5000/user_discuss?userID=3FtPAHrhhveJGNzC5FaBWv&newsID=VSDV&text=Gwyneth Paltrow denied a man’s accusation&username=User_dadsd&class_n=news
    http://120.48.49.157:5000/user_discuss?userID=3FtPAHrhhveJGNzC5FaBWv&newsID=VSDV&text=Gwyneth Paltrow denied a man’s accusation&username=User_dadsd&class_n=talk
    '''
    userID = request.values.get('userID')
    newsID = request.values.get('newsID')
    text = request.values.get('text')
    class_n = request.values.get('class_n')
    username = request.values.get('username')
    text1 = text.replace("\"","\'")
    
    conn = pymysql.connect(
        host=HOST, 
        port=3306,
        user='root',    #在这里输入用户名
        password='root123321',     #在这里输入密码
        charset='utf8mb4' ,
        database='USER'
        ) #连接数据库
    cur = conn.cursor()
    
    try:
        time,stime = get_now_time()
        discuss_ID = shortuuid.ShortUUID().random(length=12)
        cur.execute(
            '''INSERT INTO user_discuss (user_ID,news_ID,discuss_ID,discuss_text,username,time,S_time,class_n) VALUES ("{}","{}","{}","{}","{}","{}","{}","{}")'''.format(userID,newsID,discuss_ID,text1,username,time,stime,class_n));
        conn.commit()
        print ("记录插入成功!")
        project = {
           "code": "OK",
           "msg": '评论成功',
           "result":{

            "user_ID":userID,
            "news_ID":newsID,
            "discuss_ID":discuss_ID,
            "discuss_text":text,
            "username":username,
            "time":time,
            "S_time":stime
                
                
            }
        }
        response = json.dumps(project)  # 将python的字典转换为json字符串
        return response,200,{"Content-Type":"application/json"}
    except Exception as e:
        conn.rollback()
        print(e)
        project = {
           "code": "False",
           "msg": '错误！',
           "result":{
            "Error": str(e)
            }
        }
        response = json.dumps(project)  # 将python的字典转换为json字符串
        return response,401,{"Content-Type":"application/json"}
    conn.close()

@server.route('/user_like', methods=['post'])
def Projectlist8():
    '''
        http://127.0.0.1:5000/user_like?userID=3FtPAHrhhveJGNzC5FaBWv
    http://120.48.49.157:5000/user_like?userID=3FtPAHrhhveJGNzC5FaBWv
    '''
    userID = request.values.get('userID')
    # newsID = request.values.get('newsID')
    
    
    like_news,like_talk = get_like(userID)
    
    try:
        if len(like_news)>0 or len(like_talk)>0:
            db = pymysql.connect(
                host=HOST, 
                port=3306,
                user='root',    #在这里输入用户名
                password='root123321',     #在这里输入密码
                charset='utf8mb4' ,
                database='GOOGLE'
                ) #连接数据库
            lm = list(like_news)
            lt = list(like_talk)
            cur = db.cursor()
            
            df = pd.DataFrame(columns=['GPT3_TEXT', 'TIME', 'KEY_WORD', 'S_TIME', 'TITLE', 'NEWS_ID','ZH_CN','T_ZH','KW_ZH'])
            # 执行查询语句
            cur.execute('SELECT GPT3_TEXT, TIME, KEY_WORD, S_TIME, TITLE, NEWS_ID,ZH_CN,T_ZH,KW_ZH FROM GL_NEWS')
            # 遍历查询结果并保存到 Pandas 数据框中
            for row in cur:
                if row[5] in lm:
                    df = df.append({'GPT3_TEXT': row[0], 'TIME': row[1], 'KEY_WORD': row[2], 'S_TIME': row[3], 'TITLE': row[4], 'NEWS_ID': row[5], 'ZH_CN': row[6], 'T_ZH': row[7], 'KW_ZH': row[8]}, ignore_index=True)
                    
            
            df = df.sort_values('S_TIME', ascending=False).drop_duplicates('NEWS_ID')#.sort_index()
    
            news_list = []
            
            for index, row in df.iterrows():
                like_sum = get_act(row['NEWS_ID'],'news')
                discuss_sum = get_act(row['NEWS_ID'],'discuss')
                # b = row['THEME'].replace('Google News -','').replace('- Overview','')
                # st = get_max_time(b)
                news = {
                    "news":row['GPT3_TEXT'],
                    "Z_time":row['TIME'],
                    "Key_word":row['KEY_WORD'],
                    "Title":row['TITLE'],
                    "NEWS_ID":row['NEWS_ID'],
                    "ZH_CN":row['ZH_CN'],
                    "T_ZH":row['T_ZH'],
                    "KW_ZH":row['KW_ZH'],
                    "like":True,
                    "like_sum":like_sum,
                    "discuss_sum":discuss_sum,
                    "share_sum":0,
                    "dislike_sum":0
                    }
                if news not in news_list:
                    news_list.append(news)
                    
            
            df = pd.DataFrame(columns=["THEME","GPT3_TITLE","KEY_WORD","S_TIME","TIME","TH_ID","TH_ZH","GT_ZH","KW_ZH"])
            # 执行查询语句
            cur.execute('SELECT THEME,GPT3_TITLE,KEY_WORD,S_TIME,TIME,TH_ID,TH_ZH,GT_ZH,KW_ZH FROM GL_NEWS')
            # 遍历查询结果并保存到 Pandas 数据框中
            for row in cur:
                if row[5] in lt:
                    df = df.append({'THEME': row[0], 'GPT3_TITLE': row[1], 'KEY_WORD': row[2], 'S_TIME': row[3], 'TIME': row[4], 'TH_ID': row[5], 'TH_ZH': row[6], 'GT_ZH': row[7], 'KW_ZH': row[8]}, ignore_index=True)
                    
            
            
            # sql = '''select THEME,GPT3_TITLE,KEY_WORD,S_TIME,TIME,TH_ID from GL_NEWS WHERE TH_ID in {} '''.format(like_talk)
            # df = pd.read_sql(sql , db)
            db.close()
            df = df.sort_values('S_TIME', ascending=False).drop_duplicates('TH_ID')#.sort_index()
            
            talk_list = []
            
            for index, row in df.iterrows():
                like_sum = get_act(row['TH_ID'],'news')
                discuss_sum = get_act(row['TH_ID'],'discuss')
                b = row['THEME'].replace('Google News -','').replace('- Overview','')
                c = row['TH_ZH'].replace('谷歌新闻-','').replace('-概述','')
                # st = get_max_time(b)
                talks = {
                    "theme":b,
                    "sum_title":row['GPT3_TITLE'],
                    "Key_word":row['KEY_WORD'],
                    "S_time":row['S_TIME'],
                    "TIME":row['TIME'],
                    "NEWS_ID":row['TH_ID'],
                    "TH_ZH":c,
                    "GT_ZH":row['GT_ZH'],
                    "KW_ZH":row['KW_ZH'],
                    "like":True,
                    "like_sum":like_sum,
                    "discuss_sum":discuss_sum,
                    "share_sum":0,
                    "dislike_sum":0
                    }
    
                if talks not in talk_list:
                    talk_list.append(talks)
    
    
            project = {
               "code": "OK",
               "msg": '用户收藏',
               "result":{
                "news_list":news_list,
                "talk_list":talk_list
                }
            }
            response = json.dumps(project)  # 将python的字典转换为json字符串
            return response,200,{"Content-Type":"application/json"}
        else:
            project = {
               "code": "False",
               "msg": 'no message',
               "result":{
                }
            }
            response = json.dumps(project)  # 将python的字典转换为json字符串
            return response,200,{"Content-Type":"application/json"}
    except Exception as e:
        project = {
           "code": "False",
           "msg": "no message",
           "result":str(e)
        }
        response = json.dumps(project)  # 将python的字典转换为json字符串
        return response,400,{"Content-Type":"application/json"}

@server.route('/add_like', methods=['post'])
def Projectlist7():
    '''
        http://127.0.0.1:5000/add_like?userID=2132&newsID=2312312&is_like=1&class_n=news
    http://120.48.49.157:5000/add_like?userID=2132&newsID=2312312&is_like=0&class_n=news
    '''
    userID = request.values.get('userID')
    newsID = request.values.get('newsID')
    is_like = int(request.values.get('is_like'))
    class_n = request.values.get('class_n')
    # is_low = request.values.get('is_low')
    
    conn = pymysql.connect(
        host=HOST, 
        port=3306,
        user='root',    #在这里输入用户名
        password='root123321',     #在这里输入密码
        charset='utf8mb4' ,
        database='USER'
        ) #连接数据库
    cur = conn.cursor()
    
    
    if class_n == 'news':
        if is_like==1:
            try:
                cur.execute(
                    '''INSERT INTO user_like (user_ID,news_ID,class_n) VALUES ("{}","{}","{}")'''.format(userID,newsID,class_n));
                conn.commit()
                print ("记录插入成功!")
                project = {
                   "code": "OK",
                   "msg": '收藏成功',
                   "result":{
                    "userID":userID,
                    "newsID":newsID
                    }
                }
                response = json.dumps(project)  # 将python的字典转换为json字符串
                return response,200,{"Content-Type":"application/json"}
            except Exception as e:
                conn.rollback()
                print(e)
                project = {
                   "code": "False",
                   "msg": '错误！',
                   "result":{
                    "Error": str(e)
                    }
                }
                response = json.dumps(project)  # 将python的字典转换为json字符串
                return response,401,{"Content-Type":"application/json"}
        elif is_like==0:
            
            sql = '''delete from user_like where user_ID="{}" and news_ID="{}" '''.format(userID,newsID)
            cur.execute(sql)
            conn.commit()
            
            project = {
               "code": "OK",
               "msg": '取消收藏',
               "result":{
                "userID":userID,
                "newsID":newsID
                }
            }
            response = json.dumps(project)  # 将python的字典转换为json字符串
            return response,200,{"Content-Type":"application/json"}
        
        else:
            project = {
               "code": "False",
               "msg": '错误',
               "result":{
                "userID":userID,
                "newsID":newsID
                }
            }
            response = json.dumps(project)  # 将python的字典转换为json字符串
            return response,402,{"Content-Type":"application/json"}
    if class_n == 'talk':
        if is_like==1:
            try:
                cur.execute(
                    '''INSERT INTO user_like (user_ID,news_ID,class_n) VALUES ("{}","{}","{}")'''.format(userID,newsID,class_n));
                conn.commit()
                print ("记录插入成功!")
                project = {
                   "code": "OK",
                   "msg": '收藏成功',
                   "result":{
                    "userID":userID,
                    "newsID":newsID,
                    "_class":class_n
                    }
                }
                response = json.dumps(project)  # 将python的字典转换为json字符串
                return response,200,{"Content-Type":"application/json"}
            except Exception as e:
                conn.rollback()
                print(e)
                project = {
                   "code": "False",
                   "msg": '错误！',
                   "result":{
                    "Error": str(e)
                    }
                }
                response = json.dumps(project)  # 将python的字典转换为json字符串
                return response,403,{"Content-Type":"application/json"}
        elif is_like==0:
            
            sql = '''delete from user_like where user_ID="{}" and news_ID="{}" '''.format(userID,newsID)
            cur.execute(sql)
            conn.commit()
            
            project = {
               "code": "OK",
               "msg": '取消收藏',
               "result":{
                "userID":userID,
                "newsID":newsID,
                "_class":class_n
                }
            }
            response = json.dumps(project)  # 将python的字典转换为json字符串
            return response,200,{"Content-Type":"application/json"}
        
        else:
            project = {
               "code": "False",
               "msg": '错误',
               "result":{
                "userID":userID,
                "newsID":newsID,
                "_class":class_n
                }
            }
            response = json.dumps(project)  # 将python的字典转换为json字符串
            return response,404,{"Content-Type":"application/json"}
    project = {
       "code": "False",
       "msg": '错误',
       "result":{
        "userID":userID,
        "newsID":newsID,
        "_class":class_n
        }
    }
    response = json.dumps(project)  # 将python的字典转换为json字符串
    return response,405,{"Content-Type":"application/json"}
    conn.close()



@server.route('/apple_login', methods=['post'])
def Projectlist6():
    '''
        http://127.0.0.1:5000/apple_login?appleID=123123&name=lily&email=789@qq.com&Acode=963258&token=wqeq&RUS=2
    http://120.48.49.157:5000/apple_login?appleID=123123&name=lily&email=789@qq.com&Acode=963258&token=wqeq&RUS=2
    '''
    appleID = request.values.get('appleID')
    name = request.values.get('name')
    email = request.values.get('email')
    Acode = request.values.get('Acode')
    token = request.values.get('token')
    RUS = int(request.values.get('RUS'))
    try:
        if appleID == None :
            project = {
               "code": "False",
               "msg": 'appleID不能为空！',
               "result":{
                }
            }
            response = json.dumps(project)  # 将python的字典转换为json字符串
            return response,401,{"Content-Type":"application/json"}
        
        else:
            db = pymysql.connect(host=HOST, port=3306,user='root',password='root123321',charset='utf8mb4' ,database='USER') #连接数据库
            cursor = db.cursor()
            sql = "select Apple_ID from apple_user" 
            cursor.execute(sql)
            rest=cursor.fetchall()
            # cursor.close()  
            # db.close()
            aid = (appleID,)
            if aid in rest:
                sql = "select * from apple_user where Apple_ID = '{}'".format(appleID)
                cursor.execute(sql)
                one_rest=cursor.fetchone()
                if one_rest[8]==1:
                    project = {
                       "code": "OK",
                       "msg": 'apple账号登录',
                       "result":{
                         "user": {
                             "app_ID" :one_rest[0],
                             "appleID" : one_rest[1],
                             "Real_Name":one_rest[2],
                             "name" : one_rest[3],
                             "email" : one_rest[4],
                             "Acode" : one_rest[5],
                             "token" : one_rest[6],
                             "RUS" : one_rest[7],
                             "SEX":one_rest[8],
                             "Status":one_rest[9]
                             }
                        }
                    }
                    response = json.dumps(project)  # 将python的字典转换为json字符串
                    return response,200,{"Content-Type":"application/json"}
                elif one_rest[8]==0:
                    project = {
                       "code": "False",
                       "msg": '账号已注销',
                       "result":{
                         "appleID":appleID
                        }
                    }
                    response = json.dumps(project)  # 将python的字典转换为json字符串
                    return response,402,{"Content-Type":"application/json"}
                else:
                    project = {
                       "code": "False",
                       "msg": '登录错误',
                       "result":{
                         "appleID":appleID
                        }
                    }
                    response = json.dumps(project)  # 将python的字典转换为json字符串
                    return response,403,{"Content-Type":"application/json"}
                
            else:
                token = token.replace("\"","'")
                app_ID = shortuuid.uuid()
                n_name = get_username()
                sql =  """INSERT INTO apple_user (User_ID,Apple_ID,Real_Name,Name,Email,A_Code,Token,RUS,SEX,Status)
                         VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")""".format(app_ID,appleID,name,n_name,email,Acode,token,RUS,1,1)
                try:
                    # 执行sql语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    db.commit()
                    project = {
                       "code": "OK",
                       "msg": '新账号注册',
                       "result":{
                         "app_ID" :app_ID,
                         "appleID" : appleID,
                         "Real_Name":name,
                         "name" : n_name,
                         "email" : email,
                         "Acode" : Acode,
                         "token" : token,
                         "RUS" : RUS,
                         "SEX":1,
                         "Status":1
                        }
                    }
                    response = json.dumps(project)  # 将python的字典转换为json字符串
                    return response,200,{"Content-Type":"application/json"}
                except Exception as e:
                    # 如果发生错误则回滚
                    db.rollback()
                    project = {
                       "code": "False",
                       "msg": '错误！',
                       "result":{
                        "Error": str(e)
                        }
                    }
                    response = json.dumps(project)  # 将python的字典转换为json字符串
                    return response,404,{"Content-Type":"application/json"}
            cursor.close()  
            db.close()
    except Exception as e:
        print(e)
        project = {
           "code": "False",
           "msg": "no message",
           "result":str(e)
        }
        response = json.dumps(project)  # 将python的字典转换为json字符串
        return response,405,{"Content-Type":"application/json"}
        


@server.route('/quick_login', methods=['post'])#'get',
def Projectlist5():
    '''
        http://127.0.0.1:5000/quick_login?number=15915278761
    http://120.48.49.157:5000/quick_login?number=15915278761
    :return:
    '''
    num = request.values.get('number')
    # password = request.values.get('password')
    try:
        if num == None :
            project = {
               "code": "False",
               "msg": '账号不能为空！',
               "result":{
                   
            
                }
            }
            response = json.dumps(project)  # 将python的字典转换为json字符串
            return response,400,{"Content-Type":"application/json"}
        else:
            result1 = Pattern1.match(num)
            if result1:
                db = pymysql.connect(
                    host=HOST, 
                    # host="127.0.0.1", 
                    port=3306,
                    user='root',    #在这里输入用户名
                    password='root123321',     #在这里输入密码
                    charset='utf8mb4' ,
                    database='USER'
                    ) #连接数据库
                # 使用 cursor() 方法创建一个游标对象 cursor
                cursor = db.cursor()
                # SQL 查询语句，查询user表
                sql = "select Phone_number from personal_information" 
                # sql = "select * from user where name = '李四'"
                cursor.execute(sql)
                #这是查询表中所有的数据
                rest=cursor.fetchall()
                # cursor.close()  
                # db.close()
                # print(num, "手机号符合要求.")
                yuan = (num,)
                if yuan in rest:
                    sql = "select * from personal_information where phone_number = '{}'".format(num)
                    cursor.execute(sql)
                    one_rest=cursor.fetchone()
                    # print(one_rest)
                    # if password == one_rest[7] and one_rest[8]==1:
                    
                    if one_rest[8]==0:
                        project = {
                           "code": "False",
                           "msg": '账号已注销',
                           "result":{
                             "phone_number":num
                            }
                        }
                        response = json.dumps(project)  # 将python的字典转换为json字符串
                        return response,401,{"Content-Type":"application/json"}
                        
                    
                    project = {
                       "code": "OK",
                       "msg": '账号登录',
                       "result":{
                         "user": {
                             "app_ID" :one_rest[0],
                             "HS_url":one_rest[1],
                             "real_name":one_rest[2],
                             "ID_Number":one_rest[3],
                             "nick_name":one_rest[4],
                             "SEX":one_rest[5],
                             "Phone_number":one_rest[6],
                             # "password":one_rest[7],
                             "Status":one_rest[8]
                             }
                        }
                    }
                    response = json.dumps(project)  # 将python的字典转换为json字符串
                    return response,200,{"Content-Type":"application/json"}
                    
                else:
                    project = {
                       "code": "False",
                       "msg": '账号未注册',
                       "result":{
                         "phone_number":num
                        }
                    }
                    response = json.dumps(project)  # 将python的字典转换为json字符串
                    return response,402,{"Content-Type":"application/json"}
                cursor.close()  
                db.close()
            else:
                # print(num, "手机号不符合要求.")
                project = {
                   "code": "False",
                   "msg": '手机号不符合要求！',
                   "result":{
                    }
                }
                response = json.dumps(project)  # 将python的字典转换为json字符串
                return response,403,{"Content-Type":"application/json"}
    except Exception as e:
        print(e)
        project = {
           "code": "False",
           "msg": "no message",
           "result":str(e)
        }
        response = json.dumps(project)  # 将python的字典转换为json字符串
        return response,404,{"Content-Type":"application/json"}





@server.route('/login', methods=['post'])#'get',
def Projectlist4():
    '''
        http://127.0.0.1:5000/login?number=15915278761&password=AA123456
    http://120.48.49.157:5000/login?number=15915278761&password=AA123456
    :return:
    '''
    num = request.values.get('number')
    password = request.values.get('password')
    try:
        if num == None or password == None:
            project = {
               "code": "False",
               "msg": '账号密码不能为空！',
               "result":{
                   
            
                }
            }
            response = json.dumps(project)  # 将python的字典转换为json字符串
            return response,400,{"Content-Type":"application/json"}
        else:
            result1 = Pattern1.match(num)
            if result1:
                db = pymysql.connect(
                    host=HOST, 
                    # host="127.0.0.1", 
                    port=3306,
                    user='root',    #在这里输入用户名
                    password='root123321',     #在这里输入密码
                    charset='utf8mb4' ,
                    database='USER'
                    ) #连接数据库
                # 使用 cursor() 方法创建一个游标对象 cursor
                cursor = db.cursor()
                # SQL 查询语句，查询user表
                sql = "select Phone_number from personal_information" 
                # sql = "select * from user where name = '李四'"
                cursor.execute(sql)
                #这是查询表中所有的数据
                rest=cursor.fetchall()
                # cursor.close()  
                # db.close()
                # print(num, "手机号符合要求.")
                yuan = (num,)
                if yuan in rest:
                    sql = "select * from personal_information where phone_number = '{}'".format(num)
                    cursor.execute(sql)
                    one_rest=cursor.fetchone()
                    # print(one_rest)
                    if password == one_rest[7] and one_rest[8]==1:
                        
                        project = {
                           "code": "OK",
                           "msg": '账号登录',
                           "result":{
                             "user": {
                                 "app_ID" :one_rest[0],
                                 "HS_url":one_rest[1],
                                 "real_name":one_rest[2],
                                 "ID_Number":one_rest[3],
                                 "nick_name":one_rest[4],
                                 "SEX":one_rest[5],
                                 "Phone_number":one_rest[6],
                                 # "password":one_rest[7],
                                 "Status":one_rest[8]
                                 }
                            }
                        }
                        response = json.dumps(project)  # 将python的字典转换为json字符串
                        return response,200,{"Content-Type":"application/json"}
                    elif one_rest[8]==0:
                        project = {
                           "code": "False",
                           "msg": '账号已注销',
                           "result":{
                             "phone_number":num
                            }
                        }
                        response = json.dumps(project)  # 将python的字典转换为json字符串
                        return response,401,{"Content-Type":"application/json"}
                    else:
                        project = {
                           "code": "False",
                           "msg": '账号密码错误',
                           "result":{
                             "phone_number":num
                            }
                        }
                        response = json.dumps(project)  # 将python的字典转换为json字符串
                        return response,402,{"Content-Type":"application/json"}
                    
                else:
                    project = {
                       "code": "False",
                       "msg": '账号未注册',
                       "result":{
                         "phone_number":num
                        }
                    }
                    response = json.dumps(project)  # 将python的字典转换为json字符串
                    return response,403,{"Content-Type":"application/json"}
                cursor.close()  
                db.close()
            else:
                # print(num, "手机号不符合要求.")
                project = {
                   "code": "False",
                   "msg": '手机号不符合要求！',
                   "result":{
                    }
                }
                response = json.dumps(project)  # 将python的字典转换为json字符串
                return response,404,{"Content-Type":"application/json"}
    except Exception as e:
        print(e)
        project = {
           "code": "False",
           "msg": "no message",
           "result":str(e)
        }
        response = json.dumps(project)  # 将python的字典转换为json字符串
        return response,405,{"Content-Type":"application/json"}




@server.route('/register', methods=['post'])#'get',
def Projectlist3():
    '''
        http://127.0.0.1:5000/register?number=15915278761&password=AA123456
    http://120.48.49.157:5000/register?number=15915278761&password=AA123456
    :return:
    '''
    num = request.values.get('number')
    try:
        if num == None:
            project = {
               "code": "False",
               "msg": '手机号不能为空！',
               "result":{
            
                }
            }
            response = json.dumps(project)  # 将python的字典转换为json字符串
            return response,400,{"Content-Type":"application/json"}
        else:
            result1 = Pattern1.match(num)
            if result1:
                password = request.values.get('password')
                # captcha = request.values.get('captcha')
                
                app_ID = shortuuid.uuid()
                project = {
                   "code": "OK",
                   "msg": '账号注册',
                   "result":{
                    "user": {
                        "app_ID" :app_ID,
                        "HS_url":'',
                        "real_name":'',
                        "ID_Number":0,
                        "nick_name":'user_'+num,
                        "SEX":1,
                        "Phone_number":num,
                        "password":password,
                        "Status":1,
                        }
                    }
                }
                db = pymysql.connect(
                    host=HOST, 
                    # host="127.0.0.1", 
                    port=3306,
                    user='root',    #在这里输入用户名
                    password='root123321',     #在这里输入密码
                    charset='utf8mb4' ,
                    database='USER'
                    ) #连接数据库
                U = project['result']['user']
                cursor = db.cursor()
                sql =  """INSERT INTO personal_information (app_ID,HS_url,real_name,ID_Number,nick_name,SEX,Phone_number,password,Status)
                         VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}")""".format(U["app_ID"],U["HS_url"],U["real_name"],U["ID_Number"],U["nick_name"],
                         U["SEX"],U["Phone_number"],U["password"],U["Status"])
                try:
                    # 执行sql语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    db.commit()
                except Exception as e:
                    # 如果发生错误则回滚
                    db.rollback()
                    project = {
                       "code": "False",
                       "msg": '错误！',
                       "result":{
                        "Error": str(e)
                        }
                    }
                    response = json.dumps(project)  # 将python的字典转换为json字符串
                    return response,401,{"Content-Type":"application/json"}
                    
                   
                cursor.close()  
                db.close()
                
                
                
                response = json.dumps(project)  # 将python的字典转换为json字符串
                return response,200,{"Content-Type":"application/json"}
            else:
                # print(num, "手机号不符合要求.")
                project = {
                   "code": "False",
                   "msg": '手机号不符合要求！',
                   "result":{
                    }
                }
                response = json.dumps(project)  # 将python的字典转换为json字符串
                return response,402,{"Content-Type":"application/json"}
    except Exception as e:
        print(e)
        project = {
           "code": "False",
           "msg": "no message",
           "result":str(e)
        }
        response = json.dumps(project)  # 将python的字典转换为json字符串
        return response,403,{"Content-Type":"application/json"}
    
    


@server.route('/search/phone', methods=['get'])#'get',
def Projectlist1():
    
    '''
        http://127.0.0.1:5000/search/phone?number=15915278761
    http://120.48.49.157:5000/search/phone?number=15915278761
    '''
    num = request.values.get('number')
    # name= request.values.get('name')
    try:
        if num == None:
            project = {
               "code": "False",
               "msg": '手机号不能为空！',
               "result":{
                }
            }
            response = json.dumps(project)  # 将python的字典转换为json字符串
            return response,400,{"Content-Type":"application/json"}
        
        # Pattern1 = re.compile(r'^1[34578]\d{9}$')
        else:
            result1 = Pattern1.match(num)
            if result1:
                db = pymysql.connect(
                    host=HOST, 
                    # host="127.0.0.1", 
                    port=3306,
                    user='root',    #在这里输入用户名
                    password='root123321',     #在这里输入密码
                    charset='utf8mb4' ,
                    database='USER'
                    ) #连接数据库
                # 使用 cursor() 方法创建一个游标对象 cursor
                cursor = db.cursor()
                # SQL 查询语句，查询user表
                sql = "select Phone_number from personal_information" 
                # sql = "select * from user where name = '李四'"
                cursor.execute(sql)
                #这是查询表中所有的数据
                rest=cursor.fetchall()
                cursor.close()  
                db.close()
                # print(num, "手机号符合要求.")
                yuan = (num,)
                if yuan in rest:
                    boo = True
                    jie = '账号已存在'
                    # print('存在')
                else:
                    boo = False
                    jie = '新账号'
        
                project = {
                   "code": "OK",
                   "msg": jie,
                   "result":{
                     "register":boo
                    }
                }
                response = json.dumps(project)  # 将python的字典转换为json字符串
                return response,200,{"Content-Type":"application/json"}
            else:
                # print(num, "手机号不符合要求.")
                project = {
                   "code": "False",
                   "msg": '手机号不符合要求！',
                   "result":{
                    }
                }
                response = json.dumps(project)  # 将python的字典转换为json字符串
                return response,401,{"Content-Type":"application/json"}
    except Exception as e:
        print(e)
        project = {
           "code": "False",
           "msg": "no message",
           "result":str(e)
        }
        response = json.dumps(project)  # 将python的字典转换为json字符串
        return response,402,{"Content-Type":"application/json"}
    
    
@server.route('/topic_today', methods=['get'])#'get',
def G_topic_today():
    '''
        http://127.0.0.1:5000/topic_today?page=1&userID=3FtPAHrhhveJGNzC5FaBWv
    http://120.48.49.157:5000/topic_today?page=1&userID=3FtPAHrhhveJGNzC5FaBWv
    '''
    page = int(request.values.get('page'))
    userID = request.values.get('userID')
    try:
        if userID !='':
            # print(userID)
            like_news,like_talk = get_like(userID)
            
            
        # from sqlalchemy import create_engine
        # 使用pymysql驱动连接到mysql
        # engine = create_engine('mysql+pymysql://user:pwd@localhost/testdb')
        db = pymysql.connect(
            host=HOST, 
            port=3306,
            user='root',    #在这里输入用户名
            password='root123321',     #在这里输入密码
            charset='utf8mb4' ,
            database='GOOGLE'
            ) #连接数据库
        # 使用 cursor() 方法创建一个游标对象 cursor
        # cursor = db.cursor()
        # SQL 查询语句，查询user表
        # sql = "select THEME,GPT3_TITLE,KEY_WORD from GL_NEWS" 
        df = pd.read_sql("select THEME,GPT3_TITLE,KEY_WORD,S_TIME,TIME,TH_ID,TH_ZH,GT_ZH,KW_ZH from GL_NEWS" , db)
        db.close()
        df = df.sort_values('S_TIME', ascending=False).drop_duplicates('THEME')#.sort_index()
        # print(df)
        
        page_size = 5  # 每页条数
        total_items = df.shape[0]  # 总条数
        total_pages = (total_items + page_size - 1) // page_size  # 总页数
    
        # for page in range(1, total_pages + 1):
        if page <= total_pages:
            start_item = (page - 1) * page_size
            end_item = min(page * page_size, total_items)-1
            print(f"Page {page}: {start_item}-{end_item}")
            df = df.iloc[start_item:end_item+1]
        
            news_list = []
            for index, row in df.iterrows():
                like_sum = get_act(row['TH_ID'],'news')
                discuss_sum = get_act(row['TH_ID'],'discuss')
                
                like = False
                if row['TH_ID'] in like_talk:
                    like=True
                b = row['THEME'].replace('Google News -','').replace('- Overview','')
                c = row['TH_ZH'].replace('谷歌新闻-','').replace('-概述','')
                # st = get_max_time(b)
                news = {
                    "theme":b,
                    "sum_title":row['GPT3_TITLE'],
                    "Key_word":row['KEY_WORD'],
                    "S_time":row['S_TIME'],
                    "TIME":row['TIME'],
                    "NEWS_ID":row['TH_ID'],
                    "TH_ZH":c,
                    "GT_ZH":row['GT_ZH'],
                    "KW_ZH":row['KW_ZH'],
                    "like":like,
                    "like_sum":like_sum,
                    "discuss_sum":discuss_sum,
                    "share_sum":0,
                    "dislike_sum":0
                    }
                if news not in news_list:
                    news_list.append(news)
                # print(b,r[1])
                # print('-----------')
            # print(news_list)
            # print(len(news_list))
            # cursor.close()  
            project = {
               "code": "OK",
               "msg": "谷歌新闻主题",
               "result":news_list
            }
            response = json.dumps(project)  # 将python的字典转换为json字符串
            return response,200,{"Content-Type":"application/json"}
        else:
            print('超出页数')
            project = {
               "code": "False",
               "msg": "no message"
            }
            response = json.dumps(project)  # 将python的字典转换为json字符串
            return response,400,{"Content-Type":"application/json"}
    except Exception as e:
        print(e)
        project = {
           "code": "False",
           "msg": "no message",
           "result":str(e)
        }
        response = json.dumps(project)  # 将python的字典转换为json字符串
        return response,401,{"Content-Type":"application/json"}

@server.route('/news_list', methods=['get'])#'get',
def G_news_lists():
    '''
        http://127.0.0.1:5000/news_list?word= uranium, Ukraine &li=1&userID=3FtPAHrhhveJGNzC5FaBWv
    http://120.48.49.157:5000/news_list?word= uranium, Ukraine &li=1&userID=3FtPAHrhhveJGNzC5FaBWv
    '''
    word = request.values.get('word')
    li = int(request.values.get('li'))
    userID = request.values.get('userID')
    print(word)
    try:
        if userID !='':
            # print(userID)
            like_news,like_talk = get_like(userID)
        
        db = pymysql.connect(
            host=HOST, 
            port=3306,
            user='root',    #在这里输入用户名
            password='root123321',     #在这里输入密码
            charset='utf8mb4' ,
            database='GOOGLE'
            ) #连接数据库
        
        sql = '''select GPT3_TEXT,TIME,KEY_WORD,S_TIME,TITLE,NEWS_ID,ZH_CN,T_ZH,KW_ZH from GL_NEWS WHERE THEME like "%{}%"  '''.format(word)
        df = pd.read_sql(sql , db)
        db.close()
        df = df.sort_values('S_TIME', ascending=False)#.drop_duplicates('THEME').sort_index()
        
        
        
        page_size = 5  # 每页条数
        total_items = df.shape[0]  # 总条数
        total_pages = (total_items + page_size - 1) // page_size  # 总页数
        # print(b,r[1])
        # print('-----------')
        # print(news_list)
        # print(len(news_list))
        # cursor.close()  
        # db.close()
        if li <= total_pages:
            start_item = (li - 1) * page_size
            end_item = min(li * page_size, total_items)-1
            print(f"Page {li}: {start_item}-{end_item}")
            df = df.iloc[start_item:end_item+1]
            
            
            news_list = []
            for index, row in df.iterrows():
                like = False
                if row['NEWS_ID'] in like_news:
                    like=True
                # b = row['THEME'].replace('Google News -','').replace('- Overview','')
                # st = get_max_time(b)
                like_sum = get_act(row['NEWS_ID'],'news')
                discuss_sum = get_act(row['NEWS_ID'],'discuss')
                news = {
                    "news":row['GPT3_TEXT'],
                    "Z_time":row['TIME'],
                    "Key_word":row['KEY_WORD'],
                    "Title":row['TITLE'],
                    "NEWS_ID":row['NEWS_ID'],
                    "ZH_CN":row['ZH_CN'],
                    "T_ZH":row['T_ZH'],
                    "KW_ZH":row['KW_ZH'],
                    "like":like,
                    "like_sum":like_sum,
                    "discuss_sum":discuss_sum,
                    "share_sum":0,
                    "dislike_sum":0
                    }
                if news not in news_list:
                    news_list.append(news)
            
            try:       
                project = {
                   "code": "OK",
                   "msg": "谷歌新闻列表",
                   "result":news_list
                }
                response = json.dumps(project)  # 将python的字典转换为json字符串
                return response,200,{"Content-Type":"application/json"}
            except Exception as e:
                print(e)
                project = {
                   "code": "False",
                   "msg": "谷歌新闻列表",
                   "result":"no message"
                }
                response = json.dumps(project)  # 将python的字典转换为json字符串
                return response,400,{"Content-Type":"application/json"}
        else:
            print('超出页数')
            project = {
               "code": "False",
               "msg": "no message"
            }
            response = json.dumps(project)  # 将python的字典转换为json字符串
            return response,401,{"Content-Type":"application/json"}
    except Exception as e:
        print(e)
        project = {
           "code": "False",
           "msg": "no message",
           "result":str(e)
        }
        response = json.dumps(project)  # 将python的字典转换为json字符串
        return response,402,{"Content-Type":"application/json"}


@server.route('/twitter', methods=['get'])#'get',
def G_twitter():
    '''
        http://127.0.0.1:5000/twitter?word= Diablo 4's early access beta 
    http://120.48.49.157:5000/twitter?word= Diablo 4's early access beta 
    '''
    word = request.values.get('word')
    print(word)
    try:
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
        sql = '''select PEOPLE,PINGL,TIME,ZH_CN,P_ZH from Twitter WHERE CLASS like "%{}%"  '''.format(word)
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
                "ZH_CN":r[3],
                "Z_time":r[2],
                "ZH_Name":r[4]
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
               "msg": "no message"
            }
            response = json.dumps(project)  # 将python的字典转换为json字符串
            return response,400,{"Content-Type":"application/json"}
    except Exception as e:
        print(e)
        project = {
           "code": "False",
           "msg": "no message",
           "result":str(e)
        }
        response = json.dumps(project)  # 将python的字典转换为json字符串
        return response,401,{"Content-Type":"application/json"}
        

if __name__ == "__main__":
    server.run()

    # server.run(host="192.168.0.4", port=5000, debug=True)
    #server.run(host="192.168.0.4", port=5000, debug=True,ssl_context=('server.crt','server.key'))