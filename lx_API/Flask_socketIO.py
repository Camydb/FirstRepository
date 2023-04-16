# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 15:08:28 2023

@author: Administrator
"""

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
 
socketio = SocketIO()
socketio.init_app(app, cors_allowed_origins='*')
 
name_space = '/dcenter'
 
@app.route('/')
def index():
    
    return render_template('index.html')
 

@app.route('/push')
def push_once():
    event_name = 'dcenter'
    broadcasted_data = {'data': "test message!"}
    socketio.emit(event_name, broadcasted_data, broadcast=False, namespace=name_space)
    # print('test message!')
    return 'done!'
 
 
# @socketio.on('connect', namespace=name_space)
# def connected_msg():
#     print('client connected.')
 
 
# @socketio.on('disconnect', namespace=name_space)
# def disconnect_msg():
#     print('client disconnected.')
 
 
# @socketio.on('my_event', namespace=name_space)
# def mtest_message(message):
#     print(message)
#     emit('my_response',
#          {'data': message['data'], 'count': 1})
 
 
if __name__ == '__main__':
    socketio.run(app,port=5001)
    # socketio.run(host="10.0.20.6", port=5000, debug=True)
    # app.run(host="10.0.20.6", port=5000, debug=True)
    # ,allow_unsafe_werkzeug=True



#%%%%%%%%%%%%%%%%%%%%%%%%%%%

import datetime
import time
import requests

while True: 
    # if time.localtime().tm_hour == 8: # 运行定时任务 
    if time.localtime().tm_sec == 0:
        re = requests.get(url='https://v1.hitokoto.cn/?encode=text')
        print(re.text)
        # now = datetime.datetime.now().isoformat()
        # print(now)
        time.sleep(1)
    



'''



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


# # 未命名事件
# @socketio.on('message')
# def handle_message(message):
#      print('received message: ' + message)

# # 自定义命名事件
# @socketio.on('my_event')
# def handle_message(p1, p2):  # 形参
#      print('received message: ', p1,  p2)

# # 命名空间namespace，它允许客户端在同一个物理套接字上复用几个独立的连接
# @socketio.on('my_event', namespace='/test')
# def handle_my_custom_namespace_event(p):
#       print('received: ' + str(p))

# # 返回值给客户端
# def handle_message(p):  # 形参
#      print(p)
#      return 123  # 客户端将收到这个返回值

# #########################################################
# # on_event方法，效果等同于装饰器
# def my_function_handler(data):
#       pass

# socketio.on_event('my event', my_function_handler, namespace='/test')


# @socketio.on('event1')
# def handle_event1(p):
#       send('hello world')

# @socketio.on('event2')
# def handle_event2(p):
#       emit('event2 response', 'hi world') # event2 response为该事件的命名

# # namespace
# @socketio.on('event3')
# def handle_event3():
#       emit('event3 response', '333',  namespace='/chat')

# # 多个值用元祖的形式
# @socketio.on('event4')
# def handle_event4():
#       emit('event4 response', ('4', '44', '444'), namespace='/chat')

# # 回调函数
# def ack():
#       print ('message was received!')

# @socketio.on('event5')
# def handle_event5():
#       emit('event5 response', '555', callback=ack)
# # 当使用回调函数时，客户端接收到一个回调函数来接收消息。 客户端应用程序调用回调函数后，调用相应的服务器端回调。 
# # 如果用参数调用客户端回调，则这些回调也作为参数提供给服务器端回调。




if __name__ == '__main__':
    socketio.run(app,allow_unsafe_werkzeug=True)
    # ,allow_unsafe_werkzeug=True
# socketio.run（）函数封装了Web服务器的启动，代替了app.run（）标准的Flask开发服务器启动。 
# 当应用程序处于调试模式时，Werkzeug开发服务器仍在socketio.run（）中使用和正确配置。 
# 在生产模式下首选使用eventlet Web服务器，否则使用gevent Web服务器。 
# 如果没有安装eventlet和gevent，则使用Werkzeug开发Web服务器。


#%%%%%%%%%%%%%%%%%%%


from flask_socketio import Namespace, emit

class MyCustomNamespace(Namespace):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_my_event(self, data):
        emit('my_response', data)

socketio.on_namespace(MyCustomNamespace('/test'))

if __name__ == '__main__':
    socketio.run(app,allow_unsafe_werkzeug=True)
'''