# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 16:50:42 2023

@author: Administrator
"""

#export
# 【整体流程】
# 在app.py程序文件中，app是flask的实例，功能就是接受来自web服务器的请求，
# 1、浏览器将请求给web服务器，web服务器将请求给app ,
# 2、app收到请求，通过路由找到对应的视图函数，然后将请求处理，得到一个响应response
# 3、然后app将响应返回给web服务器，
# 4、web服务器返回给浏览器，
# 5、浏览器展示给用户观看，流程完毕。

# 【1、初始化】
# 所有的Flask都必须创建程序实例
# web服务器把客户端所有的请求都转发给这个程序实例，程序实例是Flask的对象
# 一般情况下用如下方法实例化
# Flask类只有一个必须指定的参数，即程序主模块或者包的名字，__name__是系统变量，该变量指的是本py文件的文件名

from flask import Flask, render_template, request, redirect
import random
import linecache
import json
app = Flask(__name__)
 
 
 
# 【2、路由和视图函数】
# 客户端发送url给web服务器，web服务器将url转发给flask程序实例，程序实例
# 需要知道对于每一个url请求启动哪一部分代码，所以保存了一个url和python函数的映射关系。
# 处理url和函数之间关系的程序，称为路由
# 在flask中，定义路由最简便的方式，是使用程序实例的app.route装饰器，把装饰的函数注册为路由
 
 
@app.route('/privacy')
def cdc_say():
    return render_template('privacy.html')
    # return "Hello, Flask !"
 
@app.route('/cancel')
def angela_say():
    return render_template('cancel.html')
 
@app.route('/user')
def alex_say():
    return render_template('user.html')
 
@app.route('/code')
def User_Agent():
    txt = open(r'/root/yan.txt', 'rb')
    data = txt.read().decode('utf-8')  # python3一定要加上这句不然会编码报错！
    txt.close()

    # 获取txt的总行数！
    n = data.count('\n')
    #print("总行数", n)
    # 选取随机的数
    i = random.randint(1, (n + 1))
    #print("本次使用的行数", i)
    ###得到对应的i行的数据
    line=linecache.getline(r'/root/yan.txt', i)
    #print(line)
    
    data = {
       "code": "OK",
       "result":{
        "pic_url":line.replace('\n',''),
        "answer":line.split('/')[-1].split('.')[0]
        }
    }
    # 第一种
    response = json.dumps(data)  # 将python的字典转换为json字符串
    return response,200,{"Content-Type":"application/json"}

    
    
    #return line
# 【3、程序实例用run方法启动flask集成的开发web服务器】
#  __name__ == '__main__'是python常用的方法，表示只有直接启动本脚本时候，才用app.run方法
#  如果是其他脚本调用本脚本，程序假定父级脚本会启用不同的服务器，因此不用执行app.run()
#  服务器启动后，会启动轮询，等待并处理请求。轮询会一直请求，直到程序停止。
 
if __name__ == '__main__':
 
    print('dd',__name__)
 
    app.run(host="10.0.20.6", port=5000, debug=True)
 
# app.run( )