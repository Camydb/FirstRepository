# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 15:10:06 2023

@author: Administrator
"""

import pymysql
 
# 打开数据库连接
# db = pymysql.connect("120.48.49.157:3306","remote","remote123456","test_1" )
db = pymysql.connect(
    host="120.48.49.157", 
    port=3306,
    user='root',    #在这里输入用户名
    password='root123321',     #在这里输入密码
    charset='utf8mb4' ,
    database='TX_NEWS'
    ) #连接数据库


# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()


# SQL 查询语句，查询user表
sql = "select BEIZ from SHUM_03" 

cursor.execute(sql)

#这是查询表中所有的数据
rest=cursor.fetchall()


HTML = 'https://new.qq.com/omn/20230225/20230225V03L7400.html'
yuan = (HTML,)
if yuan in rest:
    print('存在')
# c.execute("SELECT DISTINCT * FROM 'TX_0227';")
# print ("数据表去重成功")
# c.execute('''CREATE TABLE TX_0301
#         (BIAOT           TEXT    NOT NULL,
#         ZUOZ            TEXT    NOT NULL,
#         PINGL           TEXT    ,
#         NEIR           TEXT    ,
#         TIME           TEXT    NOT NULL,
#         FENL           TEXT    NOT NULL,
#         ZURL           TEXT    NOT NULL,
#         BEIZ           TEXT);''')
# print ("数据表创建成功")


# 关闭数据库连接
cursor.close()  
db.close()

#%%%%%%%%%%%%%%%%%%%%%%%%
import random
import linecache
# with open("D:/yan.txt", "r", encoding='utf-8') as f:  #打开文本
#     data = f.read()   #读取文本
#     print(data)

def User_Agent():
    txt = open('D:/yan.txt', 'rb')
    data = txt.read().decode('utf-8')  # python3一定要加上这句不然会编码报错！
    txt.close()

    # 获取txt的总行数！
    n = data.count('\n')
    #print("总行数", n)
    # 选取随机的数
    i = random.randint(1, (n + 1))
    #print("本次使用的行数", i)
    ###得到对应的i行的数据
    line=linecache.getline(r'D:/yan.txt', i)
    print(line)
    return line

User_Agent()

#%%%%%%%%%%%%%%%%%%%%%%%
import sqlite3

conn = sqlite3.connect('D:/TenCen/history/AUTO.db')
print ("数据库打开成功")
c = conn.cursor()
# c.execute("SELECT DISTINCT * FROM 'TX_0227';")
# print ("数据表去重成功")
conn.execute(
    '''INSERT INTO TX_0301 (url,dan) VALUES ("{}","{}")'''.format(url,dan));
# c.execute('''CREATE TABLE TX_0301
#         (BIAOT           TEXT    NOT NULL,
#         ZUOZ            TEXT    NOT NULL,
#         PINGL           TEXT    ,
#         NEIR           TEXT    ,
#         TIME           TEXT    NOT NULL,
#         FENL           TEXT    NOT NULL,
#         ZURL           TEXT    NOT NULL,
#         BEIZ           TEXT);''')
# print ("数据表创建成功")
# insert into 'TT' select distinct * from 'TX_0227';
# insert into 'TT' select distinct * from 'TX_0228' WHERE 'NEIR' <> '';
conn.commit()
conn.close()


#%%%%%%%%%%%%%%%%%%%%%%%%%

import shortuuid
import uuid
# 生成一个标准格式32位UUID，参数为位数
# def new_uuid(length=None):
#     if length is None:
#         return str(uuid.uuid1())
#     else:
#         return str(shortuuid.ShortUUID().random(length=length))
    
# uid = uuid.uuid1(8)
# print(uid)
# print(uid.hex)
print(shortuuid.uuid())

#%%%%%%%%%%%%%%%%%%%%%%%%%

# 导入 requests 包
import requests

# 发送请求
x = requests.get('http://114.132.77.224:5000/code')

# 返回网页内容
print(x.text)

#%%%%%%%%%%%%%%%%%%%%%%%%

url = 'https://i.postimg.cc/GpHR9tmg/MWJ4.jpg\n'
u = url.split('/')[-1].split('.')[0]
print(u.split('.')[0])

#%%%%%%%%%%%%%%%%%%%%%%%%%%


project = {
   "code": "OK",
   "result":{
    "msg": '账号注册',
    "user": {
        "app_ID" :'app_ID',
        "HS_url":'',
        "real_name":'',
        "ID_Number":'',
        "nick_name":'user_'+'num',
        "SEX":1,
        "Phone_number":'num',
        "password":'password',
        "Following":'',
        "Status":1,
        }
    }
}
print(project['result']['user'])


#%%%%%%%%%%%%%%%%%%%%%%%%%%%
import re 

input1 = '10915278761'
Pattern1 = re.compile(r'^1[34578]\d{9}$')
result1 = Pattern1.match(input1)
if result1:
    print(input1, "手机号符合要求.")
else:
    print(input1, "手机号不符合要求.")