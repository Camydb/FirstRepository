# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 17:36:33 2023

@author: Administrator
"""
import pymysql
import flask,json
from flask import request,send_file,make_response#jsonify
import shortuuid
import re
import random
import pandas as pd
import string
import time
from datetime import datetime
import urllib.parse
import os

# from sqlalchemy import create_engine
'''
flask： web框架，通过flask提供的装饰器@server.route()将普通函数转换为服务
pip3 install flask -i https://pypi.doubanio.com/simple
'''
# 创建一个服务，把当前这个python文件当做一个服务
server = flask.Flask(__name__)

Pattern1 = re.compile(r'^1[34578]\d{9}$')


# HOST="120.48.49.157"
HOST="127.0.0.1"

# server.config['JSON_AS_ASCII'] = False
# @server.route()可以将普通函数转变为服务 的路径、请求方式

def get_share(newsID):
    db = pymysql.connect(
        host=HOST, 
        port=3306,
        user='root',    #在这里输入用户名
        password='root123321',     #在这里输入密码
        charset='utf8mb4' ,
        database='USER'
        ) #连接数据库

    df = pd.read_sql('''SELECT user_ID,news_ID,share_ID FROM user_share WHERE news_ID= "{}"  '''.format(newsID), db) #收藏的新闻，话题，评论
    db.close()
    df = df.drop_duplicates('share_ID')#.sort_index()
    return(len(df))



def get_top():
    # 获取当前时间戳
    now = time.time()
    db = pymysql.connect(
        host=HOST, 
        port=3306,
        user='root',    #在这里输入用户名
        password='root123321',     #在这里输入密码
        charset='utf8mb4' ,
        database='GOOGLE'
        ) #连接数据库
    # db = create_engine('mysql+pymysql://root:root123321@{}:3306/GOOGLE'.format(HOST))
    # 查询数据
    # df = pd.read_sql_query('SELECT * FROM table_name', engine)

    df = pd.read_sql('''SELECT TH_ID,TIME,S_TIME FROM GL_NEWS  ''',db)
    db.close()
    three_days_ago = int(now - (1 * 24 * 60 * 60 + 8 * 60 * 60))
    df['S_TIME'] = pd.to_numeric(df['S_TIME'], errors='coerce')
    df1 = df[df['S_TIME'] >= three_days_ago]
    counts = df1['TH_ID'].value_counts()
    top = counts.head().index.tolist()
    my_list = list(counts.iloc[5:].index.tolist())
    random.shuffle(my_list)
    
    df2 = df[df['S_TIME'] < three_days_ago]
    # my_list2 = list(df2['TH_ID'])
    my_list2 = list(set(list(df2['TH_ID'])))
    random.shuffle(my_list2)
    return(top+my_list+my_list2)

def get_now_time():
    SAVE_TIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date1 = datetime.strptime(str(SAVE_TIME), "%Y-%m-%d %H:%M:%S")
    s_t=time.strptime(str(date1),"%Y-%m-%d %H:%M:%S")
    S_TIME=int(time.mktime(s_t))
    return(SAVE_TIME,S_TIME)

def get_dislike(userID):
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
    df = pd.read_sql('''SELECT discuss_ID,class_n FROM user_dislike WHERE user_ID= "{}"  '''.format(userID), db)
    # '''select PEOPLE,PINGL,TIME,ZH_CN from Twitter WHERE CLASS like "%{}%"  '''.format(word)
    # 关闭连接
    db.close()
    # ((df.loc[df['class_n'] == 'news'])['news_ID'])
    return(tuple((df.loc[df['class_n'] == 'news'])['discuss_ID']),tuple((df.loc[df['class_n'] == 'talk'])['discuss_ID']),tuple((df.loc[df['class_n'] == 'discuss'])['discuss_ID']))


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
    
    
    
    return(tuple((df.loc[df['class_n'] == 'news'])['news_ID']),tuple((df.loc[df['class_n'] == 'talk'])['news_ID']),tuple((df.loc[df['class_n'] == 'discuss'])['news_ID']))

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
    if class_n == 'news' or class_n == 'talk' or class_n == 'like_discuss':
        df = pd.read_sql('''SELECT user_ID,class_n FROM user_like WHERE news_ID= "{}"  '''.format(search_id), db) #收藏的新闻，话题，评论
        db.close()
        df = df.drop_duplicates('user_ID')#.sort_index()
        return(len(df))
    
    elif class_n == 'discuss':
        df = pd.read_sql('''SELECT user_ID,discuss_ID,class_n FROM user_discuss WHERE news_ID= "{}"  '''.format(search_id), db)
        db.close()
        df = df.drop_duplicates('discuss_ID')#.sort_index()
        return(len(df))
    
    elif class_n == 'dislike':
        df = pd.read_sql('''SELECT user_ID,discuss_ID,class_n FROM user_dislike WHERE discuss_ID= "{}"  '''.format(search_id), db)
        db.close()
        df = df.drop_duplicates('user_ID')#.sort_index()
        return(len(df))
    
    else:
        print('False')
        db.close()
        return 0

@server.route('/chuan', methods=['get'])
def chuan():
    '''
        http://127.0.0.1:5000/chuan?name=safsafsdfsdfsd.png
    http://120.48.49.157:5000/chuan?name=safsafsdfsdfsd.png
    '''
    name = request.values.get('name')
    print(name)
    try:
        file = request.files['file']
        path = '/root/img/{}'.format(name)
        file.save(path)  # 保存上传的文件到指定路径
        print("上传成功")
        project = {
           "code": "OK",
           "msg": "上传成功"
        }
        response = json.dumps(project)  # 将python的字典转换为json字符串
        return response,200,{"Content-Type":"application/json"}
    except Exception as e:
        print(e)
        print("上传失败")
        project = {
           "code": "False",
           "msg": "上传失败",
           "result":str(e)
        }
        response = json.dumps(project)  # 将python的字典转换为json字符串
        return response,400,{"Content-Type":"application/json"}



@server.route('/images/<name>')
def get_image(name):
    """
    Endpoint to retrieve an image by name
    """
    image_path = os.path.join("/root/img", name)
    if os.path.isfile(image_path):
        return send_file(image_path, mimetype='image/png')
    else:
        # return jsonify({"error": "Image not found"}), 404
        project = {
           "code": "False",
           "msg": "no message",
           "result":"Image not found"
        }
        response = json.dumps(project)  # 将python的字典转换为json字符串
        return response,400,{"Content-Type":"application/json"}


@server.route('/context', methods=['get'])
def context():
    '''
        http://127.0.0.1:5000/context?TH_ID=3wPcRUB6R
    http://120.48.49.157:5000/context?TH_ID=3wPcRUB6R
    '''
    TH_ID = request.values.get('TH_ID')
    try:
        # save_time,stime = get_now_time()
        conn = pymysql.connect(
            host=HOST, 
            port=3306,
            user='root',    #在这里输入用户名
            password='root123321',     #在这里输入密码
            charset='utf8mb4' ,
            database='GOOGLE'
            ) #连接数据库
        cur = conn.cursor()
        
        cur.execute('SELECT context,THEME,KEY_WORD,context_ZH,TH_ZH,KW_ZH FROM GL_NEWS WHERE TH_ID = "{}" '.format(TH_ID))
        rows = cur.fetchall()
        # for row in rows:
        #     if row[0] == userID:
        #         path = row[1]
        #         nick_name = urllib.parse.quote(row[2])
        
        if rows[0][0] is None:
            ct = ''
            ct_zh = ''
        else:
            ct = rows[0][0]
            ct_zh = rows[0][3]

        
        conn.close()
        
        project = {
           "code": "OK",
           "msg": 'context',
           "result":{
               "newsID":TH_ID,
               "context":ct,
               "context_ZH":ct_zh,
               "Key_word":rows[0][2],
               "KW_ZH":rows[0][5],
               "like":False,
               "dislike":False,
               "like_sum":0,
               "discuss_sum":0,
               "share_sum":0,
               "dislike_sum":0,
               "share":{
                   "title":rows[0][1],
                   "title_ZH":rows[0][4],
                   "content":ct,
                   "context_ZH":ct_zh,
                   "url":"https://www.newzsup.com/"
                   }
           
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


@server.route('/share', methods=['get'])
def share():
    '''
        http://127.0.0.1:5000/share?userID=fhLgcu7A6RvxkW3sFmN936&newsID=VzLtzi4B8YDFk2SPw37h8s
    http://120.48.49.157:5000/share?userID=fhLgcu7A6RvxkW3sFmN936&newsID=VzLtzi4B8YDFk2SPw37h8s
    '''
    userID = request.values.get('userID')
    newsID = request.values.get('newsID')
    try:
        save_time,stime = get_now_time()
        conn = pymysql.connect(
            host=HOST, 
            port=3306,
            user='root',    #在这里输入用户名
            password='root123321',     #在这里输入密码
            charset='utf8mb4' ,
            database='USER'
            ) #连接数据库
        cur = conn.cursor()
        
        
        share_ID = shortuuid.ShortUUID().random(length=7)
        cur.execute(
            '''INSERT INTO user_share (user_ID,news_ID,share_ID,time,stime) 
            VALUES ("{}","{}","{}","{}","{}")'''.format(userID,newsID,share_ID,save_time,stime));
        # sql = '''delete from user_discuss where user_ID="{}" and discuss_ID="{}" '''.format(userID,discussID)
        # cur.execute(sql)
        conn.commit()
        conn.close()
        
        project = {
           "code": "OK",
           "msg": '分享成功',
           "result":{
               "userID":userID,
               "newsID":newsID
           
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
    
@server.route('/personal', methods=['GET'])
def get_personal():
    '''
        http://127.0.0.1:5000/personal?userID=Lw7CH4upxDy7tzDS9XChsg
    http://120.48.49.157:5000/personal?userID=Lw7CH4upxDy7tzDS9XChsg
    '''
    userID = request.values.get('userID')
    # get image
    # img_path = 'D:/image/aa.jpg'
    conn = pymysql.connect(
        host=HOST, 
        port=3306,
        user='root',    #在这里输入用户名
        password='root123321',     #在这里输入密码
        charset='utf8mb4' ,
        database='USER'
        ) #连接数据库
    cur = conn.cursor()
    
    path = ''
    nick_name = ''
    
    
    cur.execute('SELECT app_ID,HS_url,nick_name FROM personal_information')
    rows = cur.fetchall()
    for row in rows:
        if row[0] == userID:
            path = row[1]
            nick_name = urllib.parse.quote(row[2])
            
    cur.execute('SELECT User_ID,HS_url,Name FROM apple_user')
    rows = cur.fetchall()
    for row in rows:
        if row[0] == userID:
            path = row[1]
            nick_name = urllib.parse.quote(row[2])
    conn.close()
    

    
    if path !='':
        # path = 'D:/image/file1.png'
        img = send_file(path, mimetype='image/gif')
        # img = send_file('D:/image/aa.jpg', mimetype='image/gif')
        # get data
        data = {
            'user_name': nick_name,
            'userID': userID
        }
        # json_data = jsonify(data)
        # create response object
        response = make_response(img)
        # response.set_cookie('mycookie', 'myvalue')
        # response.set_data(json_data.data)
        response.headers['result'] = data
        return response
    else:
        # path = 'D:/image/aa.jpg'
        img = send_file('/root/h_imgs/user.png', mimetype='image/gif')
        # img = send_file('D:/image/aa.jpg', mimetype='image/gif')
        # get data
        data = {
            'user_name': nick_name,
            'userID': userID
        }
        # json_data = jsonify(data)
        # create response object
        response = make_response(img)
        # response.set_cookie('mycookie', 'myvalue')
        # response.set_data(json_data.data)
        response.headers['result'] = data
        return response



@server.route('/version', methods=['get'])
def version():
    '''
        http://127.0.0.1:5000/version
    http://120.48.49.157:5000/version
    '''
    project = {
       "code": "OK",
       "msg": 'OK',
       "result":{
        "version": "1.0.1",
        "Update_content":'',
        "ZH_text":'',
        "Force_updates":False
        }
    }
    response = json.dumps(project)  # 将python的字典转换为json字符串
    return response,200,{"Content-Type":"application/json"}

@server.route('/change_user_info', methods=['POST'])
def change_user_info():
    '''
        http://127.0.0.1:5000/change_user_info?userID=adasdsad&user_name=sdfdfsd
    http://120.48.49.157:5000/change_user_info?userID=adasdsad&user_name=sdfdfsd
    '''
    save_time,stime = get_now_time()
    # path_list = []
    # try:
    #     files = request.files.getlist('file')
    #     for file in files:
    #         path = '/root/images/{}_{}.png'.format(stime, files.index(file))
    #         file.save(path) 
    #         path_list.append(path)
    # except Exception as e:
    #     print(e)
    #     print("上传失败")
    # print("上传成功")

    
    try:
        file = request.files['file']
        path = '/root/h_imgs/{}.png'.format(stime)
        file.save(path)  # 保存上传的文件到指定路径
    except Exception as e:
        path = ''
        print(e)
    # question = request.form.get('question')
    # question = request.files['question']
    user_name = request.values.get('user_name')
    userID = request.values.get('userID')
    # save_time,stime = get_now_time()
    print(user_name)
    print(userID)
    
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
        # path,user_name,userID
        cur.execute('''UPDATE personal_information SET HS_url = "{}",nick_name = "{}"  WHERE app_ID = "{}" '''.format(path,user_name,userID))
        conn.commit()
        
        cur.execute('''UPDATE apple_user SET HS_url = "{}",Name = "{}"  WHERE User_ID = "{}" '''.format(path,user_name,userID))
        conn.commit()
        
        conn.close()
        print ("修改!")
        project = {
           "code": "OK",
           "msg": 'OK',
           "result":{
            "user_ID":userID,
           "user_name":user_name

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
    

@server.route('/revise', methods=['post'])
def Projectlist_15():
    '''
        http://127.0.0.1:5000/revise?phone_number=97878978&p_word=123455
    http://120.48.49.157:5000/revise?phone_number=79879879&p_word=123455
    '''
    phone_number = request.values.get('phone_number')
    p_word = request.values.get('p_word')
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
        # cur.execute('''UPDATE GL_NEWS SET ZH_CN = ? WHERE GPT3_TEXT = ?''', (value,key))
        sql =( ''' UPDATE personal_information SET password = "{}" WHERE Phone_number = "{}" '''.format(p_word,phone_number))
        cur.execute(sql)
        conn.commit()
        
        
        
        conn.close()
        
        project = {
           "code": "OK",
           "msg": '修改密码',
           "result":{
               "phone_number":phone_number
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


@server.route('/cancel', methods=['post'])
def Projectlist_14():
    '''
        http://127.0.0.1:5000/cancel?userID=97878978
    http://120.48.49.157:5000/cancel?userID=79879879
    '''
    userID = request.values.get('userID')
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
        
        sql = '''delete from user_discuss where user_ID="{}"  '''.format(userID)
        cur.execute(sql)
        conn.commit()
        
        sql = '''delete from user_dislike where user_ID="{}"  '''.format(userID)
        cur.execute(sql)
        conn.commit()
        
        sql = '''delete from user_like where user_ID="{}" '''.format(userID)
        cur.execute(sql)
        conn.commit()
        
        sql = '''delete from personal_information where app_ID="{}" '''.format(userID)
        cur.execute(sql)
        conn.commit()
        
        sql = '''delete from apple_user where User_ID="{}" '''.format(userID)
        cur.execute(sql)
        conn.commit()
        
        conn.close()
        
        project = {
           "code": "OK",
           "msg": '注销账号',
           "result":{
               "userID":userID
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

@server.route('/del_all', methods=['post'])
def Projectlist_13():
    '''
        http://127.0.0.1:5000/del_all?userID=97878978
    http://120.48.49.157:5000/del_all?userID=79879879
    '''
    userID = request.values.get('userID')
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
        
        sql = '''delete from user_discuss where user_ID="{}"  '''.format(userID)
        cur.execute(sql)
        conn.commit()
        
        sql = '''delete from user_dislike where user_ID="{}"  '''.format(userID)
        cur.execute(sql)
        conn.commit()
        
        sql = '''delete from user_like where user_ID="{}" '''.format(userID)
        cur.execute(sql)
        conn.commit()
        
        
        conn.close()
        
        project = {
           "code": "OK",
           "msg": '删除',
           "result":{
               "userID":userID
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


@server.route('/upload', methods=['POST'])
def upload():
    '''
        http://127.0.0.1:5000/upload?question=scscscscsc&userID=vdfvfdvfdv&class_n=context
    http://120.48.49.157:5000/upload?question=scscscscsc&userID=vdfvfdvfdv&class_n=context
    '''
    save_time,stime = get_now_time()
    path_list = []
    try:
        files = request.files.getlist('file')
        for file in files:
            path = '/root/images/{}_{}.png'.format(stime, files.index(file))
            file.save(path) 
            path_list.append(path)
    except Exception as e:
        print(e)
        print("上传失败")
    print("上传成功")

    
    # try:
    # file = request.files['file']
    # path = '/root/images/{}.png'.format(stime)
    # file.save(path)  # 保存上传的文件到指定路径
    # except Exception as e:
    #     path = ''
    #     print(e)
    # question = request.form.get('question')
    # question = request.files['question']
    question = request.values.get('question')
    userID = request.values.get('userID')
    class_n = request.values.get('class_n')
    # save_time,stime = get_now_time()
    
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
        
        f_back_ID = shortuuid.ShortUUID().random(length=6)
        cur.execute(
            '''INSERT INTO user_feedback (user_ID,f_back_ID,text,image,time,stime,class_n) 
            VALUES ("{}","{}","{}","{}","{}","{}","{}")'''.format(userID,f_back_ID,question,path_list,save_time,stime,class_n));
        conn.commit()
        print ("反馈成功!")
        project = {
           "code": "OK",
           "msg": 'OK',
           "result":{

            "user_ID":userID,
            "f_back_ID":f_back_ID,
            "question":question,
            "time":save_time

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
    


@server.route('/add_dislike', methods=['post'])
def Projectlist_12():
    '''
        http://127.0.0.1:5000/add_dislike?userID=2132&newsID=2312312&is_dislike=1&class_n=news
    http://120.48.49.157:5000/add_dislike?userID=2132&newsID=2312312&is_dislike=0&class_n=discuss
    '''
    userID = request.values.get('userID')
    newsID = request.values.get('newsID')
    is_dislike = int(request.values.get('is_dislike'))
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
        if is_dislike==1:
            try:
                cur.execute(
                    '''INSERT INTO user_dislike (user_ID,discuss_ID,class_n) VALUES ("{}","{}","{}")'''.format(userID,newsID,class_n));
                conn.commit()
                print ("记录插入成功!")
                project = {
                   "code": "OK",
                   "msg": 'news dislike',
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
        elif is_dislike==0:
            
            sql = '''delete from user_dislike where user_ID="{}" and discuss_ID="{}" '''.format(userID,newsID)
            cur.execute(sql)
            conn.commit()
            
            project = {
               "code": "OK",
               "msg": 'cancel dislike',
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
    if class_n == 'discuss':
        if is_dislike==1:
            try:
                cur.execute(
                    '''INSERT INTO user_dislike (user_ID,discuss_ID,class_n) VALUES ("{}","{}","{}")'''.format(userID,newsID,class_n));
                conn.commit()
                print ("记录插入成功!")
                project = {
                   "code": "OK",
                   "msg": 'discuss dislike',
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
                return response,403,{"Content-Type":"application/json"}
        elif is_dislike==0:
            
            sql = '''delete from user_dislike where user_ID="{}" and discuss_ID="{}" '''.format(userID,newsID)
            cur.execute(sql)
            conn.commit()
            
            project = {
               "code": "OK",
               "msg": 'cancel dislike',
               "result":{
                "userID":userID,
                "discussID":newsID
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
                "discussID":newsID
                }
            }
            response = json.dumps(project)  # 将python的字典转换为json字符串
            return response,404,{"Content-Type":"application/json"}
        
    if class_n == 'talk' or class_n == 'context':
        if is_dislike==1:
            try:
                cur.execute(
                    '''INSERT INTO user_dislike (user_ID,discuss_ID,class_n) VALUES ("{}","{}","{}")'''.format(userID,newsID,class_n));
                conn.commit()
                print ("记录插入成功!")
                project = {
                   "code": "OK",
                   "msg": 'talk dislike',
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
                return response,405,{"Content-Type":"application/json"}
        elif is_dislike==0:
            
            sql = '''delete from user_dislike where user_ID="{}" and discuss_ID="{}" and class_n="{}"'''.format(userID,newsID,class_n)
            cur.execute(sql)
            conn.commit()
            
            project = {
               "code": "OK",
               "msg": 'cancel dislike',
               "result":{
                "userID":userID,
                "discussID":newsID
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
                "discussID":newsID
                }
            }
            response = json.dumps(project)  # 将python的字典转换为json字符串
            return response,406,{"Content-Type":"application/json"}
    
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
    return response,407,{"Content-Type":"application/json"}
    conn.close()


@server.route('/discuss_list', methods=['get'])
def Projectlist_10():
    '''
        http://127.0.0.1:5000/discuss_list?newsID=8T4AZAkd5t9bBXG3kFuAUP&class_n=news&userID=3FtPAHrhhveJGNzC5FaBWv
    http://120.48.49.157:5000/discuss_list?newsID=8T4AZAkd5t9bBXG3kFuAUP&class_n=talk&userID=3FtPAHrhhveJGNzC5FaBWv
    '''
    
    newsID = request.values.get('newsID')
    userID = request.values.get('userID')
    class_n = request.values.get('class_n')
    
    like_news,like_talk,like_discuss = get_like(userID)
    dislike_news,dislike_talk,dislike_discuss = get_dislike(userID)
    
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
        df = pd.read_sql('''select * from user_discuss where news_ID = "{}" and class_n = "{}" '''.format(newsID,class_n) , db)
        db.close()
        df = df.sort_values('S_time', ascending=False).drop_duplicates('discuss_ID')#.sort_index()
        
        discuss_list = []
        
        for index, row in df.iterrows():
            like_sum = get_act(row['discuss_ID'],'news')
            discuss_sum = get_act(row['discuss_ID'],'discuss')
            dislike_sum = get_act(row['discuss_ID'],'dislike')
            
            like = False
            if row['discuss_ID'] in like_discuss:
                like=True
            dislike = False
            if row['discuss_ID'] in dislike_discuss:
                dislike=True
            
            # b = row['THEME'].replace('Google News -','').replace('- Overview','')
            # st = get_max_time(b)
            news = {
                "user_ID":row['user_ID'],
                "news_ID":row['news_ID'],
                "discuss_ID":row['discuss_ID'],
                "discuss_text":row['discuss_text'],
                "username":row['username'],
                "time":row['time'],
                "S_time":row['S_time'],
                
                "like":like,
                "dislike":dislike,
                "like_sum":like_sum,
                "discuss_sum":discuss_sum,
                "share_sum":0,
                "dislike_sum":dislike_sum
                
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
            "S_time":stime,
            
            "like":False,
            "dislike":False,
            "like_sum":0,
            "discuss_sum":0,
            "share_sum":0,
            "dislike_sum":0
                
                
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
    
    
    like_news,like_talk,like_discuss = get_like(userID)
    dislike_news,dislike_talk,dislike_discuss = get_dislike(userID)
    
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
            ld = list(like_discuss)
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
                dislike_sum = get_act(row['NEWS_ID'],'dislike')
                
                dislike = False
                if row['NEWS_ID'] in dislike_news:
                    dislike=True
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
                    "dislike":dislike,
                    "like_sum":like_sum,
                    "discuss_sum":discuss_sum,
                    "share_sum":0,
                    "dislike_sum":dislike_sum
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
                dislike_sum = get_act(row['TH_ID'],'dislike')
                
                dislike = False
                if row['TH_ID'] in dislike_talk:
                    dislike=True
                
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
                    "dislike":dislike,
                    "like_sum":like_sum,
                    "discuss_sum":discuss_sum,
                    "share_sum":0,
                    "dislike_sum":dislike_sum
                    }
    
                if talks not in talk_list:
                    talk_list.append(talks)
            
            
            db = pymysql.connect(
                host=HOST, 
                port=3306,
                user='root',    #在这里输入用户名
                password='root123321',     #在这里输入密码
                charset='utf8mb4' ,
                database='USER'
                ) #连接数据库
            
            
            cur = db.cursor()
            
            df = pd.DataFrame(columns=['discuss_ID', 'discuss_text', 'username', 'time', 'S_time','user_ID'])
            # 执行查询语句
            cur.execute('SELECT discuss_ID,discuss_text,username,time,S_time,user_ID FROM user_discuss')
            # 遍历查询结果并保存到 Pandas 数据框中
            for row in cur:
                if row[0] in ld:
                    df = df.append({'discuss_ID': row[0], 'discuss_text': row[1], 'username': row[2], 'time': row[3], 'S_time': row[4], 'user_ID': row[5]}, ignore_index=True)
                    
            
            df = df.sort_values('S_time', ascending=False).drop_duplicates('discuss_ID')#.sort_index()
    
            discuss_list = []
            
            for index, row in df.iterrows():
                like_sum = get_act(row['discuss_ID'],'like_discuss')
                # like_sum = get_act(row['NEWS_ID'],'news')
                # discuss_sum = get_act(row['NEWS_ID'],'discuss')
                # b = row['THEME'].replace('Google News -','').replace('- Overview','')
                dislike_sum = get_act(row['discuss_ID'],'dislike')
                
                dislike = False
                if row['discuss_ID'] in dislike_discuss:
                    dislike=True
                # st = get_max_time(b)
                news = {
                    "userID":row["user_ID"],
                    "discuss_ID":row["discuss_ID"],
                    "discuss_text":row["discuss_text"],
                    "username":row["username"],
                    "time":row["time"],
                    "S_time":row["S_time"],
                    "like":True,
                    "dislike":dislike,
                    "like_sum":like_sum,
                    "discuss_sum":0,
                    "share_sum":0,
                    "dislike_sum":dislike_sum
                    }
                if news not in discuss_list:
                    discuss_list.append(news)
            
            
            
            
            
            
            project = {
               "code": "OK",
               "msg": '用户收藏',
               "result":{
                "news_list":news_list,
                "talk_list":talk_list,
                "discuss_list":discuss_list
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
                   "msg": '新闻收藏成功',
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
    if class_n == 'discuss':
        if is_like==1:
            try:
                cur.execute(
                    '''INSERT INTO user_like (user_ID,news_ID,class_n) VALUES ("{}","{}","{}")'''.format(userID,newsID,class_n));
                conn.commit()
                print ("记录插入成功!")
                project = {
                   "code": "OK",
                   "msg": '评论收藏成功',
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
                "discussID":newsID
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
                "discussID":newsID
                }
            }
            response = json.dumps(project)  # 将python的字典转换为json字符串
            return response,404,{"Content-Type":"application/json"}
    if class_n == 'talk' or class_n == 'context':
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
                    "talkID":newsID,
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
                return response,405,{"Content-Type":"application/json"}
        elif is_like==0:
            
            sql = '''delete from user_like where user_ID="{}" and news_ID="{}" and class_n="{}"'''.format(userID,newsID,class_n)
            cur.execute(sql)
            conn.commit()
            
            project = {
               "code": "OK",
               "msg": '取消收藏',
               "result":{
                "userID":userID,
                "talkID":newsID,
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
                "talkID":newsID,
                "_class":class_n
                }
            }
            response = json.dumps(project)  # 将python的字典转换为json字符串
            return response,406,{"Content-Type":"application/json"}
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
    return response,407,{"Content-Type":"application/json"}
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
            like_news,like_talk,like_discuss = get_like(userID)
            dislike_news,dislike_talk,dislike_discuss = get_dislike(userID)
            # print('+++++++++++++')
            # print(get_dislike(userID))
            # print('+++++++++++++')
            
            
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
        df = pd.read_sql("select THEME,GPT3_TITLE,KEY_WORD,S_TIME,TIME,TH_ID,TH_ZH,GT_ZH,KW_ZH,AI_img,PIC_URL from GL_NEWS" , db)
        db.close()
        df = df.sort_values('S_TIME', ascending=False).drop_duplicates('TH_ID')#.sort_index()
        # print(df)
        order = get_top()
        df = df.loc[df['TH_ID'].isin(order)]
        df = df.dropna()
        df = df.set_index('TH_ID')
        df = df.reindex(order)
        
        # df = df.reindex(order)
        
        page_size = 10  # 每页条数
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
                like_sum = get_act(index,'news')
                discuss_sum = get_act(index,'discuss')
                dislike_sum = get_act(index,'dislike')
                
                like = False
                if index in like_talk:
                    like=True
                dislike = False
                if index in dislike_talk:
                    dislike=True
                # b = row['THEME'].replace('Google News -','').replace('- Overview','')
                # c = row['TH_ZH'].replace('谷歌新闻-','').replace('-概述','')
                # st = get_max_time(b)
                if row['AI_img'] =='':
                    aimg = ''
                else:
                    aimg = "http://120.48.49.157:5000/images/"+row['AI_img']
                news = {
                    "theme":row['THEME'],
                    "sum_title":row['GPT3_TITLE'],
                    "Key_word":row['KEY_WORD'],
                    "S_time":row['S_TIME'],
                    "TIME":row['TIME'],
                    "NEWS_ID":index,
                    "TH_ZH":row['TH_ZH'],
                    "GT_ZH":row['GT_ZH'],
                    "KW_ZH":row['KW_ZH'],
                    "AI_img":aimg,
                    "like":like,
                    "dislike":dislike,
                    "like_sum":like_sum,
                    "discuss_sum":discuss_sum,
                    "share_sum":0,
                    "dislike_sum":dislike_sum,
                    "share":{
                        "title":row['THEME'],
                        "content":row['GPT3_TITLE'],
                        "url":"https://www.newzsup.com/"
                        }
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
            like_news,like_talk,like_discuss = get_like(userID)
            dislike_news,dislike_talk,dislike_discuss = get_dislike(userID)
            
        
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
                dislike = False
                if row['NEWS_ID'] in dislike_news:
                    dislike=True
                # b = row['THEME'].replace('Google News -','').replace('- Overview','')
                # st = get_max_time(b)
                like_sum = get_act(row['NEWS_ID'],'news')
                discuss_sum = get_act(row['NEWS_ID'],'discuss')
                dislike_sum = get_act(row['NEWS_ID'],'dislike')
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
                    "dislike":dislike,
                    "like_sum":like_sum,
                    "discuss_sum":discuss_sum,
                    "share_sum":get_share(row['NEWS_ID']),
                    "dislike_sum":dislike_sum,
                    "share":{
                        "title":row['TITLE'],
                        "content":row['GPT3_TEXT'],
                        "url":"https://www.newzsup.com/"
                        }
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
        sql = '''select PEOPLE,PINGL,TIME,ZH_CN,P_ZH from Twitter WHERE CLASS_ID = "{}"  '''.format(word)
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
    
@server.route('/twitter_pl', methods=['get'])#'get',
def P_twitter():
    '''
        http://127.0.0.1:5000/twitter_pl?key_word=NATO Membership
    http://120.48.49.157:5000/twitter_pl?key_word=NATO Membership 
    '''
    key_word = request.values.get('key_word')
    print(key_word)
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
        sql = '''select name,text,on_time from twitter_say WHERE key_word = "{}"  '''.format(key_word)
        # sql = "select * from user where name = '李四'"
        cursor.execute(sql)
        #这是查询表中所有的数据
        rest=cursor.fetchall()
        # print(rest)
        news_list = []
        for r in rest:
            news = {
                "username":r[0],
                "ZH_name":r[0],
                "discuss_text":r[1],
                "ZH_talk":r[1],
                "time":r[2]
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
               "msg": "Twitter网友评论",
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
    # server.run()

    server.run(host="192.168.0.4", port=5000, debug=True)
    #server.run(host="192.168.0.4", port=5000, debug=True,ssl_context=('server.crt','server.key'))