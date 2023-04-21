from sqlalchemy import create_engine
import pymysql
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
# from multiprocessing import Pool
import re
import pandas as pd
import random
import spacy
# HOST="120.48.49.157"

# token = 't-g20543cGFYKVK4SE343FV4WVIOTEN2P457JJWTLC'

# openai.api_key = "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"

url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen'
# url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen'


print('OK')

# while True:

urls = []
wbdata = requests.get(url)


#%%%%%%%%%%%%%%%%%
if wbdata.status_code == 200:
    # data = response.json()
    # 对获取到的文本进行解析
    soup = BeautifulSoup(wbdata.text, 'lxml')
    # print(soup.title.text)
    # 获取文章 内容
    # tx = soup.title.text
    # print(tx)
    # twitter(soup)

    lj = soup.find_all(attrs={'aria-label': 'Full Coverage'})

    # js = soup.find(attrs={'jsname':'gKDw6b'})
    # uurl = js.find_all(attrs={'class':'VDXfz'})
    for uu in lj:
        try:
            surl = 'https://news.google.com/' + uu['href'][2:]
            print(surl)
            # get_news(surl,tx)
            # one_tit, CLASS_ID = twitter(surl)
            # print(one_tit)

            so = surl + '&so=1'
            # urls.append(so)
            # time.sleep(3)
            print(so)
            # print('-+-+-+-+-+-+-+-+-+-+-+')
            # title_sum(so, one_tit, CLASS_ID)
            # print('-+-+-+-+-+-+-+-+-+-+-+')
        except Exception as e:
            print(e)
        print('-----------------')

print(urls)
print(len(urls))


#%%%%%%%%%%%%%%%%%%%%%%%%%
def request_header():
    headers = {
        # 'User-Agent': UserAgent().random ,#常见浏览器的请求头伪装（如：火狐,谷歌）
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        #'User-Agent': UserAgent().Chrome #谷歌浏览器
        }
    return headers

url = 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2ozdFphbEJ4RkRqN3BqYkxXY1p5Z0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1'
# def title_sum(url, one_tit, CLASS_ID):
wbdata = requests.get(url, headers=request_header())
if wbdata.status_code == 200:
    # data = response.json()
    # 对获取到的文本进行解析
    soup = BeautifulSoup(wbdata.text, 'lxml')
    # print(soup.title.text)
    # 获取文章 内容
    # tx = soup.title.text
    # print(tx)
    # twitter(soup)
    # lj = soup.find_all(attrs={'aria-label':'Full Coverage'})
    js = soup.find_all(attrs={'class': 'xrnccd'})
    # uurl = js.find_all(attrs={'class':'VDXfz'})
    # news = 'Help me summarize all the news headlines in three sentences.\n\n'

    # key_word = "Help me extract one keyword.\n\n"

    df = pd.DataFrame(columns=['title', 'TIME'])
    # for j in js:
    #     try:
    #         title = j.h3.text
    #         # new_url = 'https://news.google.com/'+j.a['href'][2:]
    #         new_time = j.time['datetime']
    #         print(title)
    #         # print(new_url)
    #         print(new_time)
    #         # news = news + '\n' + title
    #         # key_word = key_word + '\n' + title
    #         # jurl = j.find(attrs={'class':'ipQwMb ekueJc RD0gLb'})
    #         # # surl = 'https://news.google.com/'+uu['href'][2:]
    #         # j_title = jurl.text
    #         # j_url = 'https://news.google.com/'+jurl['href'][2:]
    #
    #         # df = pd.DataFrame(columns=['title', 'TIME'])
    #         # for row in cur.execute('SELECT NEWS_ID,TITLE,TIME FROM GL_NEWS where TH_ID = "{}" '.format(th_id) ):
    #         # df = df.append({'title': row[1], 'TIME': row[2]}, ignore_index=True)
    #         df = pd.concat([df, pd.DataFrame({'title': [title], 'TIME': [new_time]})], ignore_index=True)
    #
    #         # print(j_title)
    #         # print(j_url)
    #         # get_news(surl,tx)
    #         # time.sleep(3)
    #         # print(uu.href)
    #     except Exception as e:
    #         # logging.error(e, exc_info=True)
    #         print(e)
    #     print('-----------------')


    for j in js:
        try:
            title = j.h3.text
            new_url = 'https://news.google.com/' + j.a['href'][2:]
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
            img = j.img['src']
            print(img)
            # get_news(title, new_url, new_time, two, one_title, url, three, location, CLASS_ID, context1, context2,
            #          img_url, TH_ZH, KW_ZH, GT_ZH, CT_ID)
            # time.sleep(3)
            # print(uu.href)
        except Exception as e:
            print(e)
        print('-----------------')
# return 0


#%%%%%%%%%%%%%%%%%%%%%%

from sqlalchemy import create_engine,text

# 创建一个数据库引擎对象，连接数据库
engine = create_engine('mysql+pymysql://admin:Aa123321@{}:3306/GOOGLE'.format("database-1.cwrdah6vau2j.us-east-1.rds.amazonaws.com"))

# 执行一些操作
# conn = engine.connect()
# result = conn.execute('SELECT * FROM Twitter')
# for row in result:
#     print(row)

with engine.connect() as conn:
    result = conn.execute(text('SELECT * FROM Twitter'))
    for row in result:
        print(row)

# 关闭连接
conn.close()