# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 19:29:47 2023

@author: amy
"""

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
import bs4, csv
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import sqlite3
from fake_useragent import UserAgent
import threading
import random
import urllib.parse
from selenium.webdriver import ChromeOptions
from datetime import datetime

TUI = []

def save(name,content,talk,send,like,view,url,stime,key_word):
    conn = sqlite3.connect("D:/T_py/TWITTER.db")
    # print(db)
    save_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # NEWS_ID = shortuuid.uuid()
    # date1 = datetime.strptime(str(TIME), "%Y-%m-%dT%H:%M:%SZ")
    # s_t=time.strptime(str(date1),"%Y-%m-%d %H:%M:%S")
    # S_TIME=int(time.mktime(s_t))
    name = name.replace('\"','\'')
    content = content.replace('\"','\'')
    
    try:
        conn.execute(
            '''INSERT INTO twitter_url (name,content,talk,send,like,view,url,time,save_time,key_word) VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'''.format(name,content,talk,send,like,view,url,stime,save_time,key_word));
        conn.commit()
        print ("记录插入成功!")
    except Exception as e:
        conn.rollback()
        print(e)
    conn.close()
    
             # name,url,stime,text,key_word,view
def SAY_save(name,text,view,stime,url,key_word):
    conn = sqlite3.connect("D:/T_py/TWITTER.db")
    # print(db)
    save_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # NEWS_ID = shortuuid.uuid()
    # date1 = datetime.strptime(str(TIME), "%Y-%m-%dT%H:%M:%SZ")
    # s_t=time.strptime(str(date1),"%Y-%m-%d %H:%M:%S")
    # S_TIME=int(time.mktime(s_t))
    
    try:
        conn.execute('''INSERT INTO twitter_say (name,text,view,on_time,save_time,url,key_word) VALUES ("{}","{}","{}","{}","{}","{}","{}")'''.format(name,text,view,stime,save_time,url,key_word));
        conn.commit()
        print ("记录插入成功!")
    except Exception as e:
        conn.rollback()
        print(e)
    conn.close()

def request_header():
    headers = {
        # 'User-Agent': UserAgent().random #常见浏览器的请求头伪装（如：火狐,谷歌）
        'User-Agent': UserAgent().Chrome #谷歌浏览器
        }
    return headers

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
#%%%%%%%%%%%%%%%%%%%%


import sqlite3 as sq3
import time

db = sq3.connect("D:/T_py/TWITTER.db")

cur = db.cursor()
cur2 = db.cursor()

texts = []
for row in cur.execute('SELECT view,url,key_word FROM twitter_url' ):
# for row in cur.execute('SELECT GPT3_TEXT FROM Gl_NEWS' ):
# for row in cur.execute('SELECT GPT3_TITLE FROM Gl_NEWS' ):
# for row in cur.execute('SELECT KEY_WORD FROM Gl_NEWS' ):
# for row in cur.execute('SELECT TITLE FROM Gl_NEWS' ):
    li = [row[1],row[2]]
    if li not in texts:
        try:
            cur2.execute('''UPDATE twitter_say SET key_word = ? WHERE url = ?''', (row[2],row[1]))
            db.commit()
        except Exception as e:
            db.rollback()
            print(e)
        # if row[1] is None:
        # li = [row[1],row[2]]
        # print(li)
        # texts.append(li)
    # else:
    #     print("不为空")
db.close()

# text_s = list(set(texts))

# s_urls = split_list(text_s,20)
# print(len(text_s))
# print(len(s_urls[0]))
# print(texts)

#%%%%%%%%%%%%%%%%%%%%%%%


def ping(pus):
    global TUI
    # 实例化对象
    option = ChromeOptions()
    # option.add_experimental_option('excludeSwitches',['enable-automation'])# 开启实验性功能
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    option.add_argument('--blink-settings=imagesEnabled=false')
    # 去除特征值
    # option.add_argument("--disable-blink-features=AutomationControlled")
    # ipurl = 'https://dev.kdlapi.com/api/getproxy/?secret_id=oddm05z4s2t2j338op8m&num=100&protocol=2&method=1&an_ha=1&quality=1&signature=vce2g38s38udywrrld036xgqo72mn012&sep=aa'
    # response = requests.get(url=ipurl, headers=request_header())
    # rs=response.text
    # lsip1 = rs.split("aa")
    
    browser = webdriver.Chrome(options=option)
    
    # # 修改get方法
    # script = '''object.defineProperty(navigator,'webdriver',{undefinedget: () => undefined})'''
    # #execute_cdp_cmd用来执行chrome开发这个工具命令
    # browser.execute_cdp_cmd("page.addscriptToEvaluateonNewDocument",{"source": script})
    
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator,"webdriver",{get: () => undefined})'
    })
    browser.get ('https://www.google.com/')
    time.sleep(5)
    
    
    
    # for url in text_s:
    # url = 'https://twitter.com/MayaA62580468/status/1640636787294093312'
    for pu in pus:
        browser.get (pu)
        wait = WebDriverWait (browser, 10)
    
        time.sleep(3)
        soup = BeautifulSoup(browser.page_source,'lxml')
        # print(soup.title)
        
        # lj = soup.find_all(attrs={'class':'css-1dbjc4n'})
        a = soup.find_all('time')
        
        # js = soup.find(attrs={'jsname':'gKDw6b'})
        # uurl = js.find_all(attrs={'class':'VDXfz'})
        for uu in a:
            try:
                # surl = 'https://news.google.com/'+uu['href'][2:]
                # print(uu["href"])
                stime = uu["datetime"]
                print(stime)
                name = uu.parent.parent.parent.parent.parent
                name = name.text.split("·")[0]
                print(name)
                print('+++++++++++++')
                replace = uu.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent
                # print(replace.text)
                txt = replace.find_all('span')
                ds = []
                for t in txt:
                    if '@' not in t.text:
                        ds.append(t.text)
                DD = max(ds, key=len)
                print(DD)
                print('+++++++++++++')
                # print(replace.find_all('span')[13].text)
                
                at = replace.find_all(attrs={'class':'css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0'})
                view = at[-1].text
                print(view)
                
                # say = uu.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent
                # print(say.text)
                # name = fu["href"].split("/")[1]
                # print(name)
                # xk = "https://twitter.com"+fu["href"]
                # print(xk)
                # # uu['href']
                # # so = surl + '&so=1'
                # # urls.append(so)
                # save(name,xk,stime,k)
                key_word = ''
                
                li = [name,DD,view,stime,pu,key_word]
                if li not in TUI:
                    TUI.append(li)
                    # SAY_save(name,DD,view,stime,url,key_word)
            except Exception as e:
                print(e)
            print('----------------------------------------')


#%%%%%%%%%%%%


time.sleep(5)
br = browser.find_element(By.XPATH,'//*[contains(@id,"react-root")]')
say = br.find_elements(By.XPATH,'//*[contains(@id,"id__")]/span')
name = br.find_elements(By.XPATH,'//*[contains(@id,"id__")]/div[1]/div/a/div/div[1]/span/span')
ti = br.find_elements(By.TAG_NAME,'time')

# 使用 zip 函数将多个列表打包成元组
zipped = zip(say, name, ti)

# 使用列表推导式生成新的列表
new_list = [[s.text, n.text, t.get_attribute('datetime')] for s, n, t in zipped]

# new_list = [[say[i].text, name[i].text, ti[i].get_attribute('datetime')] for i in range(len(say))]
print(new_list)

# for lis in new_list:
#     SAY_save(lis[1],url,lis[2],lis[0])


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



soup = BeautifulSoup(browser.page_source,'lxml')
# print(soup)
# <span class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0">South Korea is also one of the most racist countries ever. You say this but you're most likely not from or have never been to South Korea</span>
# lj = soup.find_all(attrs={'class':'css-1dbjc4n'})
lj = soup.find_all(attrs={'class':'css-1dbjc4n'})


# a = soup.find_all('span')
# js = soup.find(attrs={'jsname':'gKDw6b'})
# uurl = js.find_all(attrs={'class':'VDXfz'})


for uu in lj:
    try:
        a = uu.find(attrs={'class':'css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0'})
        
        pl = a.txt
        if pl !='':
            print(pl)
        # surl = 'https://news.google.com/'+uu['href'][2:]
        # print(uu["href"])
        # stime = uu["datetime"]
        # print(stime)
        # fu = uu.parent
        # name = fu["href"].split("/")[1]
        # print(name)
        # xk = "https://twitter.com"+fu["href"]
        # print(xk)
        # uu['href']
        # so = surl + '&so=1'
        # urls.append(so)
        # save(name,xk,stime,k)
        print('-----------------')
    except Exception as e:
        print(e)
        pass
        # //*[@id="id__3okry5khnl9"]/span
        # //*[@id="id__pi8xix8htp"]/div[1]/div/a/div/div[1]/span/span
    # //*[@id="id__2ehuooqcd2l"]/span
    # //*[@id="id__i1933a1yyyl"]/span/text()
    # //*[@id="id__48u3vhgkfsc"]/div[1]/div/a/div/div[1]/span/span
    # //*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[21]/div/div/article/div/div/div[2]/div[2]
#%%%%%%%%%%%%%%%%%%%%%%%%%%
# import re
# soup = BeautifulSoup(browser.page_source, 'html.parser')
# pattern = re.compile(r'id__.*')
for sp in browser.find_elements(By.XPATH,'//*[contains(@id,"id__")]/span'):
    try:
        print(sp.text)
        siblings_texts = sp.find_elements(By.XPATH, 'preceding-sibling::*/text()')
        for text in siblings_texts:
            print(text)
    except Exception as e:
        print(e)
    
    # fu = span.parent
    print('-----------')



#%%%%%%%%%%%%%%%%%%%%%%%%%%%


br = browser.find_element(By.XPATH,'//*[contains(@id,"react-root")]/div/div/div[2]/main/div/div/div/div/div/section/div/div')

say = br.find_elements(By.XPATH,'//*[contains(@id,"id__")]/span')
name = br.find_elements(By.XPATH,'//*[contains(@id,"id__")]/div[1]/div/a/div/div[1]/span/span')
ti = br.find_elements(By.TAG_NAME,'time')
new_list = [[say[i].text, name[i].text, ti[i].get_attribute('datetime')] for i in range(len(say))]
print(new_list)
# for t in ti:
#     print(t.get_attribute('datetime'))

    
# result = {}
# for s, n in zip(say, name):
#     result[s.text] = n.text
# print(result)
    # # fu = span.parent
    # print('-----------')

new_list = [[say[i].text, name[i].text, ti[i].get_attribute('datetime')] for i in range(len(say))]
print(new_list)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%

import sqlite3 as sq3
# import pandas as pd
# import time

db = sq3.connect("D:/T_py/GOOGLE.db")
# df = pd.read_sql("SELECT GPT3_TEXT FROM GL_NEWS" , db)
cur = db.cursor()

texts = []
for row in cur.execute('SELECT KEY_WORD FROM Gl_NEWS' ):
# for row in cur.execute('SELECT GPT3_TEXT FROM Gl_NEWS' ):
# for row in cur.execute('SELECT GPT3_TITLE FROM Gl_NEWS' ):
# for row in cur.execute('SELECT KEY_WORD FROM Gl_NEWS' ):
# for row in cur.execute('SELECT TITLE FROM Gl_NEWS' ):
    # sql = "SELECT * FROM table_name ORDER BY id DESC LIMIT 1000"
    # if row[1] is None:
    texts.append(row[0])
    # else:
    #     print("不为空")
db.close()
text_s = list(set(texts))
print(text_s)
print(len(text_s))

s_urls = split_list(text_s,10)

#%%%%%%%%%%%%%%%%%%%%%%%%%%
# keys = ['NATO Membership','Human Rights']

def tuiwen(keys):
    global TUI
    # 实例化对象
    option = ChromeOptions()
    # option.add_experimental_option('excludeSwitches',['enable-automation'])# 开启实验性功能
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    # 去除特征值
    # option.add_argument("--disable-blink-features=AutomationControlled")
    # ipurl = 'https://dev.kdlapi.com/api/getproxy/?secret_id=oddm05z4s2t2j338op8m&num=100&protocol=2&method=1&an_ha=1&quality=1&signature=vce2g38s38udywrrld036xgqo72mn012&sep=aa'
    # response = requests.get(url=ipurl, headers=request_header())
    # rs=response.text
    # lsip1 = rs.split("aa")
    
    browser = webdriver.Chrome(options=option)
    
    # # 修改get方法
    # script = '''object.defineProperty(navigator,'webdriver',{undefinedget: () => undefined})'''
    # #execute_cdp_cmd用来执行chrome开发这个工具命令
    # browser.execute_cdp_cmd("page.addscriptToEvaluateonNewDocument",{"source": script})
    
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator,"webdriver",{get: () => undefined})'
    })
    browser.get ('https://www.google.com/')
    time.sleep(5)
    
    for k in keys:
        try:
            
            k1 = k.replace("Keyword:","")
            url_encoded = urllib.parse.quote(k1)
            url =  'https://twitter.com/search?q={}&src=typeahead_click&f=top'.format(url_encoded)
            
            browser.get (url)
            
            wait = WebDriverWait (browser, 10)
            
            
            i=0
            while i<5:
                i=i+1
                time.sleep(3)
                browser.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
                
                soup = BeautifulSoup(browser.page_source,'lxml')
                # print(soup.title)
        
                # lj = soup.find_all(attrs={'class':'css-1dbjc4n'})
                a = soup.find_all('time')
        
                # js = soup.find(attrs={'jsname':'gKDw6b'})
                # uurl = js.find_all(attrs={'class':'VDXfz'})
                for uu in a:
                    try:
                        # surl = 'https://news.google.com/'+uu['href'][2:]
                        # print(uu["href"])
                        stime = uu["datetime"]
                        print(stime)
                        h = uu.parent
                        # name = fu["href"].split("/")[1]
                        # print(name)
                        ht = "https://twitter.com"+h["href"]
                        print(ht)
                        
                        name = uu.parent.parent.parent.parent.parent.parent
                        name = name.text.split("·")[0]
                        print(name)
                        
                        say = uu.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent
                        # print(say.text)
                        
                        div = say.find_all('div')
                        divs = []
                        for d in div:
                            # print(d.text)
                            divs.append(d.text)
                        DD = max(divs, key=len)
                        print(DD)
                        
                        at = say.find_all(attrs={'class':'css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0'})
                        view = at[-1].text
                        like = at[-2].text
                        send = at[-3].text
                        # if at[-4].text =='':
                        if at[-4].text.isdigit():
                            talk = at[-4].text
                        else:
                            talk = at[-3].text
                            send = "0"
                        print(talk,send,like,view)
                        # k = 'NATO Membership'
                        
                        li = [name,DD,talk,send,like,view,ht,stime,k]
                        if li not in TUI:
                            TUI.append(li)
                        
                        # save(name,DD,talk,send,like,view,ht,stime,k)
                        # save(name,content,talk,send,like,view,url,time,key_word)
        
                    except Exception as e:
                        print(e)
                    print('---------------------------------------------------')
        except Exception as e:
            print(e)
            


#%%%%%%%%%%%%%%%%%%


TF = {}
import shortuuid

# def fetch_url(urls):
#     # global TF
#     for t in urls:
#         try:
#             print(t)
#             # lang = langchain(t)
#             # la = shortuuid.ShortUUID().random(length=9)
#             # la = lark(t)
#             # print(la)
#             # print(la)
#             # TF[t]=la
#         except Exception as e:
#             print(e)
        

threads = []

# create 10 threads
for urls in s_urls:
    t = threading.Thread(target=ping, args=(urls,))
    threads.append(t)
    t.start()

# wait for all threads to complete
for t in threads:
    t.join()

#%%%%%%%%%%%%%%%%%%%
for t in TUI:
    print(t)


#%%%%%%%%%%%%%%%%%%

# li = [name,DD,talk,send,like,view,ht,stime,k]

for t in TUI:
    # save(name,DD,talk,send,like,view,ht,stime,k)
    # SAY_save(name,DD,view,stime,url,key_word)
    SAY_save(t[0],t[1],t[2],t[3],t[4],t[5])
    

# save(name,DD,talk,send,like,view,ht,stime,k)

#%%%%%%%%%%%


soup = BeautifulSoup(browser.page_source,'lxml')
# print(soup.title)

# lj = soup.find_all(attrs={'class':'css-1dbjc4n'})
a = soup.find_all('time')

# js = soup.find(attrs={'jsname':'gKDw6b'})
# uurl = js.find_all(attrs={'class':'VDXfz'})
for uu in a:
    try:
        # surl = 'https://news.google.com/'+uu['href'][2:]
        # print(uu["href"])
        stime = uu["datetime"]
        print(stime)
        h = uu.parent
        # name = fu["href"].split("/")[1]
        # print(name)
        ht = "https://twitter.com"+h["href"]
        print(ht)
        
        name = uu.parent.parent.parent.parent.parent.parent
        name = name.text.split("·")[0]
        print(name)
        
        say = uu.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent
        # print(say.text)
        
        div = say.find_all('div')
        divs = []
        for d in div:
            # print(d.text)
            divs.append(d.text)
        DD = max(divs, key=len)
        print(DD)
        
        at = say.find_all(attrs={'class':'css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0'})
        view = at[-1].text
        like = at[-2].text
        send = at[-3].text
        # if at[-4].text =='':
        if at[-4].text.isdigit():
            talk = at[-4].text
        else:
            talk = at[-3].text
            send = "0"
        print(talk,send,like,view)
        k = 'NATO Membership'
        # save(name,DD,talk,send,like,view,ht,stime,k)
        save(name,DD,talk,send,like,view,ht,stime,k)
        # save(name,content,talk,send,like,view,url,time,key_word)

    except Exception as e:
        print(e)
    print('---------------------------------------------------')


# <span class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0">3</span>
# <span class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0">24.8万</span>
# longest = max(my_list, key=len)



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%

import requests
url = 'https://twitter.com/airpinks/status/1638250873104003083'

urls = []

header = {
        # "Host": "twitter.com",
        # "Connection": "keep-alive",
        # "Cache-Control": "max-age=0",
        # "sec-ch-ua":'''"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"''',
        # "sec-ch-ua-mobile": "?0",
        # "sec-ch-ua-platform": "Windows",
        # "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        # "Sec-Fetch-Site": "same-origin",
        # "Sec-Fetch-Mode": "navigate",
        # "Sec-Fetch-User": "?1",
        # "Sec-Fetch-Dest": "document",
        # "Accept-Encoding": "gzip, deflate, br",
        # "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie":'''mbox=session#7c93250e97b448d2a8e1257d1a41969a#1679312058|PC#7c93250e97b448d2a8e1257d1a41969a.35_0#1742554998; _ga_BYKEBDM7DS=GS1.1.1679310202.1.0.1679310223.0.0.0; _ga=GA1.2.2013787596.1679026002; _gid=GA1.2.1986921952.1679913267; guest_id_ads=v1%3A168014498773887609; guest_id_marketing=v1%3A168014498773887609; gt=1641273153212272642; guest_id=v1%3A168014498773887609; personalization_id="v1_1SqQxVAa+FgNBaU/X3VJXw=="; ct0=8a79c5b9f1b71c2d2991cfb59a09648d '''
 
        
        }

wbdata = requests.get(url,headers=header)
if wbdata.status_code == 200:
    # data = response.json()
    # 对获取到的文本进行解析
    soup = BeautifulSoup(wbdata.text,'lxml')
    print(soup.title)
    # 获取文章 内容
    # tx = soup.title.text
    # print(tx)
    print(soup)
    
    # lj = soup.find_all(attrs={'class':'css-1dbjc4n'})
    
    # # js = soup.find(attrs={'jsname':'gKDw6b'})
    # # uurl = js.find_all(attrs={'class':'VDXfz'})
    # for uu in lj:
    #     try:
    #         # surl = 'https://news.google.com/'+uu['href'][2:]
    #         print(uu.time.text)
    #         # uu['href']
    #         # so = surl + '&so=1'
    #         # urls.append(so)

    #     except Exception as e:
    #         print(e)
    #     print('-----------------')
else:
    print(wbdata.status_code)

#%%%%%%%%%
# <div class="css-1dbjc4n"><div dir="auto" lang="en" class="css-901oao r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0" id="id__th0auzliv8p" data-testid="tweetText"><span class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0">Just saw her post where she apologised</span></div></div>
# soup = BeautifulSoup(browser.page_source,'lxml')
# print(soup.title)

# lj = soup.find_all(attrs={'class':'css-1dbjc4n'})
# a = soup.find_all(attrs={'class':'css-1dbjc4n'})
a = soup.find_all('span')
# js = soup.find(attrs={'jsname':'gKDw6b'})
# uurl = js.find_all(attrs={'class':'VDXfz'})
for uu in a:
    try:
        pl = uu.text
        print(pl)
        # surl = 'https://news.google.com/'+uu['href'][2:]
        # print(uu["href"])
        # stime = uu["datetime"]
        # print(stime)
        # fu = uu.parent
        # name = fu["href"].split("/")[1]
        # print(name)
        # xk = "https://twitter.com"+fu["href"]
        # print(xk)
        # uu['href']
        # so = surl + '&so=1'
        # urls.append(so)
        # save(name,xk,stime,k)

    except Exception as e:
        print(e)
    print('-----------------')
#%%%%%%%%%%%%%%

url = 'https://twitter.com/airpinks/status/1638250873104003083'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# 获取推文内容
# tweet = soup.find('div', {'class': 'css-1dbjc4n r-18u37iz r-1h0z5md r-1j3t67a'})
a = soup.find_all("a")
# 获取推文时间
# time = soup.find('time', {'class': 'css-1dbjc4n r-18u37iz r-1j3t67a r-1w6e6rj'})

print('推文内容：', a.text)
# print('推文时间：', time.text)

#%%%%%%%%%%%%%%%%


import requests
import json
import urllib.parse
import csv
import pandas as pd
from itertools import  chain
import numpy as np
from datetime import datetime, timedelta
import time
import calendar
#getuserID可通过user screenname获取ID，不用人工去获取


headers = {
    "cookie": '''mbox=session#7c93250e97b448d2a8e1257d1a41969a#1679312058|PC#7c93250e97b448d2a8e1257d1a41969a.35_0#1742554998; _ga_BYKEBDM7DS=GS1.1.1679310202.1.0.1679310223.0.0.0; _ga=GA1.2.2013787596.1679026002; _gid=GA1.2.1986921952.1679913267; guest_id_ads=v1%3A168014498773887609; guest_id_marketing=v1%3A168014498773887609; gt=1641273153212272642; guest_id=v1%3A168014498773887609; personalization_id="v1_1SqQxVAa+FgNBaU/X3VJXw=="; ct0=8a79c5b9f1b71c2d2991cfb59a09648d ''',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "x-csrf-token": "fdb15b80c46f69b0de4bca152aa8791d",
    "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
}

def main():
        #包装header，伪装成浏览器。
        #*******************为需要替换部分
        
        #也可直接获取id 爬取
        # username = pd.read_csv('*******************.csv')
        # for i in range(0, len(username['username'])):
        #     print(str(username['username'][i]))
        #     csv_username=str(username['username'][i])
        #     userID=getuserID(csv_username,headers)
            
        userID = '2942074931'
        twitterURL = "https://twitter.com/i/api/2/timeline/profile/" + userID + ".json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&include_tweet_replies=false&count=20&userId=" + userID + "&ext=mediaStats%2ChighlightedLabel"
        flag=True
        content = []
        full_content=[]
        response = connect(headers, twitterURL)
        #flag 相当于确定获取到的内容是否在当日里。flag = false 停止爬取
        while (flag):
            # 建立连接
            response = connect(headers, twitterURL)
            # formatRes修改源码的类型
            responseJson = formatRes(response.content)
            # 爬取每个json中 所有推文以及时间，转推，点赞等
            content = parsetweets(responseJson)
            # 将每个json中的内容添加到一个列表中
            full_content.extend(content)
            #获取下一页推文的json包
            twitterURL = getNewURL(responseJson,userID)
            flag=CtrlFlag(content)
            # n = n - 1
        print("------------------------------------------------------------------------------------------------\n------------------------------------------------------------------------------------------------")
        # 提取只要当天的推文
        everydaytweet=todaytweet(full_content)
        # 将内容保存到CSV中，每个用户一个CSV
        # saveData(everydaytweet, csv_username)
        time.sleep(30)

#     获取当天的推文：本来想法：直接在CSV中进行排序，然后截取当天推文。时间排序没成功：：：：：直接在列表中截取当天的推文，再保存在CSV文件中可以。
def CtrlFlag(content):
    flag=True
    time = (todaytime() + timedelta(hours=-8)).strftime("%Y-%m-%d")
    count=0
    for i in range(0,len(content)):
        if content[i][0][0:10] not in str(time):
            count=count+1
        if count==len(content):
            flag=False
    return flag
def getuserID(username,headers):
    connectURL = "https://twitter.com/i/api/graphql/jMaTS-_Ea8vh9rpKggJbCQ/UserByScreenName?variables=%7B%22screen_name%22%3A%22" + username + "%22%2C%22withHighlightedLabel%22%3Atrue%7D"
    print(connectURL)
    response=connect(headers,connectURL)
    
    # soup = BeautifulSoup(response.text,'lxml')
    # print(soup)
    responseJson= formatRes(response.content)
    print(responseJson)
    data=responseJson['data']['user']
    print(data)
    userID=find('rest_id',data)
    return 0

def todaytweet(full_content):
    content=[]
    #todaytime是香港时间，-8获得UTC时间，与爬取的created_at时间统一
    time=(todaytime()+ timedelta(hours=-8)).strftime("%Y-%m-%d")
    for i in range(0,len(full_content)):

        if full_content[i][0][0:10] in str(time):
            content.append(full_content[i])
    return content

# 爬取推文，和时间等，对时间进行格式化****/**/**
def parsetweets(dict):
    dict = dict['globalObjects']['tweets']
    full_text=findAll('full_text',dict)
    created_at=findAll('created_at',dict)
    favorite_count=findAll('favorite_count',dict)
    quote_count=findAll('quote_count',dict)
    reply_count=findAll('reply_count',dict)
    retweet_count=findAll('retweet_count',dict)
    formatcreated_at=[]
    time1=[]
    time2=[]
    utc_time1=[]
    for i in range(0,len(created_at)):
        #从twitter爬下来的时候，就是UTC时间，统一为UTC时间，将本地时间（香港）-8小时。美国时间+5小时
        time1.append(datetime.strptime(created_at[i],"%a %b %d %H:%M:%S +0000 %Y"))
        time2.append(datetime.strftime(time1[i],'%Y-%m-%d %H:%M:%S'))   #datatime转str
    tweetData = []
    #tweetData = list(chain.from_iterable(zip( created_at,full_text)))  # 合并两个列表
    # print(tweetData)
    for i in range(0,len(full_text)):
        tweetData.append([time2[i],full_text[i],favorite_count[i],quote_count[i],reply_count[i],retweet_count[i]])
    return tweetData

# 当前日期 20201029格式，此时时间type：datetime,调用可能需要转换成str
def todaytime():
    today=datetime.today()
    return today

#保存到CSV中,每个人保存在一个CSV文件中、
def saveData(content,filename):
    filetime = todaytime().strftime('%y%y%m%d')
    filename=filetime+" "+filename
    filepath = 'D:/twitterdata/'+filename+'.csv'
    name=['Time', 'Tweet','Favorite','Quote','Reply','Retweet']
    Data=pd.DataFrame(columns=name,data=content)
    Data.to_csv(filepath,encoding='utf-8-sig')

# 直接查找键值 find
def find(target, dictData, notFound='没找到'):
    queue = [dictData]
    while len(queue) > 0:
        data = queue.pop()
        for key, value in data.items():
            if key == target: return value
            elif type(value) == dict: queue.append(value)
    return notFound
def findAll(target, dictData, notFound=[]):
    #print(dictData)
    result = []
    for key, values in dictData.items():
        content = values[target]
        result.append(content)
    #print(result)
    return result

# 获取到cursor，并组成新的url
def getNewURL(responseJson,userID):
    responseJsonCursor1 = responseJson['timeline']['instructions'][0]['addEntries']['entries'][-1]#这是字典，是列表中的最后一个元素
    cursorASCII=find('cursor',responseJsonCursor1)
    cursorASCII2 = find('value', cursorASCII)
    cursor=urllib.parse.quote(cursorASCII2)
    newURL="https://twitter.com/i/api/2/timeline/profile/"+userID+".json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&include_tweet_replies=false&count=20&cursor="+cursor+"&userId="+userID+"&ext=mediaStats%2ChighlightedLabel"
    return newURL

#格式化获取到的json//bytes转string loads()将string读入字典中
def formatRes(res):
       strRes = str(res, 'utf-8')
       dictRes = json.loads(strRes)
       return dictRes

#设置代理proxies，链接获取网页数据。代理部分需要自己设置
def connect(headers,twitterURL):
       # proxies = {"http": "http://127.0.0.1:4780", "https": "http://127.0.0.1:4780", }
       response = requests.get(twitterURL,headers = headers)
       return response


# getuserID('SubeiZ',headers)


if __name__=="__main__":   #当程序执行时
    main()
    
    
#%%%%%%%%%%%%%%%%%%%%%%%%%%%


import time
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re
import sys

##对页面文字进行解析，只选取评论部分--工具函数
def get_comment_from_page(comment):
    contents=[]
    text_list=comment.split('\n·')[1:]
    for i in text_list:
        for j in i.split('\n'):
            if  (re.search('@|回复|年', j) or len(j)<2 or not re.search(' ', j)):
                pass
            else:
                contents.append(j)
    return contents            
#获取主页所有的推文
def get_alltweets_url(driver):
    urls=driver.find_elements(By.XPATH, value="//a")
    url_list=[]
    for i in urls:
        url=i.get_attribute("href")
        if('https://twitter.com/SpiritPledgeDAL/status/' in url and len(url)==62):
            url_list.append(url)
    return url_list

#获取推文链接函数
def page_down_main(url):
    chrome_options=Options()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url=url)
    check_height = driver.execute_script("return document.body.scrollHeight;")
    wait = WebDriverWait(driver,10) 
    url_list=[]
    while True:
        url=get_alltweets_url(driver)
        url_list=url_list+url
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            WebDriverWait(driver, 5).until(lambda driver: driver.execute_script("return document.body.scrollHeight;") > check_height)
            check_height = driver.execute_script("return document.body.scrollHeight;")
        except TimeoutException:
            break
    driver.close()
    return  url_list
#获取推文评论
def page_down_comment(url):
    chrome_options=Options()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url=url)
    check_height = driver.execute_script("return document.body.scrollHeight;")
    wait = WebDriverWait(driver, 5) 
    comment_list=[]
    while True:
        comment_origin=driver.find_element_by_css_selector('div.css-1dbjc4n').text
        comment=get_comment_from_page(comment_origin)
        comment_list=comment_list+comment
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            WebDriverWait(driver, 5).until(lambda driver: driver.execute_script("return document.body.scrollHeight;") > check_height)
            check_height = driver.execute_script("return document.body.scrollHeight;")
        except TimeoutException:
            break
    driver.close()
    return  comment_list    

#进行爬虫
def twitter_acrapy(url):
    url_list=page_down_main(url)
    comments=[]
    for i in range(len(url_list)):
        comment=page_down_comment(url_list[i])
        comments=comments+comment
        sys.stdout.write("\r 正在爬取页数:{0}".format(i))
        sys.stdout.flush()
    return comments
        
url='https://twitter.com/SpiritPledgeDAL'
comments=twitter_acrapy(url)