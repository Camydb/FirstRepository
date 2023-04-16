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
# import logging
# logging.basicConfig(filename='D:/WS8801/errors.log', level=logging.ERROR)
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
from multiprocessing import Pool
import re
import pandas as pd
import random
import spacy


HOST="120.48.49.157"

# token = 't-g20543cGFYKVK4SE343FV4WVIOTEN2P457JJWTLC'


    


def get_CLASS_ID(url):
    # db = pymysql.connect(
    #     host=HOST, 
    #     port=3306,
    #     user='root',    #在这里输入用户名
    #     password='root123321',     #在这里输入密码
    #     charset='utf8mb4' ,
    #     database='GOOGLE'
    #     ) #连接数据库
    # cursor = db.cursor()
    
    # 创建数据库连接
    db = create_engine('mysql+pymysql://root:root123321@{}:3306/GOOGLE'.format(HOST))
    
    # 查询数据
    # df = pd.read_sql_query('SELECT * FROM table_name', engine)
    
    df = pd.read_sql_query('''SELECT THEME_URL,TH_ID FROM GL_NEWS  ''',db)
    # db.close()
    df = df.drop_duplicates('THEME_URL')#.sort_index()
    urls = list(df['THEME_URL'])
    new_url = url+'&so=1'
    if new_url in urls:
        # print("in")
        result = df.loc[df['THEME_URL'] == new_url, 'TH_ID'].iloc[0]
        print(result)
        return(result)
    else:
        result = shortuuid.ShortUUID().random(length=9)
        print('not in')
        return(result)
    



def sun_twi_title():
    # db = pymysql.connect(
    #     host=HOST, 
    #     port=3306,
    #     user='root',    #在这里输入用户名
    #     password='root123321',     #在这里输入密码
    #     charset='utf8mb4' ,
    #     database='GOOGLE'
    #     ) #连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    # cursor = db.cursor()
    # 使用pandas的read_sql函数读取数据
    db = create_engine('mysql+pymysql://root:root123321@{}:3306/GOOGLE'.format(HOST))
    df = pd.read_sql_query('''SELECT PINGL FROM Twitter  ''',db)
    # db.close()
    df = df.drop_duplicates('PINGL')#.sort_index()
    return(list(df["PINGL"]))



def sun_news_title():
    # db = pymysql.connect(
    #     host=HOST, 
    #     port=3306,
    #     user='root',    #在这里输入用户名
    #     password='root123321',     #在这里输入密码
    #     charset='utf8mb4' ,
    #     database='GOOGLE'
    #     ) #连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    # cursor = db.cursor()
    # 使用pandas的read_sql函数读取数据
    db = create_engine('mysql+pymysql://root:root123321@{}:3306/GOOGLE'.format(HOST))

    df = pd.read_sql_query('''SELECT TITLE FROM GL_NEWS  ''',db)
    # db.close()
    df = df.drop_duplicates('TITLE')#.sort_index()
    return(list(df["TITLE"]))

# print(sun_news_title())

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


def context(summary):
    """
    输入新闻的三句话总结，输出相关背景知识
    """
    prompt = """ As an experienced news editor, you need to provide explanations for certain ideas in news articles so that middle school students can better understand the news. This will help the students comprehend news stories and keep them informed about current events. Please provide background information for this news:'{}'
    """.format(summary)
    result = gpt_title(prompt)
    return result

# url = 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lkdkxYeEJoRjE4RkNSSU5pYUVpZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1'
def title_sum(url,one_tit,CLASS_ID):
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
        # news = 'Help me summarize all the news headlines in three sentences.\n\n'
        
        # key_word = "Help me extract one keyword.\n\n"
        
        df = pd.DataFrame(columns=['title', 'TIME'])
        for j in js:
            try:
                title = j.h3.text
                # new_url = 'https://news.google.com/'+j.a['href'][2:]
                new_time = j.time['datetime']
                print(title)
                # print(new_url)
                print(new_time)
                # news = news + '\n' + title
                # key_word = key_word + '\n' + title
                # jurl = j.find(attrs={'class':'ipQwMb ekueJc RD0gLb'})
                # # surl = 'https://news.google.com/'+uu['href'][2:]
                # j_title = jurl.text
                # j_url = 'https://news.google.com/'+jurl['href'][2:]
                
                # df = pd.DataFrame(columns=['title', 'TIME'])
                # for row in cur.execute('SELECT NEWS_ID,TITLE,TIME FROM GL_NEWS where TH_ID = "{}" '.format(th_id) ):
                    # df = df.append({'title': row[1], 'TIME': row[2]}, ignore_index=True)
                df = pd.concat([df, pd.DataFrame({'title': [title], 'TIME': [new_time]})], ignore_index=True)
                
                
                # print(j_title)
                # print(j_url)
                # get_news(surl,tx)
                # time.sleep(3)
                # print(uu.href)
            except Exception as e:
                # logging.error(e, exc_info=True)
                print(e)
            print('-----------------')
        # summary,title,topic,location
        two,one_title,three,location = gpt_output(df)
        print(two,title,three,location)
        
        context1 = context(two)
        img_url = ai_img(two)
        context2 = deepl(context1)
        
        print(img_url)
        
        context1 = context1.replace("\"","\'")
        context2 = context2.replace("\"","\'")
        # three = gpt_title(key_word)
        # print(two)
        # print(three)
        TH_ZH = deepl(one_title)
        KW_ZH = deepl(three)
        GT_ZH = deepl(two)
        
        
        # print(gpt_translate(th))
        print('-----------------')
        # TH_ID = shortuuid.ShortUUID().random(length=9)
        
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
                get_news(title,new_url,new_time,two,one_title,url,three,location,CLASS_ID,context1,context2,img_url,TH_ZH,KW_ZH,GT_ZH)
                # time.sleep(3)
                # print(uu.href)
            except Exception as e:
                print(e)
            print('-----------------')
    return 0




def gpt_title(text):


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

def request_header():
    headers = {
        # 'User-Agent': UserAgent().random ,#常见浏览器的请求头伪装（如：火狐,谷歌）
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
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




def deepl(text):
    try:
        prompt = '''Translate this from English to Chinese: "{}" '''.format(text)
        return(gpt_title(prompt))
        # url = 'https://api-free.deepl.com/v2/translate'
        # auth_key = 'df628d3e-e50e-be55-6ad3-a43df1fbf411:fx'
        # # text = 'Hello, world!'
        # target_lang = 'ZH'
    
        # payload = {'text': text, 'target_lang': target_lang}
        # headers = {'Authorization': f'DeepL-Auth-Key {auth_key}'}
    
        # response = requests.post(url, data=payload, headers=headers)
    
        # # print(response.json()['translations'][0]['text'])
        # return(response.json()['translations'][0]['text'])
    except Exception as e:
        print(e)
        return text



def ai_img(article):
    try:
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(article)

        # iterate over each entity in the document
        for ent in doc.ents:
            # if the entity is a location, remove it from the text
            if ent.label_ == 'GPE':
                article = article.replace(ent.text, 'it')
        response = openai.Image.create(
          prompt=article,
          n=1,
          size="512x512"
        )
        image_url = response['data'][0]['url']
        # print(image_url)
        name2 = image_url.split('?')[0].split('/')[-1]
        print(name2)
        response = requests.get(image_url)
        # path2 = "D:/WS8801/img/"+name2
        path2 = "/home/ubuntu/img/"+name2
        with open(path2, 'wb') as f:
            f.write(response.content)
        
        url = 'http://120.48.49.157:5000/chuan?name={}'.format(name2)
        files = {'file': open(path2, 'rb')}
        response = requests.get(url, files=files)
        print(response.text)
        
        return(name2)
    except Exception as e:
        print("Error:", e)
        return('')
    


# =============================================================================
# def lark(text):
#     global token
#     url = 'https://open.larksuite.com/open-apis/translation/v1/text/translate'
#     # headers = {'Authorization': 'Bearer t-g2053n6c7EF4YVHPSO3QWKJ5CWD6ULMUE3ZSKENR', 'Content-Type': 'application/json; charset=utf-8'}
#     headers = {'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json; charset=utf-8'}
#     data = {
#         "source_language": "en",
#         "text": ''' {} '''.format(text),
#         "target_language": "zh",
#         "glossary": [
#             {
#                 "from": "Lark",
#                 "to": "Lark"
#             }
#         ]
#     }
#     try:
#         response = requests.post(url, headers=headers, json=data)
#         if response.status_code==200:
#             print(response.status_code)
#             return(response.json()['data']['text'])
#         else:
#             token = get_token()
#             time.sleep(1)
#             return(text)
#     
#     except Exception as e:
#         print(e)
#         print('重新请求')
#         token = get_token()
#         print(token)
#         # print(response.text)
#         # print(text)
#         # time.sleep(1)
#         return(text)
# =============================================================================

def save(db,TITLE,AUTHOR,CONTENT,TIME,THEME,THEME_URL,GPT3_TITLE,GPT3_TEXT,NEWS_URL,PIC_URL,REMARKS,three,TH_ID,context1,context2,img_url,TH_ZH,KW_ZH,GT_ZH):
    # conn = sqlite3.connect(db)
    # print(db)
    SAVE_TIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    NEWS_ID = shortuuid.uuid()
    
    date1 = datetime.strptime(str(TIME), "%Y-%m-%dT%H:%M:%SZ")
    s_t=time.strptime(str(date1),"%Y-%m-%d %H:%M:%S")
    S_TIME=int(time.mktime(s_t))
    
    try:
        print("开始存储")
        conn = pymysql.connect(
            host=HOST, 
            port=3306,
            user='root',    #在这里输入用户名
            password='root123321',     #在这里输入密码
            charset='utf8mb4' ,
            database='GOOGLE'
            ) #连接数据库
        cur = conn.cursor()
        
 
        # TH_ZH = deepl(THEME)
        # KW_ZH = deepl(three)
        # GT_ZH = deepl(GPT3_TITLE)
        
        ZH_CN =  deepl(GPT3_TEXT)
        T_ZH = deepl(TITLE)
        print("翻译完成")
        # T_ZH,TH_ZH,KW_ZH,GT_ZH,ZH_CN
        sensitive = str(TITLE+THEME+three+GPT3_TITLE+GPT3_TEXT+REMARKS).lower()
        if "china" in sensitive or "taiwan" in sensitive or "jinping" in sensitive:
            print ("敏感数据")
            pass
        else:
            cur.execute(
                '''INSERT INTO GL_NEWS (NEWS_ID,TITLE,AUTHOR,CONTENT,TIME,S_TIME,SAVE_TIME,THEME,KEY_WORD,THEME_URL,GPT3_TITLE,GPT3_TEXT,NEWS_URL,PIC_URL,REMARKS,TH_ID,T_ZH,TH_ZH,KW_ZH,GT_ZH,ZH_CN,context,context_ZH,AI_img) 
                VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'''.format(NEWS_ID,TITLE,AUTHOR,CONTENT,TIME,S_TIME,SAVE_TIME,THEME,three,THEME_URL,GPT3_TITLE,GPT3_TEXT,NEWS_URL,PIC_URL,REMARKS,TH_ID,T_ZH,TH_ZH,KW_ZH,GT_ZH,ZH_CN,context1,context2,img_url));
            conn.commit()
            print ("记录插入成功!")
        
        
        
        # try:
        #     cur.execute('''UPDATE GL_NEWS SET T_ZH = ?,TH_ZH = ?,KW_ZH = ?,GT_ZH = ?,ZH_CN = ? WHERE NEWS_ID = ?''', (T_ZH,TH_ZH,KW_ZH,GT_ZH,ZH_CN,NEWS_ID))
        #     conn.commit()
        # except Exception as e:
        #     conn.rollback()
        #     print(e)
        
        
    except Exception as e:
        conn.rollback()
        print(e)
    conn.close()
    

def get_news(title,news_url,new_time,two,one_tit,one_url,three,location,TH_ID,context1,context2,img_url,TH_ZH,KW_ZH,GT_ZH):
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
    location = location.replace("\"","\'")
    
    
    # news_text = escape_string(news_text)
    # news_title = escape_string(news_title)
    
    # news_authors = news.authors.replace("\"","\'")
    sql_title = sun_news_title()
    if news_title not in sql_title:
    
        gpt_text = gpt_sum(news_text)
        gpt_text = gpt_text.replace("\"","\'")
        
        # gpt_text = ''
        if news_text!='':
            try:
                save("D:/T_py/GOOGLE.db",news_title,news.authors,news_text,new_time,one_tit,one_url,two,gpt_text,news_url,news.top_image,location,three,TH_ID,context1,context2,img_url,TH_ZH,KW_ZH,GT_ZH)
                # save(               db,TITLE,     AUTHOR,      CONTENT,  TIME,    THEME,  THEME_URL,GPT3_TITLE,GPT3_TEXT,NEWS_URL,PIC_URL,REMARKS)
            except Exception as e:
                print(e)
        else:
            print('no news')
            pass
    else:
        print("重复新闻")



def twitter(url):
    CLASS_ID = get_CLASS_ID(url)
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
            
            
            # conn = sqlite3.connect("D:/T_py/GOOGLE.db")
            # print(db)
            stime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # cursor = conn.cursor()
            # ZH_CN = lark(pt).replace("\"","\'")
            # P_ZH = lark(di.text).replace("\"","\'")
            
            
            twi_title = sun_twi_title()
            conn = pymysql.connect(
                host=HOST, 
                port=3306,
                user='root',    #在这里输入用户名
                password='root123321',     #在这里输入密码
                charset='utf8mb4' ,
                database='GOOGLE'
                ) #连接数据库
            cur = conn.cursor()
            
            
            print("++++++++++++++")
            print(pt)
            print("++++++++++++++")
            if pt not in twi_title:
                try:
                    ZH_CN = deepl(pt).replace("\"","\'")
                    P_ZH = deepl(di.text).replace("\"","\'")
    
                    cur.execute(
                        '''INSERT INTO Twitter (PINGL,ZH_CN,PEOPLE,P_ZH,TIME,BJ_TIME,S_TIME,CLASS,CLASS_URL,CLASS_ID) VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'''.format(pt,ZH_CN,di.text,P_ZH,tm,stime,date[:-3],title,url,CLASS_ID));
                    conn.commit()
                    print ("记录插入成功!")
                except Exception as e:
                    conn.rollback()
                    print(e)
            else:
                print("评论重复")
                pass
            conn.close()  
            print('-----------------')
        return (title,CLASS_ID)

# so = 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lVdjZQX0JoSERzdzZ4bmJLeVJTZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1'
# one_tit = "E3 2023 canceled"
# title_sum(so,one_tit)


#%%%%%%%%%%%%%%%%%%

url =   'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen'
# url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen'




while True:

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
                one_tit,CLASS_ID = twitter(surl)
                print(one_tit)
                
                so = surl + '&so=1'
                urls.append(so)
                # time.sleep(3)
                # print(so)
                print('-+-+-+-+-+-+-+-+-+-+-+')
                title_sum(so,one_tit,CLASS_ID)
                # print('-+-+-+-+-+-+-+-+-+-+-+')
            except Exception as e:
                print(e)
            print('-----------------')
            
    print(urls)
    print(len(urls))


#%%%%%%%%%%%%%%%%%%%%

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
cur.execute("SELECT GPT3_TITLE, context, AI_img FROM Gl_NEWS")
rows = cur.fetchall()

for row in rows:
    if row[0] not in texts:
        # print(row[0])
        texts.append(row[0])
        con = context(row[0])
        con = con.replace("\"","\'")
        print(con)
        img = ai_img(row[0])
        print(img)
        cur1.execute('''UPDATE Gl_NEWS SET context = "{}",AI_img = "{}" WHERE GPT3_TITLE= "{}" '''.format(con,img,row[0]))
        print('----------------------')
        db.commit()
    #     print("不为空")
db.close()
print(len(texts))
# text_s = list(set(texts))

# s_urls = split_list(text_s,10)
# print(len(text_s))
#%%%%%%%%%%%%%%%%%%%%

reversed_list = text_s[::-1]
for t in reversed_list:
    tx = t[:-5]
    # print(tx)
    try:
        one_tit,CLASS_ID,code = twitter(t)
        print(one_tit,CLASS_ID,code)
    except Exception as e:
        print(e)

#%%%%%%%%%%%%%%

ut = 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pBenZMX0JoR2pUWC04cjVVamZDZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen'

one_tit,code = twitter(ut)
# print(one_tit)
print(one_tit,code)

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
# import threading
# import requests


df = pd.read_sql('''SELECT THEME_URL,TH_ID FROM GL_NEWS''', conn)
# '''select PEOPLE,PINGL,TIME,ZH_CN from Twitter WHERE CLASS like "%{}%"  '''.format(word)
# 关闭连接
conn.close()
df = df.drop_duplicates('THEME_URL')
# li = list(df['THEME_URL'])
# li = set(li)
print(len(df))
#%%%%%%%%%%%%%%%%%
import sqlite3 as sq3
conn = sq3.connect("D:/T_py/GOOGLE.db")
cur = conn.cursor()
cur2 = conn.cursor()

# TH = {}
# for row in cur.execute('SELECT THEME_URL,TH_ID FROM GL_NEWS' ):
for index, row in df.iterrows():
    print(row['THEME_URL'], row['TH_ID'])
# for key, value in SUM.items():
    # print(key, value)
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
        # TH[row[0][:-5]]=row[1]
        # T1 = row[1].replace("\\","")
        # T2 = row[2].replace("\\","")
        # kd = row[1].replace('\n','')
        # ti = row[2].replace('\n','')
        # tX = row[3].replace('\n','')
        # NEWS_ID = shortuuid.uuid()
        # print(NEWS_ID)
        # gpt_text = '123456'
        cur2.execute('''UPDATE Twitter SET CLASS_ID = ? WHERE CLASS_URL = ?''', (row['TH_ID'],row['THEME_URL']))
        # cur2.execute('''UPDATE GL_NEWS SET ONE_TITLE = ? WHERE TH_ID = ?''', (value[1],key))
        # cur2.execute('''UPDATE GL_NEWS SET KEY_WORD= ? WHERE TH_ID = ?''', (value[2],key))
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
print(TH)
#%%%%%%%%%%%%%%%%%%%%%%%%%

import sqlite3 as sq3
conn = sq3.connect("D:/T_py/GOOGLE.db")

cur = conn.cursor()
cur2 = conn.cursor()


for row in cur.execute('SELECT CLASS_URL,CLASS_ID FROM Twitter' ):
# for key, value in SUM.items():
    if row[1] is None:
        try:
            # TH[row[0]]=row[1]
      
            cur2.execute('''UPDATE Twitter SET CLASS_ID = ? WHERE CLASS_URL= ?''', (TH[row[0]],row[0]))
            conn.commit()
            print('------------------')
        except Exception as e:
            print(e)
            print('------------------')
conn.close()




#%%%%%%%%%%%%%%%%%%%%%%

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
import pandas as pd

SUM = {}

def gpt_sum(th_id):
    global SUM
    df = pd.DataFrame(columns=['title', 'TIME'])
    try:
        conn = sq3.connect("D:/T_py/GOOGLE.db")
    
        cur = conn.cursor()
        # cur2 = conn.cursor()
        # th_id = '4V7dyxM9x'
        
        index = ''
        # for row in cur.execute('SELECT NEWS_ID,CONTENT,GPT3_TEXT FROM GL_NEWS' ):
        df = pd.DataFrame(columns=['title', 'TIME'])
        for row in cur.execute('SELECT NEWS_ID,TITLE,TIME FROM GL_NEWS where TH_ID = "{}" '.format(th_id) ):
            # df = df.append({'title': row[1], 'TIME': row[2]}, ignore_index=True)
            df = pd.concat([df, pd.DataFrame({'title': [row[1]], 'TIME': [row[2]]})], ignore_index=True)
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
            # if row[2]=='':
            #     index.append(row[0])
            # else:
            #     print('不为空')
            #     pass
            # print(row[1],row[2])
            # index = index + row[1] +'\n'
            # index = index + row[2] +'\n'
                
        conn.close()
        
        print(df)
        
        
        

        
        
        # 几句话总结
        prompt1 = """You are an experienced news editor at some news agency and your readers are first-year college students. Now some news just happened and you can read all the different titles other news outlets wrote about this news. Can you synthesize all the information provided by those titles and summarize them to first year college students? Output result: News summarized in three sentences.
        Here is the news with "title" and "time":'''
        {}
        '''
        """.format(index)
        # 一句话标题
        prompt2 = """You are an experienced news editor at some news agency and your readers are first-year college students. Now some news just happened and you can read all the different titles other news outlets wrote about this news. Can you synthesize all the information provided by those titles and summarize them to first year college students? Output result: News summarized into one news title.
        Here is the news with "title" and "time":'''
        {}
        '''
        """.format(index)
        # 关键词，放在详情页
        prompt3 = """You are an experienced news editor at some news agency and your readers are first-year college students. Now some news just happened and you can read all the different titles other news outlets wrote about this news. Can you synthesize all the information provided by those titles and summarize them to first year college students? Output result: Express the central topic in 2 words.
        Here is the news with "title" and "time":'''
        {}
        '''
        """.format(index)
        
        # title_sum = gpt_title(prompt1)
        # time.sleep(2)
        # one_sum = gpt_title(prompt2)
        # time.sleep(2)
        # key_word = gpt_title(prompt3)
        
        # SUM[th_id]=[title_sum,one_sum,key_word]
        return df
    except Exception as e:
        print(e)

# gpt_sum('3fqM5ocNZ')
# print(SUM)
id_list = ['4V7dyxM9x', '5pBmG6Zxv', '3wZYs2Lrt', '9rbx4pJVZ', 'sqRMJNpdE', '3oNsgivGU', '3UNP65vM9', 'RVoHyPAfj', 'KjAe7fmEF', '39r2XSy4q', 'FwmBp73h5', 'KH3kj8rxP', 'DMSszvs3E', '5z93SnLqC', '5Q96oK8Zx', 'nXTbxySax', '3ptcHcK3Y', 'SiFtbMrxc', '3MzSG2X4B', '4Fm2SY898', '5DdBar6PW', '36NVg8frh', '5wwh4rgBE', '3TBN2AD9e', '5SW2bqi6X', '34yYCFiyH', '3GTw25uzV', 'mnZcFKENV', '5cUSvpUj9', '5Eq2fE4jm', '3MKxD6j6q', '5PCb4QifT', '3oLrj49SK', '4PtYPdBoA', '3Nk997d2q', '4z2YFd3yi', '3AHQDuycc', 'UgY6c6Lja', 'y6Bs2Y4Wv', '5om2ahBmS', 'XTWrgzybp', '42huTLgsD', '4EkCgfGoP', 'VvhNMmGEv', '57gJLTtna', '4TgAFzqK4', 'PUXWXMpew', '345y9VX96', '3VsezmVJB', 'hx37w8WDc', '4oxWpR4M2', '4hXfDVRWL', 'QjZLffGGW', 'JhP3HBFA2', '53iJj3jT2', 'YX8oVf92Z', '48hADw2Kn', '5WGuST9eM', '3ZyfL2qFo', '3ghjJi5cP', '39FJeQ44B', '4o3okNJTf', '3yjEua5FU', '3MEefX2UW', '5SUDwh7vy', 'usm4EBq2H', '3xv3Qywdw', '3aTsrkvLJ', '4Mdg2AZMT', '4F9pPz9eH', '5gzDTAEwK', '5KFtCXGqW', '5VgXU3QKK', '44V3B5a5N', '4EZWDH7KV', 'NkuMUFukz', 'q3GtNeqAh', '3ztJ3vXG9', '5WzJ4wEX2', '5fBvRv8i8', '3fqM5ocNZ', '4vosLYXnv', '5TEWHMiRj', '4qqm2qma4', 'WsT3QRhNp', '58ZiupNUT', '5mvuccLQs', '4pUHiJKUL', '32wmRtxUz', '3zwmZ3jKP', '4hH5LWmLy', 'mVzh7BtyD', '5pMRSheMw', '6nenfTB7J', '3svuT8tHP', '4uVivNR5H', 'd5yjrvi2q', '5DpFbLpqG', '3K9j6De3U', '5en44rfzH', '5stJhr2YM', 'ZasueNgBv', 'uauz2vLva', '4hw9YJNoC']
# s_id = split_list(id_list,2)

yyy = gpt_sum('5pBmG6Zxv')

print(yyy)

#%%%%%%%%%%%%%%%%%


# TF = {}
# import shortuuid
import threading
def fetch_url(urls):
    # global TF
    for t in urls:
        try:
            # lang = langchain(t)
            # la = shortuuid.ShortUUID().random(length=9)
            # print(la)
            gpt_sum(t)
            # print(la)
            # TF[t]=la
        except Exception as e:
            print(e)
            time.sleep(3)
        

threads = []

# create 10 threads
for urls in s_id:
    t = threading.Thread(target=fetch_url, args=(urls,))
    threads.append(t)
    t.start()

# wait for all threads to complete
for t in threads:
    t.join()

#%%%%%%%%%%%%%%%%%%%%%%%%%%%

print(SUM)


#%%%%%%%%%%%%%%%%%%%%%%%
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
    
print(gpt_output(yyy))

#%%%%%%%%%%%%%%%%%%%%

print (yyy)


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

#%%%%%%%%%%%%%%%%%%


# 几句话总结
prompt1 = """You are an experienced news editor at some news agency and your readers are first-year college students. Now some news just happened and you can read all the different titles other news outlets wrote about this news. Can you synthesize all the information provided by those titles and summarize them to first year college students? Output result: News summarized in three sentences.
Here is the news with "title" and "time":'''
{}
'''
""".format(df.to_string())
# 一句话标题
prompt2 = """You are an experienced news editor at some news agency and your readers are first-year college students. Now some news just happened and you can read all the different titles other news outlets wrote about this news. Can you synthesize all the information provided by those titles and summarize them to first year college students? Output result: News summarized into one news title.
Here is the news with "title" and "time":'''
{}
'''
""".format(df.to_string())
# 关键词，放在详情页
prompt3 = """You are an experienced news editor at some news agency and your readers are first-year college students. Now some news just happened and you can read all the different titles other news outlets wrote about this news. Can you synthesize all the information provided by those titles and summarize them to first year college students? Output result: Express the central topic in 2 words.
Here is the news with "title" and "time":'''
{}
'''
""".format(df.to_string())

# df格式：

#%%%%%%%%%%%%%%%%%


import json

import requests


def tranlate(source, direction):
    url = "http://api.interpreter.caiyunai.com/v1/translator"

    # WARNING, this token is a test token for new developers,
    # and it should be replaced by your token
    token = "3975l6lr5pcbvidl6jl2"

    payload = {
        "source": source,
        "trans_type": direction,
        "request_id": "demo",
        "detect": True,
    }

    headers = {
        "content-type": "application/json",
        "x-authorization": "token " + token,
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    return json.loads(response.text)["target"]


source = ["Lingocloud is the best translation service.", "彩云小译は最高の翻訳サービスです"]
target = tranlate(source, "auto2zh")

print(target)


#%%%%%%%%%%%%
TITLE = 'fsf'
THEME ='efsdCtTAIWANinaf'

sensitive = str(TITLE+THEME).lower()
if "china" in sensitive or "taiwan" in sensitive:
    print ("敏感数据")
    pass
else:
    
    print ("记录插入成功!")
    
#%%%%%%%%%%%%%%%%%


conn = pymysql.connect(
    host=HOST, 
    port=3306,
    user='root',    #在这里输入用户名
    password='root123321',     #在这里输入密码
    charset='utf8mb4' ,
    database='USER'
    ) #连接数据库
cur = conn.cursor()

userID = '123qwq'
# path,user_name,userID
cur.execute('''UPDATE personal_information SET HS_url = "{}",nick_name = "{}"  WHERE app_ID = "{}" '''.format(userID,userID,userID))
conn.commit()
conn.close()

#%%%%%%%%%%%%%%%%%%%%
usrtID = 'Lw7CH4upxDy7tzDS9XChsg'

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
for row in cur.execute('SELECT app_ID,HS_url,nick_name FROM personal_information'):
    if row[0] == usrtID:
        path = row[1]
        nick_name = row[2]
        
for row in cur.execute('SELECT User_ID,HS_url,Name FROM apple_user'):
    if row[0] == usrtID:
        path = row[1]
        nick_name = row[2]