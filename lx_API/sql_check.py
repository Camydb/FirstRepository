# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 17:27:15 2023

@author: amy
"""
import openai
import re

def gpt_title(text):


    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      temperature=0,
      messages=[
        # {"role": "user", "content": "Can you help me summarize a piece of news?"},
        # {"role": "assistant", "content": "Sure, please provide me with the piece of news you would like me to summarize."},
        {"role": "user", "content": text}
      ]
    )

    # print(completion.choices[0].message.content)
    return(completion.choices[0].message.content.replace('\n',''))

def gpt_output(df):
    prompt = """As an experienced news editor, you need to summarize news based on various news outlets' titles and your intended readers are first-year college students. Output three results: 1. News summarized in a few sentences. 2. News summarized into one short news title. 3. Express the central topic in no more than two words. 4. Where the news happened
                Desired Output Format:
                1. Summary: -||-
                2. Title: -||-
                3. Topic: -||-
                4. Location: -||-
                News Input presented in table format:'''
                {}
                '''
                """

    prompt = prompt.format(df.to_string())
    result = gpt_title(prompt)


    # 保存
    try:
        summary = re.findall("1\.\ Summary:\ (.*)2\.", result)[0]
    except Exception as e:
        print(e)
        summary = ''
        
    try:
        title = re.findall("2\.\ Title:\ (.*)3\.", result)[0]
    except Exception as e:
        print(e)
        title = ''
        
    try:
        topic = re.findall("3\.\ Topic:\ (.*)4\.", result)[0]
    except Exception as e:
        print(e)
        topic = ''
        
    try:
        location = re.findall("4\.\ Location:\ (.*)$", result)[0]
    except Exception as e:
        print(e)
        location = ''
        
        
    return (summary,title,topic,location)


def deepl(text):
    try:
        prompt = '''Translate this from English to Chinese: "{}" '''.format(text)
        return(gpt_title(prompt))
        
    except Exception as e:
        print(e)
        return text
#%%%%%%%%%%%%%%%%%%%%%%%%

token = 't-g2054fj6WUJDTXNYFEZKPFXGR5CTPI5JDWBVDLNN'

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
        "text": ''' {} '''.format(text),
        "target_language": "zh",
        "glossary": [
            {
                "from": "Lark",
                "to": "Lark"
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code==200:
            print(response.status_code)
            return(response.json()['data']['text'])
        else:
            token = get_token()
            time.sleep(1)
            return(text)
    
    except Exception as e:
        print(e)
        print('重新请求')
        token = get_token()
        print(token)
        # print(response.text)
        # print(text)
        # time.sleep(1)
        return(text)

# print(get_token())

#%%%%%%%%%%%%%%%%%%%%%%%
import pymysql
import threading
import requests
from datetime import datetime
import sqlite3 as sq3
import pandas as pd
import time
def open_db():
    # 打开数据库连接
    db = pymysql.connect(host="127.0.0.1", user="root", password="Aa123321", port=3306, database="google")
    return db


def get_title(th_id):
    db = open_db()
    cur = db.cursor()
    texts = ''
    cur.execute("SELECT TH_ID,TITLE,TIME FROM Gl_NEWS")
    rows = cur.fetchall()
    i=0
    df = pd.DataFrame(columns=['title', 'TIME'])
    for row in rows:
        if row[0] == th_id:
            # print(row[0])
            # texts=texts+row[1]+'\n'
            df = pd.concat([df, pd.DataFrame({'title': [row[1]], 'TIME': [row[2]]})], ignore_index=True)

    db.close()
    print(len(df))
    print(df)
    g = gpt_output(df)
    return (g)

# print(get_title('mnZcFKENV'))
def context(summary):
    """
    输入新闻的三句话总结，输出相关背景知识
    """
    prompt = """ As an experienced news editor, you need to provide explanations for certain ideas in news articles so that middle school students can better understand the news. This will help the students comprehend news stories and keep them informed about current events. Please provide background information for this news:'{}'
    """.format(summary)
    result = gpt_title(prompt)
    return result

#%%%%%%%%%%%%%%%%%%%%%%%%

from langdetect import detect
import pymysql
import threading
import requests
from datetime import datetime
import sqlite3 as sq3
import pandas as pd
import time

# db = sq3.connect("D:/T_py/GOOGLE.db")
# df = pd.read_sql("SELECT GPT3_TEXT FROM GL_NEWS" , db)
# db.close()
def open_db():
    # 打开数据库连接
    db = pymysql.connect(host="127.0.0.1", user="root", password="Aa123321", port=3306, database="google")
    return db
# urls = list(df["GPT3_TEXT"])
db = open_db()
# cursor = db.cursor()
cur = db.cursor()
cur1 = db.cursor()

texts = []
# for row in cur.execute('SELECT GPT3_TITLE,context,AI_img FROM Gl_NEWS' ):
# for row in cur.execute('SELECT GPT3_TEXT FROM Gl_NEWS' ):
# for row in cur.execute('SELECT GPT3_TITLE FROM Gl_NEWS' ):
# for row in cur.execute('SELECT KEY_WORD FROM Gl_NEWS' ):
# for row in cur.execute('SELECT TITLE FROM Gl_NEWS' ):
# sql = "SELECT * FROM table_name ORDER BY id DESC LIMIT 1000"
    # else:
# cur.execute("SELECT TH_ID,THEME,TH_ZH,KEY_WORD,KW_ZH,GPT3_TITLE,GT_ZH,REMARKS FROM Gl_NEWS")
cur.execute("SELECT context,context_ZH FROM Gl_NEWS")
rows = cur.fetchall()
i=0
for row in rows:
    if row[0] not in texts:
        texts.append(row[0])
        try:
            # if detect(row[1])=='en':
            if row[1]=='':
                print(row[0])
                # print(row[0])
                
                r1 = context(row[0]).replace("\"","\'")
                print(r1)
                # cur1.execute('''UPDATE Gl_NEWS SET TH_ZH = "{}" WHERE THEME = "{}" '''.format(r1,row[0]))
                cur1.execute('''UPDATE Gl_NEWS SET context = "{}" WHERE GPT3_TITLE = "{}" '''.format(r1,row[0]))
                db.commit()
                print('插入成功')
                print(i)
                i+=1
                print('---------------')
        except Exception as e:
            print(e)
        
    else:
        pass
        
        # r1 = deepl(row[0]).replace("\"","\'")
        # con = context(row[0])
        # con = con.replace("\"","\'")
        # if row[1] == '':
        #     print(i)
        #     i+=1
        #     two_title,one_title,keyword,location = get_title(row[0])
            
        #     tt = deepl(two_title).replace("\"","\'")
        #     ot = deepl(one_title).replace("\"","\'")
        #     kw = deepl(keyword).replace("\"","\'")
            
        #     two_title = two_title.replace("\"","\'")
        #     one_title = one_title.replace("\"","\'")
        #     keyword = keyword.replace("\"","\'")
        #     location = location.replace("\"","\'")
        #     # one_title,ot,keyword,kw,two_title,tt,location,row[0]
            
        #     cur1.execute('''UPDATE Gl_NEWS SET THEME = "{}",TH_ZH = "{}",KEY_WORD = "{}",KW_ZH = "{}",GPT3_TITLE = "{}",GT_ZH = "{}",REMARKS = "{}" WHERE TH_ID = "{}" '''.format(one_title,ot,keyword,kw,two_title,tt,location,row[0]))
        #     db.commit()
        #     print('插入成功')
        
        # print(con)
        # img = ai_img(row[0])
        # print(img)
        # cur1.execute('''UPDATE Gl_NEWS SET context = "{}",AI_img = "{}" WHERE GPT3_TITLE= "{}" '''.format(con,img,row[0]))
        # print('----------------------')
        # db.commit()
    #     print("不为空")
db.close()
print(len(texts))
# text_s = list(set(texts))

# s_urls = split_list(text_s,10)
# print(len(text_s))



#%%%%%%%%%%%%%%%%%%%%%%%

import pymysql
import threading
import requests
from datetime import datetime
import sqlite3 as sq3
import pandas as pd
import time

# db = sq3.connect("D:/T_py/GOOGLE.db")
# df = pd.read_sql("SELECT GPT3_TEXT FROM GL_NEWS" , db)
# db.close()
def open_db():
    # 打开数据库连接
    db = pymysql.connect(host="127.0.0.1", user="root", password="Aa123321", port=3306, database="google")
    return db
# urls = list(df["GPT3_TEXT"])
db = open_db()
# cursor = db.cursor()
cur = db.cursor()
cur1 = db.cursor()

texts = []
# for row in cur.execute('SELECT GPT3_TITLE,context,AI_img FROM Gl_NEWS' ):
# for row in cur.execute('SELECT GPT3_TEXT FROM Gl_NEWS' ):
# for row in cur.execute('SELECT GPT3_TITLE FROM Gl_NEWS' ):
# for row in cur.execute('SELECT KEY_WORD FROM Gl_NEWS' ):
# for row in cur.execute('SELECT TITLE FROM Gl_NEWS' ):
# sql = "SELECT * FROM table_name ORDER BY id DESC LIMIT 1000"
    # else:
cur.execute("SELECT TH_ID,THEME,TH_ZH,KEY_WORD,KW_ZH,GPT3_TITLE,GT_ZH,REMARKS FROM Gl_NEWS")
rows = cur.fetchall()
i=0
for row in rows:
    if row[0] not in texts:
        # print(row[0])
        texts.append(row[0])
        # con = context(row[0])
        # con = con.replace("\"","\'")
        if row[1] == '':
            print(i)
            i+=1
            two_title,one_title,keyword,location = get_title(row[0])
            
            tt = deepl(two_title).replace("\"","\'")
            ot = deepl(one_title).replace("\"","\'")
            kw = deepl(keyword).replace("\"","\'")
            
            two_title = two_title.replace("\"","\'")
            one_title = one_title.replace("\"","\'")
            keyword = keyword.replace("\"","\'")
            location = location.replace("\"","\'")
            # one_title,ot,keyword,kw,two_title,tt,location,row[0]
            
            cur1.execute('''UPDATE Gl_NEWS SET THEME = "{}",TH_ZH = "{}",KEY_WORD = "{}",KW_ZH = "{}",GPT3_TITLE = "{}",GT_ZH = "{}",REMARKS = "{}" WHERE TH_ID = "{}" '''.format(one_title,ot,keyword,kw,two_title,tt,location,row[0]))
            db.commit()
            print('插入成功')
        
        # print(con)
        # img = ai_img(row[0])
        # print(img)
        # cur1.execute('''UPDATE Gl_NEWS SET context = "{}",AI_img = "{}" WHERE GPT3_TITLE= "{}" '''.format(con,img,row[0]))
        # print('----------------------')
        # db.commit()
    #     print("不为空")
db.close()
print(len(texts))
# text_s = list(set(texts))

# s_urls = split_list(text_s,10)
# print(len(text_s))


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
token = 't-g2054fj6WUJDTXNYFEZKPFXGR5CTPI5JDWBVDLNN'

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
        "text": ''' {} '''.format(text),
        "target_language": "zh",
        "glossary": [
            {
                "from": "Lark",
                "to": "Lark"
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code==200:
            print(response.status_code)
            return(response.json()['data']['text'])
        else:
            token = get_token()
            time.sleep(1)
            return(text)
    
    except Exception as e:
        print(e)
        print('重新请求')
        token = get_token()
        print(token)
        # print(response.text)
        # print(text)
        # time.sleep(1)
        return(text)

# print(get_token())

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

from langdetect import detect
import pymysql
import threading
import requests
from datetime import datetime
import sqlite3 as sq3
import pandas as pd
import time

# db = sq3.connect("D:/T_py/GOOGLE.db")
# df = pd.read_sql("SELECT GPT3_TEXT FROM GL_NEWS" , db)
# db.close()
def open_db():
    # 打开数据库连接
    db = pymysql.connect(host="127.0.0.1", user="root", password="Aa123321", port=3306, database="google")
    return db
# urls = list(df["GPT3_TEXT"])
db = open_db()
# cursor = db.cursor()
cur = db.cursor()
cur1 = db.cursor()

texts = []
# for row in cur.execute('SELECT GPT3_TITLE,context,AI_img FROM Gl_NEWS' ):
# for row in cur.execute('SELECT GPT3_TEXT FROM Gl_NEWS' ):
# for row in cur.execute('SELECT GPT3_TITLE FROM Gl_NEWS' ):
# for row in cur.execute('SELECT KEY_WORD FROM Gl_NEWS' ):
# for row in cur.execute('SELECT TITLE FROM Gl_NEWS' ):
# sql = "SELECT * FROM table_name ORDER BY id DESC LIMIT 1000"
    # else:
# cur.execute("SELECT TH_ID,THEME,TH_ZH,KEY_WORD,KW_ZH,GPT3_TITLE,GT_ZH,REMARKS FROM Gl_NEWS")
cur.execute("SELECT context,context_ZH FROM Gl_NEWS")
rows = cur.fetchall()
i=0
for row in rows:
    if row[0] not in texts:
        texts.append(row[0])
        try:
            # if detect(row[1])=='en':
            if row[1] == '':
                # if detect(row[1])=='en':
                print(row[0])
                # print(row[0])
                
                r1 = lark(row[0]).replace("\"","\'")
                print(r1)
                # cur1.execute('''UPDATE Gl_NEWS SET TH_ZH = "{}" WHERE THEME = "{}" '''.format(r1,row[0]))
                cur1.execute('''UPDATE Gl_NEWS SET context_ZH = "{}" WHERE context = "{}" '''.format(r1,row[0]))
                db.commit()
                print('插入成功')
                print(i)
                i+=1
                print('---------------')
        except Exception as e:
            print(e)
        
    else:
        pass
        
        # r1 = deepl(row[0]).replace("\"","\'")
        # con = context(row[0])
        # con = con.replace("\"","\'")
        # if row[1] == '':
        #     print(i)
        #     i+=1
        #     two_title,one_title,keyword,location = get_title(row[0])
            
        #     tt = deepl(two_title).replace("\"","\'")
        #     ot = deepl(one_title).replace("\"","\'")
        #     kw = deepl(keyword).replace("\"","\'")
            
        #     two_title = two_title.replace("\"","\'")
        #     one_title = one_title.replace("\"","\'")
        #     keyword = keyword.replace("\"","\'")
        #     location = location.replace("\"","\'")
        #     # one_title,ot,keyword,kw,two_title,tt,location,row[0]
            
        #     cur1.execute('''UPDATE Gl_NEWS SET THEME = "{}",TH_ZH = "{}",KEY_WORD = "{}",KW_ZH = "{}",GPT3_TITLE = "{}",GT_ZH = "{}",REMARKS = "{}" WHERE TH_ID = "{}" '''.format(one_title,ot,keyword,kw,two_title,tt,location,row[0]))
        #     db.commit()
        #     print('插入成功')
        
        # print(con)
        # img = ai_img(row[0])
        # print(img)
        # cur1.execute('''UPDATE Gl_NEWS SET context = "{}",AI_img = "{}" WHERE GPT3_TITLE= "{}" '''.format(con,img,row[0]))
        # print('----------------------')
        # db.commit()
    #     print("不为空")
db.close()
print(len(texts))
# text_s = list(set(texts))

# s_urls = split_list(text_s,10)
# print(len(text_s))

#%%%%%%%%%%%%%%

title = 'Mexico investigates migration chief over deadly fire in detention center - Local News 8'
timet = '2023-04-13T00:23:02Z'
content = '''By Florencia Trucco, Karina Maciel and Karol Suarez

Mexican authorities are investigating the head of the country’s immigration agency, in the wake of last month’s deadly fire in a migrant detention center that killed at least 38 people and left dozens injured.

Mexico’s President Andrés Manuel López Obrador confirmed on Wednesday that the Attorney General’s Office is probing Francisco Garduño, commissioner of the National Institute of Migration (INM) in Ciudad Juárez, for the tragedy.

In his morning press conference, Lopez Obrador said that he did not know the scope of the investigation or the specific accusations against Garduño.

“There are several involved and this morning there was discussion that some may be accused of negligence, others of homicide. There is still a need for the Prosecutor’s Office to report more on the investigation and for the judges to be in charge of delivering justice,” the Mexican president said.

“From the beginning we maintained that there would be no impunity for anyone,” he added.

CNN is seeking comment from Garduño and his representatives.

Mexico’s Attorney General earlier announced that criminal proceedings had begun involving the INM chief and another official identified only as Antonio “N.”

Both men are accused of engaging in “alleged criminal conduct, by failing to comply with their obligations to monitor, protect and provide security to people and facilities under their charge, facilitating crimes committed against migrants.”

The statement noted that a similar incident had occurred on March 31, 2020 in Tabasco, where one person died and 14 others were injured, raising concerns of a potential “pattern of conduct in which the security measures that were essential and mandatory in these cases have been omitted by those responsible.”

Four other public servants are also being prosecuted and investigations are still ongoing, the statement concluded.

As CNN previously reported, the deadly March blaze at the INM facility started shortly after 10 p.m. inside an accommodation area, according to the agency. Authorities said it broke out after they picked up and detained a group of migrants from the streets of the border city, which sits across from El Paso, Texas.

Sixty-eight men from Central and South America were being held at the facility, the INM said in a statement, including citizens of Guatemala, Colombia, Ecuador, El Salvador, Honduras and Venezuela.

Surveillance video from inside the center obtained by CNN appeared to show that those detained were behind bars with the gate locked at the time of the fire.

An eyewitness to the blaze, a Venezuelan woman whose husband was trapped inside the building and injured in the fire, spoke to Reuters news agency. Fighting back tears, she blamed Mexican authorities and claimed the doors to the detention center were not opened.

“At 10 p.m., we started to see smoke billowing from everywhere, everybody ran away but they left the men locked in. Everybody was removed from the area, but they left the men locked in. They never opened the door,” 31-year-old Viangly Infante, a Venezuelan national, told the agency.

The INM said at the time that it strongly rejected “the acts that led to this tragedy,” and opened an investigation into the incident.

The-CNN-Wire

™ & © 2023 Cable News Network, Inc., a Warner Bros. Discovery Company. All rights reserved.'''

prompt = '''Task: Summarize the news article "{}" published on {}. Provide details about this news. Then translate the summary from English to Chinese.
Output Format:
"""
Eng: -||-
Zh: -||-
"""
Here is the whole article:
"""
{}
"""
'''.format(title,timet,content)


print(gpt_title(prompt))


#%%%%%%%%%%%%%%%

def gpt_sum(title,timet,content):
    prompt = '''Task: Summarize the news article "{}" published on {}. Provide details about this news. 
    Here is the whole article:
    """
    {}
    """
    '''.format(title,timet,content)
    # print(gpt_title(prompt))
    return(gpt_title(prompt))

print(gpt_sum(title,timet,content))


#%%%%%%%%%%%%%%%%%


import requests

url = 'http://120.48.49.157:5000/chuan?name=safsafsdfsdfsd.png'
files = {'file': open('F:/WS8801/img/img-BfEKDK3HU4tlHfUwFVmas087.png', 'rb')}
response = requests.get(url, files=files)
print(response.text)