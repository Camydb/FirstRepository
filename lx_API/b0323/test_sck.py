# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 16:37:11 2023

@author: amy
"""

from flask import Flask
from flask_sockets import Sockets
import datetime
import time
import requests
import json

app = Flask(__name__)
sockets = Sockets(app)

from flask_cors import *
CORS(app, supports_credentials=True)

@sockets.route('/echo')
def echo_socket(ws):
    print("hello")
    # msg = ws.receive()
    # print(msg)
    # while True:
    while not ws.closed:
        msg = ws.receive()
        print(msg)
        # now = datetime.datetime.now().isoformat()
        # time.sleep(3)
        # if time.localtime().tm_sec == 0:
        re = requests.get(url='https://v1.hitokoto.cn/?encode=text')
        # print(re.text)
        data = {
           "code": "OK",
           "result":{
            "text":re.text
            }
        }
        ws.send(str(data))  #发送数据
        # now = datetime.datetime.now().isoformat()
        # print(now)
        time.sleep(5)
            

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('0.0.0.0', 8080), app, handler_class=WebSocketHandler)
    print('server start')
    server.serve_forever()



#%%%%%%%%%%%%%%%%%%%%

import openai
response = openai.Image.create(
  prompt='''
  A Logo:1. Stereoscopic: The NS logo design adopts a triangular shape, making the entire logo look more three-dimensional and more vivid.
2. Concise: The entire logo uses only two letters N and Z to express the brand name simply and intuitively.
3. Avant-garde feeling: The logo design adopts streamlined lines and modern blue, giving a fashionable and avant-garde feeling.
4. Blue and White Color Matching: The entire logo uses a blue and white color matching. Blue represents professionalism and stability, while white represents simplicity and freshness.
5. Arrow shape: The shape of the entire logo is similar to an arrow, implying that NS is a news app that continues to develop and progress
      ''',
  n=1,
  size="1024x1024"
)
image_url = response['data'][0]['url']
print(image_url)



#%%%%%%%%%%%%%%%%%%%%


ss = '''China appealed to the International Criminal Court (ICC) on Monday to avoid what it termed as \'double standards\' and respect the immunity of heads of state, after an arrest warrant was issued by the tribunal for Russian President Vladimir Putin on charges of committing war crimes.\n\nThe court should \'uphold an objective and impartial stance\' and \'respect the immunity of heads of state from jurisdiction under international law\', said foreign ministry spokesperson Wang Wenbin in a press briefing.\n\nWang also appealed to the court to \'avoid politicisation and double standards\', emphasising the fact the Ukraine conflict can be resolved only through \'dialogue and negotiation\'.\n\nALSO READ | With Ukraine war at critical junction, China takes bigger role\n\nChina is not among the signatories of the Rome Statute which is a United Nations treaty that governs the court.\n\nOn Friday, the International Criminal Court announced that it is issuing an arrest warrant against Putin who is accused of unlawfully deporting Ukrainian children.\n\nThe orders were dismissed by Moscow as \'void\', and with Russia not a party to the ICC it is unclear if or how Putin could ever be extradited to face the charge.\n\nThe warrant was issued by ICC just days before Chinese President Xi Jinping\'s visit to Russia, an official trip that the Chinese premier described as a \'journey of friendship, co-operation and peace\'.\n\nWATCH | Russia, China and Iran conduct naval exercise, raises concerns in West\n\nXi landed in Moscow on Monday where he will be holding a meeting with Putin and signing an accord before he departs for Beijing on Wednesday.\n\n\'The two sides will practice genuine multilateralism, promote democracy in international relations, build a multipolar world, improve global governance and contribute to world development and progress,\' Wang said at the press briefing on Monday.\n\n(With inputs from agencies)\n\nYou can now write for wionews.com and be a part of the community. Share your stories and opinions with us here.'''


print(ss.replace('\n',''))

#%%%%%%%%%%%%%%%%%%%%%

page_size = 5  # 每页显示的条目数
total_items = 99  # 总共的条目数

# 计算总共需要显示多少页
total_pages = (total_items + page_size - 1) // page_size

# 打印每一页的起始和结束条目编号
for page in range(total_pages):
    start_item = page * page_size
    end_item = min((page + 1) * page_size, total_items)
    print(f"Page {page + 1}: items {start_item + 1}-{end_item}")
    
#%%%%%%%%%%%%%%%%%%%%%%

page_size = 5  # 每页条数
total_items = 88  # 总条数
total_pages = (total_items + page_size - 1) // page_size  # 总页数

for page in range(1, total_pages + 1):
    start_item = (page - 1) * page_size
    end_item = min(page * page_size, total_items)-1
    print(f"Page {page}: {start_item}-{end_item}")
    
#%%%%%%%%%%%%


page = 2
start_item = (page - 1) * page_size
end_item = min(page * page_size, total_items)-1
print(f"Page {page}: {start_item}-{end_item}")