# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 19:13:20 2023

@author: amy
"""
token = 't-g2053t2kGMRVXDAP6RQ74DUYJJJN5D24HXJP3P6K'

# =============================================================================
# from langchain import OpenAI
# from langchain.chains.summarize import load_summarize_chain
# from langchain.chains import AnalyzeDocumentChain
# 
# def langchain(text):
#     llm = OpenAI(temperature=0)
#     summary_chain = load_summarize_chain(llm, chain_type="map_reduce")
#     summarize_document_chain = AnalyzeDocumentChain(combine_docs_chain=summary_chain)
#     return(summarize_document_chain.run(text))
# =============================================================================

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
    # elif response.status_code==400:
    #     token = get_token()
    #     print('重新请求')
    #     headers = {'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json; charset=utf-8'}
    #     response = requests.post(url, headers=headers, json=data)
    #     time.sleep(1)
    #     return(response.json()['data']['text'])
    else:
        return ('无法翻译')


import threading
import requests
from datetime import datetime
import sqlite3 as sq3
import pandas as pd
import time

db = sq3.connect("D:/T_py/GOOGLE.db")
# df = pd.read_sql("SELECT GPT3_TEXT FROM GL_NEWS" , db)
# db.close()

# urls = list(df["GPT3_TEXT"])

cur = db.cursor()

texts = []
# for row in cur.execute('SELECT THEME,TH_ZH FROM Gl_NEWS' ):
# for row in cur.execute('SELECT GPT3_TEXT,ZH_CN FROM Gl_NEWS' ):
# for row in cur.execute('SELECT GPT3_TITLE,GT_ZH FROM Gl_NEWS' ):
# for row in cur.execute('SELECT KEY_WORD,KW_ZH FROM Gl_NEWS' ):
for row in cur.execute('SELECT KEY_WORD FROM Gl_NEWS' ):
    # if row[1] is None:
    texts.append(row[0])
    # else:
    #     print("不为空")
db.close()

text_s = list(set(texts))

s_urls = split_list(text_s,5)
print(len(text_s))

# print(get_token())

#%%%%%%%%%%%%%%%%%%

print(text_s)

#%%%%%%%%%%%%%%%%%%%

TF = {}
import shortuuid

def fetch_url(urls):
    global TF
    for t in urls:
        try:
            # lang = langchain(t)
            la = shortuuid.ShortUUID().random(length=9)
            print(la)
            # print(la)
            TF[t]=la
        except Exception as e:
            print(e)
        

threads = []

# create 10 threads
for urls in s_urls:
    t = threading.Thread(target=fetch_url, args=(urls,))
    threads.append(t)
    t.start()

# wait for all threads to complete
for t in threads:
    t.join()
    
#%%%%%%%%%%%%%%%%%%


print(TF)


#%%%%%%%%%%%%%%%%%%%%%%%



db = sq3.connect("D:/T_py/GOOGLE.db")
cur = db.cursor()
for key, value in TF.items():
    print(key, value)
    cur.execute('''UPDATE GL_NEWS SET TH_ID = ? WHERE THEME = ?''', (value,key))
    # cur.execute('''UPDATE GL_NEWS SET KW_ZH = ? WHERE KEY_WORD = ?''', (value,key))
    # cur.execute('''UPDATE GL_NEWS SET GT_ZH = ? WHERE GPT3_TITLE = ?''', (value,key))
    # cur.execute('''UPDATE GL_NEWS SET TH_ZH = ? WHERE THEME = ?''', (value,key))
    # cur.execute('''UPDATE GL_NEWS SET TH_ZH = ? WHERE THEME = ?''', (value,key))
    # cur.execute('''UPDATE GL_NEWS SET ZH_CN = ? WHERE GPT3_TEXT = ?''', (value,key))
    # cur.execute('''UPDATE GL_NEWS SET T_ZH = ? WHERE TITLE = ?''', (value,key))
    db.commit()

db.close()


#%%%%%%%%%%%%%%%%%%%%

import random
import string

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

print(get_username())


#%%%%%%%%%%%%%%%%%
import requests
from bs4 import BeautifulSoup
import threading

# 爬虫线程类
class SpiderThread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
    
    def run(self):
        try:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # 在这里处理爬取到的数据
            print(soup.title.text)
        except Exception as e:
            print('Error:', e)

# 爬虫入口函数
def spider(urls):
    threads = []
    for url in urls:
        thread = SpiderThread(url)
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    urls = ['http://www.baidu.com', 'http://www.sina.com', 'http://www.qq.com']
    spider(urls)




#%%%%%%%%%%%%%%%%%%

import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

uuu = ['https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2phOU12eEJoRTdpYVphaERiNUpDZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lFNThMMkJoRlg4TVJ6Nmh4a1pDZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lLNF9MM0JoR1JRajFUZUVwaC1pZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2llejdIekJoRnpXMnB4Q3N4OHhDZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pkM0x6eUJoRTctcXlYQ3ptVHNpZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lBbUlfdUJoSHNDQXhGN3lSdnRpZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lqMV9icEJoRXY5VENWZExRVlJ5Z0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pGNDZ6M0JoR0Y1S2tIQVhZSDVpZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lGazhuc0JoRThPUE10Sk1ZMkZ5Z0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pFeUpqeEJoR1lKQ09lM3dzbE1TZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pKdGVudkJoRTlaMFJRMm9uM055Z0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lDMTRENUJoR3Y0al9peVRVVUt5Z0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lYOE9md0JoSExXWWltZjFwQkRTZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lTeUo3ckJoSDE2ZzRmbHdIWVZpZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lqeS1fMkJoRVpDM3Y4VkVyS2JpZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2l0XzZmeUJoRzhtYkdfYkVqZ2hpZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2loenVqMUJoSEh4ZEJzd0tocktpZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2ltbWN6dEJoRUNXaHI5c3JUREJpZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2o5bDZ2eEJoSDJTRV9kVkZsUHN5Z0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2k0d09YcEJoRmJveTNwWFlGZUhTZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pxa19mM0JoRUlMb3dKcFhHdGtpZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lnaXByNEJoSG80ZEVnRGJoSDNTZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2p5eVp6bUJoSFdJbjNZTVFCd0hpZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2k4NjlqMkJoSGhaaENoUWZFU2RDZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lSdE9UckJoRmhEQ1RpYzR2Uk1DZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pCdjVMc0JoRk5XcTQ0YU5nSThDZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lmc3BENUJoR25FVllaT2xMZ0ZTZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pMdzZ6eEJoSDBEemUydXluaEVTZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lZc29EM0JoSDh4OWE3dTROb1RpZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2k2X3V6MkJoSEEyZ29vVU9yaU9DZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pJMjhMNUJoRnFqTXViRGdDajdpZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2o3b1ludUJoSElhMDM2XzlLTFNTZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2k4dGNiNEJoRTBFZU1RNDBGWnhTZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pnLUtqc0JoRUQ0RVc4MERtQTlTZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pQX0xfbEJoSEhuRzVUWm13dF9pZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lWODZQNkJoRU1QWWR5WlpDaWtDZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2ljNGNMeEJoR3QzcDNvZ1l1UHVTZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lYa01UbkJoRm5PX01aMDBXVUN5Z0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lLazc3eUJoRWtTbHVNVV9ZWWJDZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2luMXV6aEJoSE1WdDl6XzNfMVV5Z0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pZenVQckJoRnctNGtNTnlmVkVpZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lpbTc3b0JoR2lNdGlEMDFleVl5Z0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lTZzR6ekJoRzkxSjdXZWVfWE1TZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lhcThYdEJoRjl4TExKVkQ1TlZ5Z0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2o4M19UbkJoRzl6aG1sX3dLN1NpZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pBMHMzNEJoRk5Pc2FYdEhxY2NDZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2l3MjhINEJoSFZJaHJzRFNTQV9TZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pjMHRfMUJoSF9SQzM1djl0WnJ5Z0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lrdGJMMkJoR1M1Q2VwZ0xNNUFpZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2loMTdYM0JoRzhraWFSRjZHbS1DZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2laXzRmdUJoRlk0VVhTd04xNjFTZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2k4ek1qcEJoRXRnS2stdWF2c3ZpZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pGNE92eUJoRWZiOGpqaFdFWnVpZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2kyeTh6ekJoR0FnY1NKeHFZOHNTZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2ozbmV6MkJoRUpJLXVhQk1GdEVpZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lEdDVYaUJoSDNvelFXa21XOTZpZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lYenB2NUJoRnYzT3V4Mlh4TWpDZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pOd0x2NEJoSGtHdG9vcUE2OXZTZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lvMjZ6NEJoR1o1ME1JWGRyVjl5Z0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pfbjZfeUJoRjN5ZGQtMTlYXzBTZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lEcGJ6NEJoSEM3UUJsOE9xbmp5Z0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2oxeHBMNEJoR0ZnR2p5TzdBM0RTZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pPLXEzbkJoRWpKMjJZT2dzN3R5Z0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2owa3FYdUJoSGJXa2lzcy1BZmJDZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pHaWJEbkJoRUZ4Vl9zZzBYLWNTZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lzX2ZqMEJoSHN4SVJwU05tQTdpZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lGM0tiMkJoRWl5Nnd5OVlTRm9pZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1', 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2p6NWM3MkJoRmRMdzlkVmhWb29TZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1']

def title_sum(url):
    time.sleep(1)
    print(url)
    return ('stop')


if __name__ == '__main__':
    pool = Pool(3)  # 创建拥有3个进程数量的进程池
    # testFL:要处理的数据列表，run：处理testFL列表中数据的函数
    pool.map(title_sum, uuu)
    pool.close()  # 关闭进程池，不再接受新的进程
    pool.join()  # 主进程阻塞等待子进程的退出

#%%%%%%%%%%%%%%%%%%%%%%

import time
from multiprocessing import Pool


def run(fn):
    # fn: 函数参数是数据列表的一个元素
    time.sleep(1)
    print(fn * fn)


if __name__ == "__main__":
    testFL = [1, 2, 3, 4, 5, 6]
    # print('shunxu:')  # 顺序执行(也就是串行执行，单进程)
    # s = time.time()
    # for fn in testFL:
    #     run(fn)
    # t1 = time.time()
    # print("顺序执行时间：", int(t1 - s))

    print('concurrent:')  # 创建多个进程，并行执行
    pool = Pool(3)  # 创建拥有3个进程数量的进程池
    # testFL:要处理的数据列表，run：处理testFL列表中数据的函数
    pool.map(run, testFL)
    pool.close()  # 关闭进程池，不再接受新的进程
    pool.join()  # 主进程阻塞等待子进程的退出
    # t2 = time.time()
    # print("并行执行时间：", int(t2 - t1))

#%%%%%%%%%%%%%%%%%%

import multiprocessing as mp
poolDict=mp.Manager().dict()

def myFunct(arg):
    print ('myFunct():', arg)
    for i in range(110):
        for n in range(500000):
            pass
        poolDict[arg]=i
    print ('myFunct(): completed', arg, poolDict)

from multiprocessing import Pool
pool = Pool(processes=2)
myArgsList=['arg1','arg2','arg3']

pool.apply_async( myFunct, myArgsList)
pool.close()
pool.join()
print ('completed')

#%%%%%%%%%%%%%%%%%%%


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
 
if __name__ == '__main__':
     list = ['1', '1', '1','1', '1', '1','1', '1', '1','1', '1', '1','1', '1', '1','1', '1', '1','1', '1','1']
     num = 5      # 将要创建的线程数量
     list_total = split_list(list,num)
     for i in list_total:
          print(i)
          
#%%%%%%%%%%%%%%%%%%%%%%%%
import threading
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

def get_all_ip(u):
    print(u)

if __name__ == '__main__':
    list = ['1', '1', '1','1', '1', '1','1', '1', '1','1', '1', '1','1', '1', '1','1', '1', '1','1', '1','1']
    num = 5      # 将要创建的线程数量
    list_total = split_list(list,num)
    for i in list_total:
         print(i)
          

    thread_list =[]     # 创建线程池
    for url in list_total:      # 添加线程
        t = threading.Thread(target=get_all_ip,args=(url,))
        thread_list.append(t)
        # thread1 = MyThread(func=get_all_ip,args=list_total[0])
        # thread2 = MyThread(func=get_all_ip,args=list_total[1])
    for t in thread_list:       # 批量启动线程
        t.start()
    for t in thread_list:       # 主线程等待子线程
        t.join()

#%%%%%%%%%%%%%%%%%%%%%


"""
通过实例化threading.Thread类创建线程
"""
import time
import threading


def test_thread(para='hi', sleep=3):
    """线程运行函数"""
    time.sleep(sleep)
    print(para)


def main():
    # 创建线程
    thread_hi = threading.Thread(target=test_thread)
    thread_hello = threading.Thread(target=test_thread, args=('hello', 1))
    # 启动线程
    thread_hi.start()
    thread_hello.start()
    print('Main thread has ended!')


if __name__ == '__main__':
    main()

#%%%%%%%%%%%%%%%%%%%%%%%

# 这是一个使用Python的multiprocessing模块实现并发爬虫的例子：

# ```python
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

def get_links(url):
    """
    从给定的网页中获取所有的链接
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href is not None and href.startswith('http'):
            links.append(href)
    return links

def scrape(url):
    """
    访问给定的URL并返回其文本内容
    """
    response = requests.get(url)
    return response.text

if __name__ == '__main__':
    urls = get_links('https://www.python.org/')
    with Pool(processes=4) as pool:
        pages = pool.map(scrape, urls)
        for page in pages:
            # 处理每个页面的内容
            pass


# 在这个例子中，我们使用`get_links`函数从给定的URL中获取所有链接。然后，我们使用`scrape`


#%%%%%%%%%%%%%%%%%%%%%%

import multiprocessing
import time

def sleepy_man(sec):
    print('Starting to sleep for {} seconds'.format(sec))
    time.sleep(sec)
    print('Done sleeping for {} seconds'.format(sec))

if __name__ == '__main__':
    tic = time.time()
    pool = multiprocessing.Pool(5)
    pool.map(sleepy_man, range(1,11))
    pool.close()
    
    toc = time.time()
    
    print('Done in {:.4f} seconds'.format(toc-tic))


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%

import pymysql
import pandas as pd
db = pymysql.connect(
    host="120.48.49.157", 
    port=3306,
    user='root',    #在这里输入用户名
    password='root123321',     #在这里输入密码
    charset='utf8mb4' ,
    database='USER'
    ) #连接数据库


u = '3FtPAHrhhveJGNzC5FaBWv'

# n = '3DDmMbvyhcaqtssEwq63F5'

# cursor = db.cursor()
# sql = '''delete from user_like where user_ID="{}" and news_ID="{}" '''.format(u,n)
# cursor.execute(sql)
# db.commit()
# db.close()


# 使用 cursor() 方法创建一个游标对象 cursor
# cursor = db.cursor()
# 使用pandas的read_sql函数读取数据
df = pd.read_sql('''SELECT news_ID,class_n FROM user_like WHERE user_ID= "{}"  '''.format(u), db)
# '''select PEOPLE,PINGL,TIME,ZH_CN from Twitter WHERE CLASS like "%{}%"  '''.format(word)
# 关闭连接
db.close()

# print(df["class_n"]=='news')

# print((df.loc[df['class_n'] == 'news'])['news_ID'])

print(tuple((df.loc[df['class_n'] == 'news'])['news_ID']),tuple((df.loc[df['class_n'] == 'talk'])['news_ID']))


#%%%%%%%%%%%%%%%

like_talk = ('2','1')

if '2' in like_talk:
    print('like')
    
#%%%%%%%%%%%%%%%

ids = [1, 2, 3, 4, 5]
sql = "SELECT * FROM table WHERE ID IN ({})".format(','.join(['%s']*len(ids)))
print(sql)


#%%%%%%%%%%%%%%%%%%%%%
import pymysql
import pandas as pd

HOST="120.48.49.157"

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
    if class_n == 'news' or class_n == 'talk':
        df = pd.read_sql('''SELECT user_ID,class_n FROM user_like WHERE news_ID= "{}"  '''.format(search_id), db)
        db.close()
        df = df.drop_duplicates('user_ID')#.sort_index()
        return(len(df))
    
    elif class_n == 'discuss':
        df = pd.read_sql('''SELECT user_ID,discuss_ID,class_n FROM user_discuss WHERE news_ID= "{}"  '''.format(search_id), db)
        db.close()
        df = df.drop_duplicates('discuss_ID')#.sort_index()
        return(len(df))
    
    else:
        print('False')
        db.close()
        return 0
    
print(get_act('42huTLgsD','discuss'))