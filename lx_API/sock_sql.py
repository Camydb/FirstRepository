# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 10:48:48 2023

@author: amy
"""

# import sqlite3
# conn = sqlite3.connect("D:/T_py/GOOGLE.db")
# # print(db)
# # cursor = conn.cursor()
# cursor = conn.cursor()
# cursor.execute('''select CONTENT,GPT3_TEXT from GL_NEWS''')
# # conn.commit()
# # sql = "select * from user where name = '李四'"
# #这是查询表中所有的数据
# rest=cursor.fetchone()
# print(rest[1])
# conn.close()
import shortuuid
from datetime import datetime
import sqlite3 as sq3
from newspaper import Article
import sqlite3
from pymysql.converters import escape_string
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import openai
import shortuuid

token = '11t-g2053nauY3RDO2KEV56QW7CUSJPAXUDM6EADXZP6'



def gpt_translate(text):


    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        # {"role": "user", "content": "Can you help me summarize a piece of news?"},
        {"role": "assistant", "content": text},
        {"role": "user", "content": "Translate into Chinese."}
      ]
    )

    # print(completion.choices[0].message.content)
    return(completion.choices[0].message.content.replace('\n',''))

def gpt_sum(text):


    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": "Task: Extract 5 key points from this news article.\n\n News: {}".format(text)}
        # {"role": "assistant", "content": "Sure, please provide me with the piece of news you would like me to summarize."},
        # {"role": "user", "content": text}
      ]
    )

    # print(completion.choices[0].message.content)
    return(completion.choices[0].message.content.strip("\n").replace("\n\n","\n"))

def get_token():
    url = 'https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal'
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = { "app_id": "cli_a49073a33638100a","app_secret": "b4zYuiq7HPT5Ly1OACGwGzQROKmZU1Li"}
    response = requests.post(url, headers=headers, json=data)
    print('get_token')
    return(response.json()["tenant_access_token"])




def lark(text):
    global token
    url = 'https://open.larksuite.com/open-apis/translation/v1/text/translate'
    # headers = {'Authorization': 'Bearer t-g2053n6c7EF4YVHPSO3QWKJ5CWD6ULMUE3ZSKENR', 'Content-Type': 'application/json; charset=utf-8'}
    headers = {'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json; charset=utf-8'}
    data = {
        "source_language": "en",
        "text": text,
        "target_language": "zh",
        "glossary": [
            {
                "from": "Lark",
                "to": "Lark"
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code==200:
        print(response.status_code)
        return(response.json()['data']['text'])
    elif response.status_code==400:
        token = get_token()
        print('重新请求')
        headers = {'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json; charset=utf-8'}
        response = requests.post(url, headers=headers, json=data)
        time.sleep(1)
        return(response.json()['data']['text'])
    else:
        return ('无法翻译')



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


conn = sq3.connect("D:/T_py/GOOGLE.db")
cur = conn.cursor()
cur2 = conn.cursor()

# for row in cur.execute('SELECT NEWS_ID,CONTENT,GPT3_TEXT FROM GL_NEWS' ):
for row in cur.execute('SELECT PEOPLE,P_ZH FROM Twitter' ):
    # rest=row.fetchone()
    # print(row[0])
    
    # variable = datetime.strptime(row[0], '%m/%d/%y %I:%M %p')
    # time2=time.strptime(str(row[0]),"%Y-%m-%d %H:%M:%S")
    # mkt=int(time.mktime(time2))
    # text = row[0].replace('\n','')
    # date1 = datetime.strptime(row[0], "%Y-%m-%dT%H:%M:%SZ")
    # s_t=time.strptime(str(date1),"%Y-%m-%d %H:%M:%S")
    # mkt=int(time.mktime(s_t))
    # kd = row[1].replace('\n','')
    if row[1] is None:
        try:
            lk = lark(row[0])
            print(lk)
            # kd = row[1].replace('\n','')
            # ti = row[2].replace('\n','')
            # tX = row[3].replace('\n','')
            # NEWS_ID = shortuuid.uuid()
            # print(NEWS_ID)
            # gpt_text = '123456'
            # cur2.execute('''UPDATE GL_NEWS SET GPT3_TEXT = ? WHERE NEWS_ID = ?''', (gpt,row[0]))
            # cur2.execute('''UPDATE GL_NEWS SET GPT3_TITLE = ? WHERE NEWS_ID = ?''', (ti,row[0]))
            cur2.execute('''UPDATE Twitter SET P_ZH = ? WHERE PEOPLE = ?''', (lk,row[0]))
            # cur2.execute('''UPDATE GL_NEWS SET GPT3_TITLE = ? WHERE GPT3_TITLE= ?''', (text,row[0]))
            conn.commit()
            print('------------------')
        except Exception as e:
            print(e)
            print('------------------')
    else:
        print("不为空")
    
        
conn.close()


#%%%%%%%%%%%%%%%%%%%%%%%%%

# import sqlite3


# conn = sqlite3.connect("D:/T_py/GOOGLE.db")
# # print(db)
# # cursor = conn.cursor()
# cursor = conn.cursor()
# cursor.execute('''select CONTENT,GPT3_TEXT from GL_NEWS''')
# # conn.commit()
# # sql = "select * from user where name = '李四'"
# #这是查询表中所有的数据
# rest=cursor.fetchone()
# print(rest[1])

# conn.close()
import shortuuid
from datetime import datetime
import sqlite3 as sq3
conn = sq3.connect("D:/T_py/GOOGLE.db")

cur = conn.cursor()
cur2 = conn.cursor()



for row in cur.execute('SELECT NEWS_ID,KEY_WORD FROM GL_NEWS' ):
    # rest=row.fetchone()
    # print(row[0])
    
    # variable = datetime.strptime(row[0], '%m/%d/%y %I:%M %p')
    # time2=time.strptime(str(row[0]),"%Y-%m-%d %H:%M:%S")
    # mkt=int(time.mktime(time2))
    # text = row[0].replace('\n','')
    # date1 = datetime.strptime(row[0], "%Y-%m-%dT%H:%M:%SZ")
    # s_t=time.strptime(str(date1),"%Y-%m-%d %H:%M:%S")
    # mkt=int(time.mktime(s_t))
    # kd = row[1].replace('\n','')
    # if row[2] is None:
    try:
        # gpt = gpt_sum(row[1])
        # print(gpt)
        ky = row[1].replace('.','')
        # kd = row[1].replace('\n','')
        # ti = row[2].replace('\n','')
        # tX = row[3].replace('\n','')
        # NEWS_ID = shortuuid.uuid()
        # print(NEWS_ID)
        # gpt_text = '123456'
        cur2.execute('''UPDATE GL_NEWS SET KEY_WORD = ? WHERE NEWS_ID = ?''', (ky,row[0]))
        # cur2.execute('''UPDATE GL_NEWS SET GPT3_TITLE = ? WHERE NEWS_ID = ?''', (ti,row[0]))
        # cur2.execute('''UPDATE GL_NEWS SET GPT3_TEXT = ? WHERE NEWS_ID = ?''', (tX,row[0]))
        # cur2.execute('''UPDATE GL_NEWS SET GPT3_TITLE = ? WHERE GPT3_TITLE= ?''', (text,row[0]))
        conn.commit()
        print('------------------')
    except Exception as e:
        print(e)
        print('------------------')
   
        
conn.close()


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%

import pandas as pd

df = pd.read_sql("select THEME,GPT3_TITLE,KEY_WORD from GL_NEWS" , db)

# sql = "select * from user where name = '李四'"
# cursor.execute(sql)
#这是查询表中所有的数据
# rest=cursor.fetchall()
db.close()
news_list = []



for r in df:
    b = r[0].replace('Google News -','').replace('- Overview','')
    # st = get_max_time(b)
    news = {
        "theme":b,
        "sum_title":r[1],
        "Key_word":r[2],
        "S_time":st
        }
    if news not in news_list:
        news_list.append(news)


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# =============================================================================
# 以下是一个使用Python编写的多线程数据库读写示例。我们将使用Python的SQLite模块来连接和操作数据库。
# 
# 首先，我们需要安装SQLite模块。可以通过运行以下命令来安装：
# 
# ```python
# pip install pysqlite3
# ```
# 
# 接下来，我们将编写一个包含两个类的程序：一个用于写入数据，另一个用于读取数据。每个类都将使用线程来执行其任务。
# 
# ```python
# =============================================================================
import threading
import sqlite3

class DatabaseWriter(threading.Thread):
    def __init__(self, data):
        threading.Thread.__init__(self)
        self.data = data
    
    def run(self):
        # Connect to the database
        conn = sqlite3.connect('example.db')
        c = conn.cursor()

        # Insert data into the database
        c.execute("INSERT INTO my_table VALUES (?)", (self.data,))
        conn.commit()

        # Close the database connection
        conn.close()

class DatabaseReader(threading.Thread):
    def run(self):
        # Connect to the database
        conn = sqlite3.connect('example.db')
        c = conn.cursor()

        # Read data from the database
        c.execute("SELECT * FROM my_table")
        rows = c.fetchall()

        # Print the data
        for row in rows:
            print(row)

        # Close the database connection
        conn.close()
# =============================================================================
# ```
# 
# 在这个例子中，我们创建了一个名为DatabaseWriter的类和一个名为DatabaseReader的类。DatabaseWriter类接受一个数据参数，它将插入到数据库中。run()函数包含了连接数据库、插入数据和关闭数据库连接的代码。
# 
# DatabaseReader类只有一个run()函数，该函数将连接到数据库、读取数据、打印数据并关闭数据库连接。
# 
# 现在，我们可以在主程序中创建一个DatabaseWriter对象和一个DatabaseReader对象，并分别启动它们的线程：
# 
# ```python
# =============================================================================
writer = DatabaseWriter("Hello, world!")
reader = DatabaseReader()

writer.start()
reader.start()

writer.join()
reader.join()
# =============================================================================
# ```
# 
# 在这个例子中，我们创建了一个DatabaseWriter对象，它将字符串"Hello, world!"插入到数据库中。我们还创建了一个DatabaseReader对象，它将读取数据库中的所有数据并打印它们。
# 
# 最后，我们启动两个线程并等待它们完成。
# 
# 这就是一个简单的多线程数据库读写程序的例子。请注意，在实际使用中，您需要更复杂的逻辑来处理并发访问和数据一致性问题。
# =============================================================================
#%%%%%%%%%%%%%%%%%%%%%%%%%

# =============================================================================
# 以下是一个简单的多线程数据库写入示例，其中使用了Python的sqlite3模块和threading模块：
# 
# ```python
# =============================================================================
import sqlite3
import threading

# 创建数据库连接
conn = sqlite3.connect('test.db')

# 创建表
conn.execute('''CREATE TABLE IF NOT EXISTS users
             (ID INT PRIMARY KEY NOT NULL,
             NAME TEXT NOT NULL);''')

# 数据
data = [(1, 'Alice'), (2, 'Bob'), (3, 'Charlie'), (4, 'David'), (5, 'Eva')]

# 写入函数
def write_to_db(data):
    for d in data:
        conn.execute("INSERT INTO users (ID, NAME) VALUES (?, ?)", d)
    conn.commit()

# 多线程写入
threads = []
for i in range(0, len(data), 2):
    t = threading.Thread(target=write_to_db, args=(data[i:i+2],))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

print("Done.")
# =============================================================================
# ```
# 
# 在这个示例中，我们首先使用sqlite3模块创建了一个数据库连接，并创建了一个名为“users”的表。然后，我们定义了一个写入函数write_to_db，它将数据写入到数据库中。
# 
# 接下来，我们使用多线程创建了多个线程，每个线程都调用write_to_db函数来写入数据。在这个示例中，我们将数据拆分成了两个元素的块，并将每个块传递给一个线程。
# 
# 最后，我们使用join方法等待所有线程完成，并输出“Done.”。
# 
# 需要注意的是，在多线程编程中，写入数据库时可能会遇到并发写入的问题。为了避免这种情况，我们可以使用锁来保护数据库写操作。
# =============================================================================

#%%%%%%%%%%%%%%%%%%%%%
import pandas as pd

db = sq3.connect("D:/T_py/GOOGLE.db")
# cur = conn.cursor()
# cur2 = conn.cursor()
# like = "News about counterattack, North Korea, and Kim Jong Un"
# 使用pandas的read_sql函数读取数据
# df = pd.read_sql('''SELECT NEWS_ID,TIME,S_TIME FROM GL_NEWS WHERE THEME LIKE "%{}%" '''.format(like), conn)
# '''select PEOPLE,PINGL,TIME,ZH_CN from Twitter WHERE CLASS like "%{}%"  '''.format(word)


df = pd.read_sql("select THEME,GPT3_TITLE,KEY_WORD,S_TIME from GL_NEWS" , db)



# sql = "select * from user where name = '李四'"
# cursor.execute(sql)
#这是查询表中所有的数据
# rest=cursor.fetchall()
db.close()
news_list = []



# =============================================================================
# for r in df:
#     b = r[0].replace('Google News -','').replace('- Overview','')
#     # st = get_max_time(b)
#     news = {
#         "theme":b,
#         "sum_title":r[1],
#         "Key_word":r[2],
#         "S_time":st
#         }
#     if news not in news_list:
#         news_list.append(news)
# =============================================================================



# 输出数据框
# df = df.drop_duplicates(subset='THEME', keep='last', inplace=True)
df = df = df.sort_values('S_TIME', ascending=False).drop_duplicates('THEME').iloc[:10]#.sort_index()
print(df)
print(df.shape[0])
# print(max(df['S_TIME']))
# conn.close()
for index, row in df.iterrows():
    print(row['THEME'],row['S_TIME'])

#%%%%%%%%%%%%

print(df.iloc[9])

#%%%%%%%%%%%%%%%%%%%


# =============================================================================
# 以下是一个简单的Python多线程写入数据库的示例：
# 
# ```python
# =============================================================================
import threading
import sqlite3
import mysql.connector

# 数据库连接配置
config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'database': 'testdb'
}

# 插入数据的SQL语句
insert_sql = "INSERT INTO users (name, age) VALUES (%s, %s)"

# 定义线程任务
def insert_data(name, age):
    # 创建数据库连接
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    # 执行插入语句
    cursor.execute(insert_sql, (name, age))
    conn.commit()
    # 关闭连接
    cursor.close()
    conn.close()

# 创建线程列表
threads = []

# 创建10个线程并启动
for i in range(10):
    t = threading.Thread(target=insert_data, args=('user{}'.format(i), i))
    threads.append(t)
    t.start()

# 等待所有线程执行完毕
for t in threads:
    t.join()
# =============================================================================
# ```
# 
# 以上代码中，我们使用了Python的`threading`模块创建了10个线程，每个线程都会向数据库中插入一条数据。为了保证数据的一致性，我们使用了MySQL的事务机制，即在提交之前执行`conn.commit()`，以便在所有线程执行完毕之后再一次性提交所有数据的插入。
# =============================================================================

#%%%%%%%%%%%%%%%%

import requests

url = 'https://example.com/api/post'
headers = {'Authorization': 'Bearer abc123', 'Content-Type': 'application/json'}
data = {'name': 'John', 'age': 30}

response = requests.post(url, headers=headers, json=data)

print(response.status_code)
print(response.json())


#%%%%%%%%%%%%%%%%%




import requests

def get_token():
    url = 'https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal'
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = { "app_id": "cli_a49073a33638100a","app_secret": "b4zYuiq7HPT5Ly1OACGwGzQROKmZU1Li"}
    response = requests.post(url, headers=headers, json=data)
    print('get_token')
    return(response.json()["tenant_access_token"])



#%%%%%%%%%%%%%%%%%%%%%%%%


import requests

token = 't-g2053nauY3RDO2KEV56QW7CUSJPAXUDM6EADXZP6'

url = 'https://open.larksuite.com/open-apis/translation/v1/text/translate'
headers = {'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json; charset=utf-8'}
data = {
    "source_language": "zh",
    "text": "尝试使用一下Lark吧",
    "target_language": "en",
    "glossary": [
        {
            "from": "Lark",
            "to": "Lark"
        }
    ]
}

response = requests.post(url, headers=headers, json=data)

print(response.status_code)
print(response.json()['data']['text'])