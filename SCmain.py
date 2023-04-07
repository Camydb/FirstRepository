# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 12:17:16 2023

@author: Administrator
"""
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

from selenium.webdriver import ChromeOptions




# =============================================================================
# # 实例化谷歌
# driver = webdriver.Chrome(options=option)
# # 修改get方法
# script = '''object.defineProperty(navigator,'webdriver',{undefinedget: () => undefined})'''
# #execute_cdp_cmd用来执行chrome开发这个工具命令
# driver.execute_cdp_cmd("page.addscriptToEvaluateonNewDocument",{"source": script})
# =============================================================================


#%%%%%%%%%%%%%%%%%%%%%


import requests

url = 'http://120.48.49.157:5000/change_user_info?userID=Lw7CH4upxDy7tzDS9XChsg&user_name=大明' # 替换为您要发送图片的 URL

# with open('D:/image/aa.jpg', 'rb') as file:
#     response = requests.post(url, files={'file': file,"question":"QQQQQQQQQQQQQQQQQQ"})

data = {
    # 'question': 'This is an image',
    'file': ('image.jpg', open('D:/image/aa.jpg', 'rb'), 'image/jpeg')
}

response = requests.post(url, files=data)

print(response.text) # 输出服务器返回的响应内容

#%%%%%%%%%%%%%%%%%%%%




def request_header():
    headers = {
        'User-Agent': UserAgent().random #常见浏览器的请求头伪装（如：火狐,谷歌）
        #'User-Agent': UserAgent().Chrome #谷歌浏览器
        }
    return headers


# ipurl = 'https://dev.kdlapi.com/api/getproxy/?secret_id=o6hbdmtkawas7lpggdwk&num=200&protocol=2&method=1&an_ha=1&quality=1&signature=9c6psfeph2jtaxgdm2kv2obz1knvinz7&sep=aa'
# response = requests.get(url=ipurl, headers=request_header())
# rs=response.text
# lsip1 = rs.split("aa")

def baocun(db,BIAOT,ZUOZ,PINGL,NEIR,TIME,FENL,ZURL,BEIZ):
    

    
    conn = sqlite3.connect(db)

    # print(db)
    # stime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.execute(
        '''INSERT INTO TX_0301 (BIAOT,ZUOZ,PINGL,NEIR,TIME,FENL,ZURL,BEIZ) VALUES ("{}","{}","{}","{}","{}","{}","{}","{}")'''.format(BIAOT,ZUOZ,PINGL,NEIR,TIME,FENL,ZURL,BEIZ));
    conn.commit()
    print ("记录插入成功!")
    conn.close()

def qing(url,tt,ZZurl,PL,lei,db):
    # 请求腾讯新闻的URL，获取其text文本
    
    
    
    # proxies = {"http": "https://" + random.choice(lsip1) }
    # print(proxies)
    
    # wbdata = requests.get(url,headers=request_header(),proxies=proxies)
    wbdata = requests.get(url,headers=request_header())
    # wbdata = requests.get(url,headers=request_header())
    
    if wbdata.status_code == 200:
        # data = response.json()
    
        # 对获取到的文本进行解析
        soup = BeautifulSoup(wbdata.text,'lxml')
    
        # print(soup)
    
    
        print(soup.title.text)
    
        # 获取文章 内容
        artical=soup.find_all(attrs={'class':'one-p'})
        
        # ss = soup.find(attrs={'name':'apub:time'})
        # stime = ss.attrs['content']
        u = url.split('/')[-1]
        # print(u[:8])
        stime =u[:8]
        # print(day)
    
        content=""    
        for para in artical:
    
            content+=para.text
        
        if len(content)==0:
            content='video'
        
        baocun(db,soup.title.text,tt,PL,content,stime,lei,ZZurl,url)
    
    else:
        time.sleep(1)
        print('错误状态')
        pass
        # "go back to response"

def pa(lei,url,db):
    from selenium.webdriver import ChromeOptions
    # chrome_option = webdriver.ChromeOptions()
    # chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 以开发者模式
    
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
    browser.get ('https://www.qq.com/')
    time.sleep(5)
    browser.get (url)
    
    wait = WebDriverWait (browser, 10)
    lis=[]
    
    while True:
        try:
            bb = browser.find_elements(By.XPATH, value='//*[contains(@id,"2023")]/div/h3/a')
            #b2 = b1.find_elements(By.XPATH, value='//div/h3/a')
            #b2 = b1.find_element(By.CLASS_NAME,'picture')
            for b1 in bb:
                html = b1.get_attribute('href')
                # b2 = b1.find_element(By.XPATH, value='../../div/div/a')
                # ZZ = b2.text
                # ZZurl = b2.get_attribute('href')
                # try:
                #     #pl = b1.find_element(By.XPATH, value='../../div/div/a').text
                #     tiao = b1.find_element(By.XPATH, value='../../../div')
                #     PL = tiao.find_element(By.CLASS_NAME, value='cmt').text
                #     # print(PL)
                # except Exception as e:
                #     #print(e)
                #     PL='0'
                    
                
                # print(html)
                # print(ZZ)
                # print(ZZurl)
                # print(PL)
                
                if 'html' in html:
                    # ZZ=l.find(attrs={'class':'source'}).text
                    
                    # try:
                    #     PL=l.find(attrs={'class':'cmt'}).text
                    # except:
                    #     PL='0'
                    # print(detail_url)
                    #print(tags)
                    # print(tt)
                    if html in lis:
                        pass
                        # print('已存在')
                        # print(len(lis))
                    else:
                        print(html)
                        lis.append(html)
                        # print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
                        
                        
                        b2 = b1.find_element(By.XPATH, value='../../div/div/a')
                        ZZ = b2.text
                        ZZurl = b2.get_attribute('href')
                        try:
                            #pl = b1.find_element(By.XPATH, value='../../div/div/a').text
                            tiao = b1.find_element(By.XPATH, value='../../../div')
                            PL = tiao.find_element(By.CLASS_NAME, value='cmt').text
                            # print(PL)
                        except Exception as e:
                            #print(e)
                            PL='0'
                        
                        qing(html,ZZ,ZZurl,PL,lei,db)
                        time.sleep(0.1)
                        # print('已存在')
                        #pass

        except Exception as e:
            print(e)
            pass
        try:
            browser.find_element(By.CLASS_NAME, value='more').click()
        except Exception as e:
            print(e)
        # browser.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
        time.sleep(1)
        browser.find_element(By.TAG_NAME,'body').send_keys(Keys.SPACE)
        time.sleep(1)
        print(len(lis))
        # browser.find_element(By.CLASS_NAME, value='more').click()
        # browser.find_element(By.CLASS_NAME, value='more').send_keys(Keys.SPACE)

# =============================================================================
#     soup = BeautifulSoup (browser.page_source, 'lxml')
#     uls = soup.find_all('li')
#     #uls =browser .find_all('li')
#     for l in uls:
#         try:
#             detail_url = l.a.attrs['href']#详情页链接
#             # tt=l.find(attrs={'class':'source'}).text
#             #tags = l.text
#             if 'html' in detail_url:
#                 # ZZ=l.find(attrs={'class':'source'}).text
#                 
#                 # try:
#                 #     PL=l.find(attrs={'class':'cmt'}).text
#                 # except:
#                 #     PL='0'
#                 # print(detail_url)
#                 #print(tags)
#                 # print(tt)
#                 if detail_url not in lis:
#                     lis.append(detail_url)
#                     
#                     
#                     ZZ=l.find(attrs={'class':'source'}).text
#                     
#                     try:
#                         PL=l.find(attrs={'class':'cmt'}).text
#                     except:
#                         PL='0'
#                     print(detail_url)
#                     print(tt)
#                     # qing(detail_url,ZZ,PL,lei,db)
#                     time.sleep(0.1)
#         
#         except Exception as e:
#                 print(e)
# =============================================================================

threads = []     #定义一个线程池

t1=threading.Thread(target=pa,args=('科技','https://new.qq.com/ch/tech/',"D:/TenCen/TECH.db",))
threads.append(t1)    #把t1线程装到线程池里

t2=threading.Thread(target=pa,args=('房产','https://new.qq.com/ch/house/',"D:/TenCen/HOUSE.db",))
threads.append(t2)    #把t1线程装到线程池里

t3=threading.Thread(target=pa,args=('数码','https://new.qq.com/ch/digi/',"D:/TenCen/DIJI.db",))
threads.append(t3)    #把t1线程装到线程池里

t4=threading.Thread(target=pa,args=('国际','https://new.qq.com/ch/world/',"D:/TenCen/WORLD.db",))
threads.append(t4)    #把t1线程装到线程池里

# t5=threading.Thread(target=pa,args=('要问','https://news.qq.com/',"D:/TenCen/NEWS.db",))
# threads.append(t5)    #把t1线程装到线程池里

# t1=threading.Thread(target=pa,args=('财经','https://new.qq.com/barrierfree.html?channel=finance',"D:/TenCen/FINANCE.db",))
# threads.append(t1)    #把t1线程装到线程池里

# t2=threading.Thread(target=pa,args=('军事','https://new.qq.com/barrierfree.html?channel=milite',"D:/TenCen/MILITE.db",))
# threads.append(t2)    #把t1线程装到线程池里

# t3=threading.Thread(target=pa,args=('汽车','https://new.qq.com/barrierfree.html?channel=auto',"D:/TenCen/AUTO.db",))
# threads.append(t3)    #把t1线程装到线程池里

# t4=threading.Thread(target=pa,args=('科技','https://new.qq.com/barrierfree.html?channel=tech',"D:/TenCen/TECH.db",))
# threads.append(t4)    #把t1线程装到线程池里

# t5=threading.Thread(target=pa,args=('娱乐','https://new.qq.com/barrierfree.html?channel=ent',"D:/TenCen/ENT.db",))
# threads.append(t5)    #把t1线程装到线程池里

# t6=threading.Thread(target=pa,args=('体育','https://new.qq.com/barrierfree.html?channel=sports',"D:/TenCen/SPORTS.db",))
# threads.append(t6)    #把t1线程装到线程池里

# t7=threading.Thread(target=pa,args=('文化','https://new.qq.com/barrierfree.html?channel=cul',"D:/TenCen/CUL.db",))
# threads.append(t7)    #把t1线程装到线程池里

# t8=threading.Thread(target=pa,args=('国际','https://new.qq.com/barrierfree.html?channel=world',"D:/TenCen/WORLD.db",))
# threads.append(t8)    #把t1线程装到线程池里

for t in threads:
    t.start()
# delete from TX_0227 where LENGTH(NEIR)<1;

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import sqlite3

conn = sqlite3.connect('D:/TenCen/DIJI.db')
print ("数据库打开成功")
c = conn.cursor()

# SQL 查询语句，查询user表
sql = "select BEIZ from TX_0227" 

c.execute(sql)

#这是查询表中所有的数据
rest=c.fetchall()


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
conn.commit()
conn.close()


# conn = sqlite3.connect('D:/TenCen/HOUSE.db')
# print ("数据库打开成功")
# c = conn.cursor()
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
# conn.commit()
# conn.close()



# conn = sqlite3.connect('D:/TenCen/DIJI.db')
# print ("数据库打开成功")
# c = conn.cursor()
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
# conn.commit()
# conn.close()



# conn = sqlite3.connect('D:/TenCen/WORLD.db')
# print ("数据库打开成功")
# c = conn.cursor()
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
# conn.commit()
# conn.close()
#%%%%%%%%%%%%%%%%%%%%%%%%%%%

# TE = [1,3,6]

# for i in range(0,10):
#     if i not in TE:
#         print(i)

#%%%%%%%%%%%%%%%%%%%%%%
url = 'https://new.qq.com/ch/tech/'
browser = webdriver.Chrome ()
browser.get (url)
wait = WebDriverWait (browser, 10)

# while True:
soup = BeautifulSoup (browser.page_source, 'lxml')
lis=[]
uls = soup.find_all('li')
#uls =browser .find_all('li')
for l in uls:
    try:
        detail_url = l.a.attrs['href']#详情页链接
        # tt=l.find(attrs={'class':'source'}).text
        # pl=l.find(attrs={'class':'cmt'}).text
        # pl = l.a.text
        #tags = l.text
        if 'html' in detail_url:
            tt=l.find(attrs={'class':'source'}).text
            pl=l.find(attrs={'class':'cmt'}).text
            # print(detail_url)
            #print(tags)
            # print(tt)
            if detail_url not in lis:
                print(detail_url)
                print(tt)
                print(pl)
                lis.append(detail_url)
                # qing(detail_url,tt,lei,db)
                time.sleep(0.1)
    
    except Exception as e:
            print(e)
            
            
browser.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
    
    
#%%%%%%%%%%%%%%%
import requests
from fake_useragent import UserAgent
def request_header():
    headers = {
        'User-Agent': UserAgent().random #常见浏览器的请求头伪装（如：火狐,谷歌）
        #'User-Agent': UserAgent().Chrome #谷歌浏览器
        }
    return headers
ipurl = 'https://dev.kdlapi.com/api/getproxy/?secret_id=oddm05z4s2t2j338op8m&num=1000&protocol=2&method=1&an_ha=1&quality=1&signature=vce2g38s38udywrrld036xgqo72mn012&sep=aa'
response = requests.get(url=ipurl, headers=request_header())
rs=response.text
lsip1 = rs.split("aa")
print(lsip1)
print(len(lsip1))


#%%%%%%%%%%%%%%%%%%

url = 'https://new.qq.com/rain/a/20230226A004GR00'
wbdata = requests.get(url,headers=request_header())


# if wbdata.status_code == 200:
# data = response.json()

# 对获取到的文本进行解析
soup = BeautifulSoup(wbdata.text,'lxml')

# print(soup)
u = url.split('/')[-1]
print(u[:8])

print(soup.title.text)

# 获取文章 内容
artical=soup.find_all(attrs={'class':'one-p'})

# ss = soup.find(attrs={'name':'apub:time'})
ss = soup.find_all(attrs={'class':'md'})
for s in ss:
    print(s.text)
# stime = ss.attrs['content']
# print(day)

content=""    
for para in artical:

    content+=para.text
    
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import requests
url = 'https://new.qq.com/omn/20230307/20230307A06H5500.html'
# wbdata = requests.get(url,headers=request_header(),proxies=proxies)
wbdata = requests.get(url,headers=request_header())
# wbdata = requests.get(url,headers=request_header())

if wbdata.status_code == 200:
    # data = response.json()

    # 对获取到的文本进行解析
    soup = BeautifulSoup(wbdata.text,'lxml')

    # print(soup)


    print(soup.title.text)

    # 获取文章 内容
    artical=soup.find_all(attrs={'class':'one-p'})
    
    # ss = soup.find(attrs={'name':'apub:time'})
    # stime = ss.attrs['content']
    u = url.split('/')[-1]
    # print(u[:8])
    stime =u[:8]
    # print(day)

    content=""    
    for para in artical:

        content+=para.text
    print(type(content))