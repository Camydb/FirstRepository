# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 10:34:11 2023

@author: amy
"""

# import requests
# from bs4 import BeautifulSoup
# import bs4, csv
# import time
# from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.common.keys import Keys
# import sqlite3
# from fake_useragent import UserAgent
# import threading
# import random

# from selenium.webdriver import ChromeOptions

## 用Article爬取单条新闻
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
from multiprocessing import Pool

token = 't-g2053nauY3RDO2KEV56QW7CUSJPAXUDM6EADXZP6'

def split_list(list,thread_num):
    list_total = []
    num = thread_num  # 线程数量
    x = len(list) // num  # 将参数进行分批（5批）方便传参
    count = 1  # 计算这是第几个列表
    for i in range(0, len(list), x):
        if count < num:
            list_total.append(list[i:i + x])
            count += 1
        else:
            list_total.append(list[i:])    # 多余的参数全部放在最后一个列表中
            break
    return list_total


def shijian(timeStamp):
    #转换成localtime
    time_local = time.localtime(timeStamp)
    #转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
    return dt

# url = 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lkdkxYeEJoRjE4RkNSSU5pYUVpZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1'
def title_sum(url,one_tit):
    wbdata = requests.get(url,headers=request_header())
    if wbdata.status_code == 200:
        # data = response.json()
        # 对获取到的文本进行解析
        soup = BeautifulSoup(wbdata.text,'lxml')
        # print(soup.title.text)
        # 获取文章 内容
        # tx = soup.title.text
        # print(tx)
        # twitter(soup)
        # lj = soup.find_all(attrs={'aria-label':'Full Coverage'})
        js = soup.find_all(attrs={'class':'xrnccd'})
        # uurl = js.find_all(attrs={'class':'VDXfz'})
        news = 'Help me summarize all the news headlines in three sentences.\n\n'
        
        key_word = "Help me extract one keyword.\n\n"
        for j in js:
            try:
                title = j.h3.text
                # new_url = 'https://news.google.com/'+j.a['href'][2:]
                # new_time = j.time['datetime']
                print(title)
                # print(new_url)
                # print(new_time)
                news = news + '\n' + title
                key_word = key_word + '\n' + title
                # jurl = j.find(attrs={'class':'ipQwMb ekueJc RD0gLb'})
                # # surl = 'https://news.google.com/'+uu['href'][2:]
                # j_title = jurl.text
                # j_url = 'https://news.google.com/'+jurl['href'][2:]
                # print(j_title)
                # print(j_url)
                # get_news(surl,tx)
                # time.sleep(3)
                # print(uu.href)
            except Exception as e:
                print(e)
            print('-----------------')
        two = gpt_title(news)
        three = gpt_title(key_word)
        print(two)
        print(three)
        # print(gpt_translate(th))
        print('-----------------')
        for j in js:
            try:
                title = j.h3.text
                new_url = 'https://news.google.com/'+j.a['href'][2:]
                new_time = j.time['datetime']
                # print(title)
                print(new_url)
                print(new_time)
                # jurl = j.find(attrs={'class':'ipQwMb ekueJc RD0gLb'})
                # # surl = 'https://news.google.com/'+uu['href'][2:]
                # j_title = jurl.text
                # j_url = 'https://news.google.com/'+jurl['href'][2:]
                # print(j_title)
                # print(j_url)
                get_news(title,new_url,new_time,two,one_tit,url,three)
                # time.sleep(3)
                # print(uu.href)
            except Exception as e:
                print(e)
            print('-----------------')
    return 0

# =============================================================================
# def gpt_translate(text):
#     # openai.api_key = os.getenv("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")
#     openai.api_key = "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"
# 
#     completion = openai.ChatCompletion.create(
#       model="gpt-3.5-turbo",
#       messages=[
#         # {"role": "user", "content": "Can you help me summarize a piece of news?"},
#         {"role": "assistant", "content": text},
#         {"role": "user", "content": "Translate into Chinese."}
#       ]
#     )
# 
#     # print(completion.choices[0].message.content)
#     return(completion.choices[0].message.content.replace('\n',''))
# =============================================================================


def gpt_title(text):
    # openai.api_key = os.getenv("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")
    # openai.api_key = "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"

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        # {"role": "user", "content": "Can you help me summarize a piece of news?"},
        # {"role": "assistant", "content": "Sure, please provide me with the piece of news you would like me to summarize."},
        {"role": "user", "content": text}
      ]
    )

    # print(completion.choices[0].message.content)
    return(completion.choices[0].message.content.replace('\n',''))

# =============================================================================
# def gpt_sum(text):
#     # openai.api_key = os.getenv("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")
#     openai.api_key = "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"
# 
#     completion = openai.ChatCompletion.create(
#       model="gpt-3.5-turbo",
#       messages=[
#         {"role": "user", "content": "Can you help me summarize a piece of news?"},
#         {"role": "assistant", "content": "Sure, please provide me with the piece of news you would like me to summarize."},
#         {"role": "user", "content": text}
#       ]
#     )
# 
#     # print(completion.choices[0].message.content)
#     return(completion.choices[0].message.content.replace('\n',''))
# =============================================================================

def gpt_sum(text):
    # openai.api_key = os.getenv("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")
    # openai.api_key = "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"

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

def request_header():
    headers = {
        'User-Agent': UserAgent().random #常见浏览器的请求头伪装（如：火狐,谷歌）
        #'User-Agent': UserAgent().Chrome #谷歌浏览器
        }
    return headers

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

def save(db,TITLE,AUTHOR,CONTENT,TIME,THEME,THEME_URL,GPT3_TITLE,GPT3_TEXT,NEWS_URL,PIC_URL,REMARKS,three):
    conn = sqlite3.connect(db)
    # print(db)
    SAVE_TIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    NEWS_ID = shortuuid.uuid()
    
    date1 = datetime.strptime(str(TIME), "%Y-%m-%dT%H:%M:%SZ")
    s_t=time.strptime(str(date1),"%Y-%m-%d %H:%M:%S")
    S_TIME=int(time.mktime(s_t))
    
    try:
        conn.execute(
            '''INSERT INTO GL_NEWS (NEWS_ID,TITLE,AUTHOR,CONTENT,TIME,S_TIME,SAVE_TIME,THEME,KEY_WORD,THEME_URL,GPT3_TITLE,GPT3_TEXT,NEWS_URL,PIC_URL,REMARKS) 
            VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'''.format(NEWS_ID,TITLE,AUTHOR,CONTENT,TIME,S_TIME,SAVE_TIME,THEME,three,THEME_URL,GPT3_TITLE,GPT3_TEXT,NEWS_URL,PIC_URL,REMARKS));
        conn.commit()
        print ("记录插入成功!")
    except Exception as e:
        conn.rollback()
        print(e)
    conn.close()
    

def get_news(title,news_url,new_time,two,one_tit,one_url,three):
    # get_news(title,new_url,new_time,two,one_tit)
    # 目标新闻网址
    # goo = 'https://news.google.com/articles/CBMiUWh0dHBzOi8vd3d3LmNic25ld3MuY29tL25ld3Mvc2lsaWNvbi12YWxsZXktYmFuay1mYWlsdXJlLXdvcmxkd2lkZS1yZXBlcmN1c3Npb25zL9IBVWh0dHBzOi8vd3d3LmNic25ld3MuY29tL2FtcC9uZXdzL3NpbGljb24tdmFsbGV5LWJhbmstZmFpbHVyZS13b3JsZHdpZGUtcmVwZXJjdXNzaW9ucy8?hl=en-US&amp;gl=US&amp;ceid=US%3Aen'
    # url = 'https://www.cbsnews.com/news/silicon-valley-bank-failure-worldwide-repercussions/'
    # url = 'https://www.nytimes.com/2023/03/12/business/janet-yellen-silicon-valley-bank.html'
    # url = 'https://www.cnn.com/2023/03/13/investing/svb-panic-china-companies-tycoons-intl-hnk/index.html'
    # url = 'https://apnews.com/article/silicon-valley-bank-bailout-yellen-deposits-failure-94f2185742981daf337c4691bbb9ec1e'
    # url = 'https://www.fdic.gov/news/press-releases/2023/pr23016.html'
    news = Article(news_url, language='en')
    news.download()        # 加载网页
    news.parse()           # 解析网页
    # print('题目：',news.title)       # 新闻题目
    # print('正文：\n',news.text)      # 正文内容      
    # print(news.publish_date) # 发布日期
    news_text = news.text.replace("\"","\'")
    news_title = title.replace("\"","\'")
    
    one_tit = one_tit.replace("\"","\'")
    two = two.replace("\"","\'")
    three = three.replace("\"","\'")
    
    
    # news_text = escape_string(news_text)
    # news_title = escape_string(news_title)
    
    # news_authors = news.authors.replace("\"","\'")
    
    gpt_text = gpt_sum(news_text)
    gpt_text = gpt_text.replace("\"","\'")
    # gpt_text = ''
    if news_text!='':
        try:
            save("D:/T_py/GOOGLE.db",news_title,news.authors,news_text,new_time,one_tit,one_url,two,gpt_text,news_url,news.top_image,'',three)
            # save(               db,TITLE,     AUTHOR,      CONTENT,  TIME,    THEME,  THEME_URL,GPT3_TITLE,GPT3_TEXT,NEWS_URL,PIC_URL,REMARKS)
        except Exception as e:
            print(e)
    else:
        print('no news')
        pass



def twitter(url):
    
    wbdata = requests.get(url,headers=request_header())
    if wbdata.status_code == 200:
        soup = BeautifulSoup(wbdata.text,'lxml')
        # print(soup.title.text)
        # 获取文章 内容
        # tx = soup.title.text
        # print(tx)
        # twitter(soup)
    
    title = soup.title.text
    artical=soup.find_all(attrs={'class':'ifw3f'})
    for para in artical:
        fu = para.parent
        
        di = fu.find(attrs={'class':'js5zDf'})
        print(di.text)
        
        print(para.text)
        pt = para.text.replace("\"","\'")
        
        # xiong = fu.find(attrs={'class':'eGzQsf'})
        # tm = xiong.time.text
        # if len(tm)<9:
        #     now = datetime.datetime.now().strftime('%m/%d/23')
        #     tm = now+' '+tm
        # print(tm)
        
        date = str(fu.time['datetime'])
        tm = shijian(int(date[:-3]))
        print(tm)
        
        
        conn = sqlite3.connect("D:/T_py/GOOGLE.db")
        # print(db)
        stime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # cursor = conn.cursor()
        ZH_CN = lark(pt).replace("\"","\'")
        P_ZH = lark(di.text).replace("\"","\'")
        try:
            conn.execute(
                '''INSERT INTO Twitter (PINGL,ZH_CN,PEOPLE,P_ZH,TIME,BJ_TIME,S_TIME,CLASS,CLASS_URL) VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}")'''.format(pt,ZH_CN,di.text,P_ZH,tm,stime,date[:-3],title,url));
            conn.commit()
            print ("记录插入成功!")
        except Exception as e:
            conn.rollback()
            print(e)
        conn.close()  
        print('-----------------')
    return title

#%%%%%%%%%%%%%%%%%%

url =   'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen'
# url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen'

urls = []


wbdata = requests.get(url,headers=request_header())
if wbdata.status_code == 200:
    # data = response.json()
    # 对获取到的文本进行解析
    soup = BeautifulSoup(wbdata.text,'lxml')
    # print(soup.title.text)
    # 获取文章 内容
    # tx = soup.title.text
    # print(tx)
    # twitter(soup)
    
    lj = soup.find_all(attrs={'aria-label':'Full Coverage'})
    
    # js = soup.find(attrs={'jsname':'gKDw6b'})
    # uurl = js.find_all(attrs={'class':'VDXfz'})
    for uu in lj:
        try:
            surl = 'https://news.google.com/'+uu['href'][2:]
            # print(surl)
            # get_news(surl,tx)
            one_tit = twitter(surl)
            print(one_tit)
            
            so = surl + '&so=1'
            urls.append(so)
            # time.sleep(3)
            # print(so)
            title_sum(so,one_tit)
        except Exception as e:
            print(e)
        print('-----------------')
        
print(urls)
print(len(urls))
# url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen'
# wbdata = requests.get(url,headers=request_header())
# if wbdata.status_code == 200:
#     # data = response.json()
#     # 对获取到的文本进行解析
#     soup = BeautifulSoup(wbdata.text,'lxml')
#     # print(soup.title.text)
#     # 获取文章 内容
#     # tx = soup.title.text
#     # print(tx)
#     # twitter(soup)
#     lj = soup.find_all(attrs={'aria-label':'Full Coverage'})
#     # js = soup.find(attrs={'jsname':'gKDw6b'})
#     # uurl = js.find_all(attrs={'class':'VDXfz'})
#     for uu in lj:
#         try:
#             surl = 'https://news.google.com/'+uu['href'][2:]
#             print(surl)
#             # get_news(surl,tx)
#             # time.sleep(3)
#             # print(uu.href)
#         except Exception as e:
#             print(e)
#         print('-----------------')




#%%%%%%%%%%%%%%%%%%%%%%%%

so = 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2o5NDhmcUJoRmUtREwxdi1VV2RDZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1'
tit = "Google News - Diablo 4's early access beta - Overview"
title_sum(so,tit)

#%%%%%%%%%%%%%%%%%%%%%%

title = 'Ashava - Diablo 4 Wiki Guide'
news_url ='https://news.google.com/articles/CBMiKWh0dHBzOi8vd3d3Lmlnbi5jb20vd2lraXMvZGlhYmxvLTQvQXNoYXZh0gEA?hl=en-US&gl=US&ceid=US%3Aen'
new_time ='2023-03-19T04:09:34Z'
two = '''Blizzard is addressing long queue times in the Diablo 4 beta and working on improving server stability, while players are asking for improvements in dungeon randomization and UI. The max level in the beta, best classes and builds, and even how to beat the Butcher boss have been discussed, along with known issues and hotfixes for performance problems, error codes, and latency issues. There is also exploration of co-op play and the appearance of the world boss Ashava in the beta.'''
one_tit = 'Blizzard State They Are Working On Diablo 4’s Long Beta Queue Times'
one_url = 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2o5NDhmcUJoRmUtREwxdi1VV2RDZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1'



get_news(title,news_url,new_time,two,one_tit,one_url)


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
import sqlite3 as sq3
conn = sq3.connect("D:/T_py/GOOGLE.db")
import threading
import requests

cur = conn.cursor()
cur2 = conn.cursor()


for row in cur.execute('SELECT BIAOT,NEIR FROM G_NEWS' ):
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
    try:
        # kd = row[1].replace('\n','')
        # ti = row[2].replace('\n','')
        # tX = row[3].replace('\n','')
        # NEWS_ID = shortuuid.uuid()
        # print(NEWS_ID)
        # gpt_text = '123456'
        cur2.execute('''UPDATE GL_NEWS SET GPT3_TEXT = ? WHERE NEWS_ID = ?''', (gpt,row[0]))
        # cur2.execute('''UPDATE GL_NEWS SET GPT3_TITLE = ? WHERE NEWS_ID = ?''', (ti,row[0]))
        # cur2.execute('''UPDATE GL_NEWS SET GPT3_TEXT = ? WHERE NEWS_ID = ?''', (tX,row[0]))
        # cur2.execute('''UPDATE GL_NEWS SET GPT3_TITLE = ? WHERE GPT3_TITLE= ?''', (text,row[0]))
        conn.commit()
        print('------------------')
    except Exception as e:
        print(e)
        print('------------------')
conn.close()

#%%%%%%%%%%%%%%%%%%%%%%%%%

import time
from datetime import datetime
# from dateutil import parser

d1 = "Jan 7 2015  1:15PM"
d2 = "2015 Jan 7  1:33PM"
d3 = "3/16/23 2:42 PM"
d4 = "2023-03-20T05:56:24Z"

# If you know date format
date1 = datetime.strptime(d4, "%Y-%m-%dT%H:%M:%SZ")
s_t=time.strptime(str(date1),"%Y-%m-%d %H:%M:%S")
mkt=int(time.mktime(s_t))
print(mkt)

#%%%%%%%%%%%%%%%%%%%%
import datetime
import time
utc_data1='2023-03-31T16:00:00.000Z'
utc_date2=datetime.datetime.strptime(utc_data1,"%Y-%m-%dT%H:%M:%S.%fZ")
mkt=int(time.mktime(utc_date2))
print(mkt)


print(utc_date2)

local_date=utc_date2+datetime.timedelta(hours=8)
local_date=datetime.datetime.strftime(local_date,"%Y%m")
print(local_date)


#%%%%%%%%%%%%%%%%%%%%%%%%%%
text = """The iPhone 15 Pro is set to have the thinnest bezels on a smartphone, measuring 1.55mm thick 😳

For comparison, the iPhone 14 Pro’s bezels are 2.17mm thick

Source: @UniverseIce pic.twitter.com/p4qZrVmhwn"""

# print(gpt_translate(text))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%


# import shortuuid
# from datetime import datetime
import sqlite3 as sq3
conn = sq3.connect("D:/T_py/GOOGLE.db")

cur = conn.cursor()
# cur2 = conn.cursor()


index = []
for row in cur.execute('SELECT NEWS_ID,CONTENT,GPT3_TEXT FROM GL_NEWS' ):
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
    if row[2]=='':
        index.append(row[0])
    else:
        print('不为空')
        pass
        
conn.close()

#%%%%%%%%%%%%%%%%%%%%%%%%%%%

try:
    gpt = gpt_sum(row[1])
    print(gpt)
    # kd = row[1].replace('\n','')
    # ti = row[2].replace('\n','')
    # tX = row[3].replace('\n','')
    # NEWS_ID = shortuuid.uuid()
    # print(NEWS_ID)
    # gpt_text = '123456'
    cur2.execute('''UPDATE GL_NEWS SET GPT3_TEXT = ? WHERE NEWS_ID = ?''', (gpt,row[0]))
    # cur2.execute('''UPDATE GL_NEWS SET GPT3_TITLE = ? WHERE NEWS_ID = ?''', (ti,row[0]))
    # cur2.execute('''UPDATE GL_NEWS SET GPT3_TEXT = ? WHERE NEWS_ID = ?''', (tX,row[0]))
    # cur2.execute('''UPDATE GL_NEWS SET GPT3_TITLE = ? WHERE GPT3_TITLE= ?''', (text,row[0]))
    conn.commit()
    print('------------------')
except Exception as e:
    print(e)
    print('------------------')
    
#%%%%%%%%%%%%%%%%%%%%

import time
from datetime import datetime
def get_now_time():
    SAVE_TIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date1 = datetime.strptime(str(SAVE_TIME), "%Y-%m-%d %H:%M:%S")
    s_t=time.strptime(str(date1),"%Y-%m-%d %H:%M:%S")
    S_TIME=int(time.mktime(s_t))
    return(SAVE_TIME,S_TIME)

print(get_now_time())