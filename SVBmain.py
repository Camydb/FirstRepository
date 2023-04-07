# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 13:54:35 2023

@author: Administrator
"""

# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai




completion=openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
)
print(completion.choices[0].message.content)


#%%%%%%%%%%%%%%%%%%%%%


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
import datetime
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import openai



def gpt(text):
   

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": "Can you help me summarize a piece of news?"},
        {"role": "assistant", "content": "Sure, please provide me with the piece of news you would like me to summarize."},
        {"role": "user", "content": text}
      ]
    )

    # print(completion.choices[0].message.content)
    return(completion.choices[0].message.content)



def request_header():
    headers = {
        'User-Agent': UserAgent().random #常见浏览器的请求头伪装（如：火狐,谷歌）
        #'User-Agent': UserAgent().Chrome #谷歌浏览器
        }
    return headers

def save(db,BIAOT,ZUOZ,PINGL,NEIR,TIME,ZURL,BEIZ,GPT3):
    conn = sqlite3.connect(db)
    # print(db)
    stime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.execute(
        '''INSERT INTO G_NEWS (BIAOT,ZUOZ,PINGL,NEIR,TIME,ZURL,BEIZ,GPT3) VALUES ("{}","{}","{}","{}","{}","{}","{}","{}")'''.format(BIAOT,ZUOZ,PINGL,NEIR,stime,ZURL,BEIZ,GPT3));
    conn.commit()
    print ("记录插入成功!")
    conn.close()


def get_news(url,tx):
    # 目标新闻网址
    # goo = 'https://news.google.com/articles/CBMiUWh0dHBzOi8vd3d3LmNic25ld3MuY29tL25ld3Mvc2lsaWNvbi12YWxsZXktYmFuay1mYWlsdXJlLXdvcmxkd2lkZS1yZXBlcmN1c3Npb25zL9IBVWh0dHBzOi8vd3d3LmNic25ld3MuY29tL2FtcC9uZXdzL3NpbGljb24tdmFsbGV5LWJhbmstZmFpbHVyZS13b3JsZHdpZGUtcmVwZXJjdXNzaW9ucy8?hl=en-US&amp;gl=US&amp;ceid=US%3Aen'
    # url = 'https://www.cbsnews.com/news/silicon-valley-bank-failure-worldwide-repercussions/'
    # url = 'https://www.nytimes.com/2023/03/12/business/janet-yellen-silicon-valley-bank.html'
    # url = 'https://www.cnn.com/2023/03/13/investing/svb-panic-china-companies-tycoons-intl-hnk/index.html'
    # url = 'https://apnews.com/article/silicon-valley-bank-bailout-yellen-deposits-failure-94f2185742981daf337c4691bbb9ec1e'
    # url = 'https://www.fdic.gov/news/press-releases/2023/pr23016.html'
    news = Article(url, language='en')
    news.download()        # 加载网页
    news.parse()           # 解析网页
    print('题目：',news.title)       # 新闻题目
    # print('正文：\n',news.text)      # 正文内容      
    # print(news.publish_date) # 发布日期
    news_text = news.text.replace("\"","\'")
    news_title = news.title.replace("\"","\'")
    
    news_text = escape_string(news_text)
    news_title = escape_string(news_title)
    
    # news_authors = news.authors.replace("\"","\'")
    
    gpt_text = gpt(news_text)
    try:
        save("D:/T_py/GOOGLE.db",news_title,news.authors,tx,news_text,'',url,news.top_image,gpt_text)
    except Exception as e:
        print(e)


def twitter(soup):
    title = soup.title.text
    artical=soup.find_all(attrs={'class':'ifw3f'})
    for para in artical:
        fu = para.parent
        
        di = fu.find(attrs={'class':'js5zDf'})
        print(di.text)
        
        print(para.text)
        pt = para.text.replace("\"","\'")
        
        xiong = fu.find(attrs={'class':'eGzQsf'})
        tm = xiong.time.text
        if len(tm)<9:
            now = datetime.datetime.now().strftime('%m/%d/23')
            tm = now+' '+tm
        print(tm)
        
        try:
            conn = sqlite3.connect("D:/T_py/GOOGLE.db")
            # print(db)
            stime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            conn.execute(
                '''INSERT INTO Twitter (PINGL,PEOPLE,TIME,BJ_TIME,CLASS) VALUES ("{}","{}","{}","{}","{}")'''.format(pt,di.text,tm,stime,title));
            conn.commit()
            print ("记录插入成功!")
            conn.close()
        except Exception as e:
            print(e)
        
        print('-----------------')




url = 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lEdDVYaUJoSE1tQ3JFdEtaQXBTZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen'
# url= 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lRci1EV0JoRkJvMkVtWVI3UWRDZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen'
# url = 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2laZ2ZmdkJoR2NwNFNnWGVkcmhDZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=0'
# url = 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pKdGVudkJoR0p6cmR2cEhUWl9pZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen'
# wbdata = requests.get(url,headers=request_header(),proxies=proxies)
wbdata = requests.get(url,headers=request_header())
if wbdata.status_code == 200:
    # data = response.json()
    # 对获取到的文本进行解析
    soup = BeautifulSoup(wbdata.text,'lxml')
    # print(soup.title.text)
    # 获取文章 内容
    tx = soup.title.text
    print(tx)
    twitter(soup)
    
    js = soup.find(attrs={'jsname':'gKDw6b'})
    uurl = js.find_all(attrs={'class':'VDXfz'})
    for uu in uurl:
        try:
            surl = 'https://news.google.com/'+uu['href'][2:]
            print(surl)
            get_news(surl,tx)
            # time.sleep(3)
            # print(uu.href)
        except Exception as e:
            print(e)
        print('-----------------')


#%%%%%%%%%%%%%%%%%%%%%%%%%%


news1 = '''
Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.

Editor’s Note: Darrell Duffie is a professor of finance at Stanford University’s Graduate School of Business, and the author of “Fragmenting Markets: Post-Crisis Bank Regulations and Financial Market Liquidity,” DeGruyter, 2022. The views expressed in this commentary belong to the author. View more opinion at CNN.



CNN —

With the shocking failure of Silicon Valley Bank on Friday, I’m sure the lights are on late this weekend at the White House, Treasury, Fed and the Federal Deposit Insurance Corporation.

Darrell Duffie Stanford University

SVB, the second largest US bank ever to go under, was hit by a garden-variety bank run accelerated by a high concentration of large uninsured deposits. Yes, there were failures of risk management and regulatory supervision. And there are likely some other banks whose balance sheets have been similarly weakened by the rapid increases in interest rates, which dramatically diminished the value of Treasuries and mortgage-backed securities. According to FDIC Chair Martin Gruenberg last week, banks have yet to recognize about $620 billion of losses in market value caused by rising interest rates.

Despite the panic over SVB’s collapse, this situation isn’t likely to morph into a broader banking crisis. Since the collapse of Lehman Brothers in 2008, the largest US banks have been forced by regulators to be much more resilient. They also rely far more heavily than SVB on retail depositors, who tend to have a greater share of their deposits covered by FDIC insurance and are less prone to run at the first sign of trouble.

Of more immediate concern is the potentially systemic impact this will have on the tech sector, which has already seen mass layoffs and investments shrivel up in recent months. Close to half of all listed US venture-backed tech and health care firms were SVB customers and many of these companies were racing to line up funds to make payroll in the aftermath of the collapse.

Given US strategic technology objectives and the broader implications for national security, the government should intervene if a significant portion of these tech firms need cash to survive.

It’s possible that may not be necessary — if most of the affected tech depositors have sufficient alternative sources of cash or can be quickly restructured in bankruptcy and continue to bring their innovations to market, then the government doesn’t need to intervene with taxpayer-funded support.

If, however, a large fraction cannot survive, then it is in the US government’s own interests to step in. It can do that in a number of different ways. The SVB catastrophe could, for example, serve as a catalyst for the government to establish a new domestic industrial development bank, as proposed by Senator Chris Coons, which could provide bridge loans to the tech industry. For some tech startups, the Small Business Administration could step in with emergency loans, as was done when Covid hit in March 2020. California and the federal government each have a Technology Modernization Fund that could potentially provide grants to keep specific types of research and development alive. But these approaches may be too slow. Many tech firms that lost access to their SVB deposits may be unable to keep the lights on for long.

There are already signs that the government is taking swift action. The FDIC, the government agency charged with SVB’s workout and insuring some of its deposits, has said that insured depositors would have access to their deposits by Monday, and that it would pay uninsured depositors an “advance dividend within the next week.”

Get our free weekly newsletter Sign up for CNN Opinion’s newsletter. Join us on Twitter and Facebook

But plenty more may need to be done. The tech sector is an engine of economic growth and a key element of US national security, especially given the rivalry between the US and China. If the government decides that it needs to help the tech sector through this mess, then it will need to act quickly.
'''
# test = news.split('\n')
# for i in test:
#     if i == '':
#         test.remove(i)
# neir = []
# z = ''
# k = ''
# for t in test:
#     # print(len(t))
#     if len(z)+len(t)<4000:
#         z += k
#         z += t
#     else:
#         k = t
#         neir.append(z)
#         z = ''
# neir.append(z)

# print(len(neir))
print(gpt(news1))
# print(gpt(neir[0])+'\n'+gpt(neir[1])+'\n'+gpt(neir[2]))
# print(gpt(neir[0])+'\n'+gpt(neir[1]))
# print(gpt(neir[0])+'\n'+gpt(neir[1])+'\n'+gpt(neir[2])+'\n'+gpt(neir[3])+'\n'+gpt(neir[4])+'\n'+gpt(neir[5])+'\n'+gpt(neir[6]))
#%%%%%%%%%%%%%%%%%%%%%%%
                                 
# print(news.authors)     # 新闻作者
# print(news.keywords)    # 新闻关键词
# print(news.summary)     # 新闻摘要

# print(news.top_image) # 配图地址
# print(news.movies)    # 视频地址
# print(news.publish_date) # 发布日期
# # print(news.html)      # 网页源代码


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


import newspaper
url = 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lRci1EV0JoRkJvMkVtWVI3UWRDZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen'      # 南方网
south_paper = newspaper.build(url, language='en')    # 构建新闻源

print(south_paper.size())

#%%%%%%%%%%
# 提取源类别
for category in south_paper.category_urls():
    print(category)

# 提取源新闻网站的品牌和描述
print('品牌：',south_paper.brand)  # 品牌
print('描述：',south_paper.description) # 描述


#%%%%%%%%%%%%%%


# 查看新闻源下面的所有新闻链接
for article in south_paper.articles:
    print(article.url)

len(south_paper.articles)      # 查看新闻链接的数量，与south_paper.size()一致
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# import sqlite3
# conn = sqlite3.connect('D:/TenCen/GOOGLE.db')
# print ("数据库打开成功")
# c = conn.cursor()
# c.execute('''CREATE TABLE G_NEWS
#         (BIAOT           TEXT    NOT NULL,
#         ZUOZ            TEXT    ,
#         PINGL           TEXT    ,
#         NEIR           TEXT    ,
#         TIME           TEXT    NOT NULL,
#         ZURL           TEXT    NOT NULL,
#         BEIZ           TEXT);''')
# print ("数据表创建成功")
# conn.commit()
# conn.close()


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

import requests
from bs4 import BeautifulSoup
# import bs4, csv
# import time
# from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.common.keys import Keys
import sqlite3
from fake_useragent import UserAgent
# import threading
# import random

# from selenium.webdriver import ChromeOptions



def request_header():
    headers = {
        'User-Agent': UserAgent().random #常见浏览器的请求头伪装（如：火狐,谷歌）
        #'User-Agent': UserAgent().Chrome #谷歌浏览器
        }
    return headers

# proxies = {"http": "https://" + random.choice(lsip1) }
# print(proxies)


url= 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lRci1EV0JoRkJvMkVtWVI3UWRDZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen'
# wbdata = requests.get(url,headers=request_header(),proxies=proxies)
wbdata = requests.get(url,headers=request_header())
# wbdata = requests.get(url,headers=request_header())

if wbdata.status_code == 200:
    # data = response.json()

    # 对获取到的文本进行解析
    soup = BeautifulSoup(wbdata.text,'lxml')

    # print(soup)
    # <a class="cihWJ" href="https://twitter.com/gignacclement/status/1634536471477583874" target="_blank" jslog="95062; 5:W251bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCwiaHR0cHM6Ly90d2l0dGVyLmNvbS9naWduYWNjbGVtZW50L3N0YXR1cy8xNjM0NTM2NDcxNDc3NTgzODc0Il0=; track:click,vis" aria-label="View this tweet on Twitter"></a>

    print(soup.title.text)

    # 获取文章 内容
    artical=soup.find_all(attrs={'class':'ifw3f'})
    
    # # ss = soup.find(attrs={'name':'apub:time'})
    # # stime = ss.attrs['content']
    # u = url.split('/')[-1]
    # # print(u[:8])
    # stime =u[:8]
    # # print(day)

    # content=""    
    # for para in artical:

    #     # content+=para.text
    #     print(para.text)
    #     print('-----------------')
        
    
    # <a class="VDXfz" jsname="hXwDdf" jslog="95014; 5:W251bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCwiaHR0cHM6Ly93d3cubnl0aW1lcy5jb20vMjAyMy8wMy8xMi9idXNpbmVzcy9qYW5ldC15ZWxsZW4tc2lsaWNvbi12YWxsZXktYmFuay5odG1sIl0=; track:click,vis" href="./articles/CBMiUWh0dHBzOi8vd3d3Lm55dGltZXMuY29tLzIwMjMvMDMvMTIvYnVzaW5lc3MvamFuZXQteWVsbGVuLXNpbGljb24tdmFsbGV5LWJhbmsuaHRtbNIBVWh0dHBzOi8vd3d3Lm55dGltZXMuY29tLzIwMjMvMDMvMTIvYnVzaW5lc3MvamFuZXQteWVsbGVuLXNpbGljb24tdmFsbGV5LWJhbmsuYW1wLmh0bWw?hl=en-US&amp;gl=US&amp;ceid=US%3Aen" tabindex="-1" target="_blank" aria-hidden="true"></a>
    js = soup.find(attrs={'jsname':'gKDw6b'})
    uurl = js.find_all(attrs={'class':'VDXfz'})
    # uurl = soup.find_all(attrs={'jsname':'hXwDdf'})
    # uurl = soup.find_all('a')
    for uu in uurl:
        # content+=para.text
        try:
            print(uu['href'])
            # print(uu.href)
        except Exception as e:
            print(e)
    # print(content)
    # if len(content)==0:
    #     content='video'
    
    
    
#%%%%%%%%%%%%%%%%%%%%%%%%%%


goo = 'https://news.google.com/articles/CBMiigFodHRwczovL3d3dy50aGVndWFyZGlhbi5jb20vYnVzaW5lc3MvbGl2ZS8yMDIzL21hci8xMy9zaWxpY29uLXZhbGxleS1iYW5rLXVrLXRlY2gtc2VjdG9yLXJlc2N1ZS1oZWxwLWplcmVteS1odW50LXJpc2hpLXN1bmFrLWJ1c2luZXNzLWxpdmXSAYoBaHR0cHM6Ly9hbXAudGhlZ3VhcmRpYW4uY29tL2J1c2luZXNzL2xpdmUvMjAyMy9tYXIvMTMvc2lsaWNvbi12YWxsZXktYmFuay11ay10ZWNoLXNlY3Rvci1yZXNjdWUtaGVscC1qZXJlbXktaHVudC1yaXNoaS1zdW5hay1idXNpbmVzcy1saXZl?hl=en-US&amp;gl=US&amp;ceid=US%3Aen'


wbdata = requests.get(url,headers=request_header())
soup = BeautifulSoup(wbdata.text,'lxml')
print(soup)
print(soup.title.text)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%


import openai


completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a doctor."},
    {"role": "user", "content": "How do girls have stomachache?"}
    
    # {"role": "user", "content": text}
  ]
)

# print(completion.choices[0].message.content)
print(completion.choices[0].message.content)