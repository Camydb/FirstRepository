import sys
from PyQt5.QtWidgets import *
# from gup import gupimg
# import pyui0823_2
import ctypes
import copy
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QMessageBox, QFileDialog, QCheckBox
from PyQt5.QtGui import QIcon
from pyppeteer_stealth import stealth
# from pyqt5_plugins.examplebutton import QtWidgets
import psutil
# from pyqt5_plugins.examplebutton import QtWidgets

# import pyui0906
import pyui1013 as pyui
import qh1
import pt1
import gjc
import huoke_daochu
import ws_tuisong
import xiaozu_daochu
# import selenium.webdriver.support.ui as ui
import time
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
import json
import pandas as pd
import re
import datetime
# import threading
# from PyQt5.QtWidgets import *
# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QInputDialog, QTextBrowser
import sys
import os
import pickle
import dq6
import xz1
# import goto
# from goto import with_goto
# from dominate.tags import label

# from PyQt5.QtGui import QIcon
# import xlrd
# import datetime
# import time
from openpyxl import Workbook
from openpyxl.styles import Border, Side, PatternFill, Font, GradientFill, Alignment
import requests

# QApplication.processEvents()
# from selenium.common.exceptions import TimeoutException
import ctypes
# from PyQt5.QtWidgets import *
import re
import json
# import threading
# from gup0804.gup import myComboBoxUtil
import sqlite3
import numpy as np
import requests
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
import random
import json
# from browsermobproxy import Server
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from fake_useragent import UserAgent
# from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
# from lxml import etree
# from requests.auth import HTTPBasicAuth
import wancishengcheng
# import youdao_translate as yd
import jinshan_translate as jinshan


import WS_login
import F_diqu
import fb_friends
import fb_diqu
import ins_tiewen
import ins_LB
import gg_map
import email_qunfa
import get_group
import group_munber
import fb_pages
import fb_groups
import fb_lives
import ins_homePage
import ins_search
# import baige
from pyppeteer import launch
from pyppeteer import launcher
import asyncio
import nest_asyncio
import base64
import ctypes
nest_asyncio.apply()
from PIL import Image
from loguru import logger
import pyautogui

questions_di_dic = {
    "taxis": "/m/0pg52",
    "bus": "/m/01bjv",
    "school bus": "/m/02yvhj",
    "motorcycles": "/m/04_sv",
    "tractors": "/m/013xlm",
    "chimneys": "/m/01jk_4",
    "crosswalks": "/m/014xcs",
    "traffic lights": "/m/015qff",
    "bicycles": "/m/0199g",
    "parking meters": "/m/015qbp",
    "cars": "/m/0k4j",
    "vehicles": "/m/0k4j",
    "bridges": "/m/015kr",
    "boats": "/m/019jd",
    "palm trees": "/m/0cdl1",
    "mountains or hills": "/m/09d_r",
    "fire hydrant": "/m/01pns0",
    "fire hydrants": "/m/01pns0",
    "a fire hydrant": "/m/01pns0",
    "stairs": "/m/01lynh",
    "出租车": "/m/0pg52",
    "巴士": "/m/01bjv",
    "校车": "/m/02yvhj",
    "摩托车": "/m/04_sv",
    "拖拉机": "/m/013xlm",
    "烟囱": "/m/01jk_4",
    "人行横道": "/m/014xcs",
    "红绿灯": "/m/015qff",
    "自行车": "/m/0199g",
    "停车计价表": "/m/015qbp",
    "汽车": "/m/0k4j",
    "桥": "/m/015kr",
    "船": "/m/019jd",
    "棕榈树": "/m/0cdl1",
    "山": "/m/09d_r",
    "消防栓": "/m/01pns0",
    "楼梯": "/m/01lynh",
    "机动车": "/m/0k4j",
    "过街人行道": "/m/014xcs",
    "小轿车": "/m/0k4j",
    "公交车": "/m/01bjv",
}
import urllib3
urllib3.disable_warnings()


class insid(QThread):  # 步骤1.创建一个线程实例
    mysignal = pyqtSignal(list,str)  # 创建一个自定义信号，参数
    try:
        pkl_file = open('inscook1.pkl', 'rb')
        self.cookies = pickle.load(pkl_file)
        pkl_file.close()
    except:
        pass

    # new_loop = asyncio.new_event_loop()
    def __init__(self):
        super(insid, self).__init__()

    def stop(self):
        # self.terminate()
        # self.mysignal.emit('停止获取')
        try:
            self.loop1.run_until_complete(self.guan())

            self.terminate()
        except:
            pass

    async def guan(self):
        # await self.page.cookies()  # cookies
        cookies_list = await self.page.cookies()
        # print(cookies_list)
        output = open('inscook1.pkl', 'wb')
        pickle.dump(cookies_list, output)
        output.close()
        self.mysignal.emit(['保存ins账号'],'label')
        # self.loop1.close()
        await self.browser.close()

    def run(self):
        self.loop1 = asyncio.new_event_loop()
        self.loop1.run_until_complete(self.main3())

    async def main3(self):

        self.mysignal.emit(['请登录账号'],'label')
        if '--enable-automation' in launcher.DEFAULT_ARGS:
            launcher.DEFAULT_ARGS.remove("--enable-automation")
        self.browser = await launch(headless=False, userDataDir=r'./instext', dumpio=True, autoClose=False,
                                    executablePath='chrome_win64/chrome.exe',
                                    handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False,
                                    args=['--no-sandbox', '--window-size=1920,1080', '--disable-infobars',
                                          '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'])  # 进入有头模式

        self.page = await self.browser.newPage()
        # 设置页面视图大小
        await self.page.setViewport({'width': 1920, 'height': 1080})
        # 是否启用JS，enabled设为False，则无渲染效果
        await self.page.setJavaScriptEnabled(enabled=True)
        # self.mysignal.emit('开始获取')
        try:
            await self.page.setCookie(*self.cookies)
        except:
            pass

        url = 'https://www.instagram.com/'

        await self.page.goto(url)
        await self.page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')

        await asyncio.sleep(300)


class fbid(QThread):  # 步骤1.创建一个线程实例
    mysignal = pyqtSignal(list,str)  # 创建一个自定义信号，参数
    try:
        pkl_file = open('fbcook1.pkl', 'rb')
        self.cookies = pickle.load(pkl_file)
        pkl_file.close()
    except:
        pass

    # new_loop = asyncio.new_event_loop()
    def __init__(self):
        super(fbid, self).__init__()

    def stop(self):
        # self.terminate()
        # self.mysignal.emit('停止获取')
        try:
            self.loop1.run_until_complete(self.guan())

            self.terminate()
        except:
            pass

    async def guan(self):
        # await self.page.cookies()  # cookies
        cookies_list = await self.page.cookies()
        # print(cookies_list)
        output = open('fbcook1.pkl', 'wb')
        pickle.dump(cookies_list, output)
        output.close()
        self.mysignal.emit(['保存账号'],'label')
        # self.loop1.close()
        await self.browser.close()

    def run(self):
        self.loop1 = asyncio.new_event_loop()
        self.loop1.run_until_complete(self.main3())

    async def main3(self):

        # self.mysignal.emit(['请登录账号'])
        if '--enable-automation' in launcher.DEFAULT_ARGS:
            launcher.DEFAULT_ARGS.remove("--enable-automation")
        self.browser = await launch(headless=False, userDataDir=r'./fbtext', dumpio=True, autoClose=False,
                                    executablePath='chrome_win64/chrome.exe',
                                    handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False,
                                    args=['--no-sandbox', '--window-size=1920,1080', '--disable-infobars',
                                          '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'])  # 进入有头模式

        self.page = await self.browser.newPage()
        # 设置页面视图大小
        await self.page.setViewport({'width': 1920, 'height': 1080})
        # 是否启用JS，enabled设为False，则无渲染效果
        await self.page.setJavaScriptEnabled(enabled=True)
        # self.mysignal.emit('开始获取')

        try:
            await self.page.setCookie(*self.cookies)
        except:
            pass

        url = 'https://www.facebook.com/'

        await self.page.goto(url)
        await self.page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')

        await asyncio.sleep(300)


class fbzhuye(QThread):  # 步骤1.创建一个线程实例
    mysignal = pyqtSignal(list,str)  # 创建一个自定义信号，参数

    def __init__(self,headless):
        self.headless = headless
        super(fbzhuye, self).__init__()
        conn = sqlite3.connect("HKHMZY.db")
        try:
            conn.execute("""
            CREATE TABLE STUD_ZY(
            QNAME TEXT NOT NULL,
            QID TEXT,
            QURL TEXT NOT NULL,
            TIME TEXT NOT NULL)
            """)
        except:
            pass
        conn.close()

        try:
            pkl_file = open('fbcook1.pkl', 'rb')
            self.cookies = pickle.load(pkl_file)
        except:
            self.mysignal.emit(['请先登录'],'label')
            pass

    def stop(self):
        # self.terminate()
        self.mysignal.emit(['停止获取'],'label')
        try:
            asyncio.new_event_loop().run_until_complete(self.guan())
        except:
            pass

    async def guan(self):
        await self.browser.close()

    def baocun(self, NAME, URL):
        conn = sqlite3.connect("HKHMZY.db")
        stime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn.execute(
            "INSERT INTO STUD_ZY (QNAME,QID,QURL,TIME) VALUES ('{}','{}','{}','{}')".format(NAME, '', URL, stime))
        conn.commit()
        # print ("记录插入成功!")
        conn.close()

    def run(self):

        asyncio.new_event_loop().run_until_complete(self.mainzb())

    async def mainzb(self):
        self.mysignal.emit(['开始主页获取'],'label')
        zyurl = str(main.ZYURL[0])
        if '--enable-automation' in launcher.DEFAULT_ARGS:
            launcher.DEFAULT_ARGS.remove("--enable-automation")

        self.browser = await launch(headless=self.headless, dumpio=True, autoClose=False,
                                    executablePath='chrome_win64/chrome.exe',
                                    handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False,
                                    args=['--no-sandbox', '--window-size=1920,1080', '--disable-infobars',
                                          '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'])  # 进入有头模式

        self.page = await self.browser.newPage()
        # 设置页面视图大小
        await self.page.setViewport(viewport={'width': 1920, 'height': 1080})
        # 是否启用JS，enabled设为False，则无渲染效果
        await self.page.setJavaScriptEnabled(enabled=True)

        try:
            await self.page.setCookie(*self.cookies)
        except:
            self.mysignal.emit(['未登录状态'],'label')
        await self.page.goto(zyurl)
        await asyncio.sleep(5)

        i = 1
        while True:
            await self.page.evaluate('window.scrollBy(0,document.body.scrollHeight)')
            # await self.page.keyboard.press('Space')
            await asyncio.sleep(3)
            try:
                await self.page.evaluate(f"document.querySelectorAll('div >span >div >span:nth-child(2) >span >span')[{i - 1}].scrollIntoView()")
                # await page.evaluate(f"document.querySelectorAll('span div span:nth-child(2) span span')[{i-1}].click()")
                await self.page.evaluate(
                    f"document.querySelectorAll('div >span >div >span:nth-child(2) >span >span')[{i - 1}].click()")
            except Exception as e:
                print(e)
                time.sleep(2)
                continue
            i +=1
            li = []
            # await asyncio.sleep(3)
            name1 = ''
            while True:
                await asyncio.sleep(3)
                divs = await self.page.xpath(
                    '/html/body/div[1]/div[1]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[1]/div/div/div/div[2]/div[1]/div/div/div/span/div/a')
                print(divs)
                #if divs:
                    #break
                for div in divs:
                    title = await (await div.getProperty('textContent')).jsonValue()
                    href = await (await div.getProperty('href')).jsonValue()
                    href = href.split('_')[0]
                    href = href[:-1]
                    if title not in li:
                        li.append(title)
                        # print(title, href)
                        try:
                            self.mysignal.emit([title, href],'table')
                            self.baocun(title, href)
                        except:
                            pass
                
                
                name = await self.page.evaluate('(element) => element.textContent', divs[-1])
                
                if name == name1:
                    close_ = await self.page.xpath('//div[@aria-label="关闭" or @aria-label="Close" ]')
                    await self.page.evaluate('node => node.click()', close_[0])
                    # await self.page.evaluate('node => node.click()', close_[0])
                    time.sleep(2)
                    #await self.page.mouse.move(x=200, y=100)  # 鼠标移动到该位置
                    #await self.page.mouse.down()  # 鼠标点击
                    #await self.page.mouse.up()  # 鼠标放开操作
                    print('wdedsfvdfbs')
                    break
                else:
                    name1 = name
                    
                    
                
                await self.page.evaluate('(element) => element.scrollIntoView()', divs[-1])  # 滚动到指定标签元素位置
                time.sleep(2.5)
                
                


class zhibo(QThread):  # 步骤1.创建一个线程实例
    mysignal = pyqtSignal(list,str)  # 创建一个自定义信号，参数

    def __init__(self,headless):
        self.headless = headless
        super(zhibo, self).__init__()
        conn = sqlite3.connect("HKHMZB.db")
        try:
            conn.execute("""
            CREATE TABLE STUD_ZB(
            QNAME TEXT NOT NULL,
            QID TEXT,
            QURL TEXT NOT NULL,
            TIME TEXT NOT NULL)
            """)
        except:
            pass
        conn.close()

        try:
            pkl_file = open('fbcook1.pkl', 'rb')
            self.cookies = pickle.load(pkl_file)
        except:
            self.mysignal.emit(['请先登录'],'label')
            pass

    def stop(self):
        # self.terminate()
        self.mysignal.emit(['停止获取'],'label')
        try:
            asyncio.new_event_loop().run_until_complete(self.guan())
        except:
            pass

    async def guan(self):
        await self.browser.close()

    def baocun(self, NAME, LJ, ID):
        conn = sqlite3.connect("HKHMZB.db")
        stime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn.execute(
            "INSERT INTO STUD_ZB (QNAME,QID,QURL,TIME) VALUES ('{}','{}','{}','{}')".format(NAME, ID, LJ, stime));
        conn.commit()
        # print ("记录插入成功!")
        conn.close()

    def run(self):

        asyncio.new_event_loop().run_until_complete(self.mainzb())

    async def mainzb(self):
        self.mysignal.emit(['开始直播获取'],'label')
        zburl = str(main.ZBURL[0])

        print(zburl)

        if '--enable-automation' in launcher.DEFAULT_ARGS:
            launcher.DEFAULT_ARGS.remove("--enable-automation")

        self.browser = await launch(headless=self.headless, dumpio=True, autoClose=False,
                                    executablePath='chrome_win64/chrome.exe',
                                    handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False,
                                    args=['--no-sandbox', '--window-size=1920,1080', '--disable-infobars',
                                          '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'])  # 进入有头模式

        self.page = await self.browser.newPage()
        # 设置页面视图大小
        await self.page.setViewport({'width': 1920, 'height': 1080})
        # 是否启用JS，enabled设为False，则无渲染效果
        await self.page.setJavaScriptEnabled(enabled=True)

        try:
            await self.page.setCookie(*self.cookies)
        except:
            self.mysignal.emit(['未登录状态'],'label')
        await self.page.goto(zburl)

        await self.page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
        while True:
            ready = await self.page.evaluate("document.readyState")
            await asyncio.sleep(2)
            if ready == "complete":
                print(ready)
                break
        await asyncio.sleep(1)
        try:
            # await self.page.click(".x16hj40l")
            
            
            dianzan = await self.page.xpath('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div[2]/div[1]/div[3]/div/div/div/div/div[2]/div/div[1]/div/span/span/span')
            await self.page.evaluate('node => node.click()', dianzan[0])
            time.sleep(2)
            await asyncio.sleep(3)
            ap = 0
            piname = ''
            yichang = 0
            while True:

                try:
                    items = await self.page.xpath(
                        '//*[contains(@id,"mount_0_0_")]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[1]')
                    for item in items:
                        # title_str1 = await (await item.getProperty('textContent')).jsonValue()
                        # print(title_str1)
                        # print(type(title_str1))
                        # print('\n')

                        link = await item.xpath('.//a')
                        try:
                            for ii in range(ap, len(link)):

                                ap = ap + 1
                                title_str1 = await (await link[ii].getProperty('textContent')).jsonValue()
                                title_link = await (await link[ii].getProperty('href')).jsonValue()
                                if title_str1 != '' and title_link != '':
                                    id1 = re.findall(r"id=\d+", title_link)
                                    # print(title_str1)
                                    # print(title_link)

                                    # print('-----------------------')

                                    if id1 != []:
                                        id2 = re.findall(r"\d+", id1[0])
                                        self.mysignal.emit([title_str1, title_link, id2[0]],'table')
                                        self.baocun(title_str1, title_link, id2[0])
                                    else:
                                        self.mysignal.emit([title_str1, title_link, ''],'table')
                                        self.baocun(title_str1, title_link, '空')

                                    # print(sstr)

                        except:
                            print('空')
                    await asyncio.sleep(2)
                    elements = await self.page.querySelectorAll('a')
                    namee = await self.page.evaluate('(element) => element.textContent', elements[-1])
                    # print(namee)
                    if namee == piname:
                        yichang = yichang + 1
                    else:
                        piname = namee
                        yichang = 0
                    await self.page.evaluate('(element) => element.scrollIntoView()', elements[-1])
                    if yichang >= 5:
                        self.mysignal.emit(['任务结束'],'label')
                        await self.browser.close()
                        break
                except:
                    self.mysignal.emit(['Abnormal'],'label')
                    yichang = yichang + 1
                    if yichang >= 3:
                        break
                    await asyncio.sleep(3)
                    pass
        except:
            try:
                self.mysignal.emit(['链接无效'],'label')
                await self.browser.close()
            except:
                pass


class facebook(QThread):  # 步骤1.创建一个线程实例
    mysignal = pyqtSignal(list,str)  # 创建一个自定义信号，参数

    def __init__(self,headless):
        self.headless=headless
        super(facebook, self).__init__()
        conn = sqlite3.connect("HKHMFB.db")
        try:
            conn.execute("""
            CREATE TABLE STUD_FB(
            QNAME TEXT NOT NULL,
            QID TEXT NOT NULL,
            QURL TEXT NOT NULL,
            TIME TEXT NOT NULL)
            """)
        except:
            pass
        conn.close()

        try:
            pkl_file = open('fbcook1.pkl', 'rb')
            self.cookies = pickle.load(pkl_file)
        except:
            self.mysignal.emit(['请先登录'],'label')
            pass

    def stop(self):

        self.mysignal.emit(['停止获取......'],'label')
        try:
            asyncio.new_event_loop().run_until_complete(self.guan())
        except:
            pass
        # self.terminate()

    async def guan(self):
        await self.browser.close()

    def baocun(self, NAME, ID, LJ):
        conn = sqlite3.connect("HKHMFB.db")
        stime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn.execute(
            "INSERT INTO STUD_FB (QNAME,QID,QURL,TIME) VALUES ('{}','{}','{}','{}')".format(NAME, ID, LJ, stime))
        conn.commit()
        # print ("记录插入成功!")
        conn.close()

    def run(self):
        asyncio.new_event_loop().run_until_complete(self.mainfb())

    async def mainfb(self):
        self.mysignal.emit(['开始获取'],'label')
        fburl = str(main.LJURL[0] + '/members')
        print(fburl)
        if '--enable-automation' in launcher.DEFAULT_ARGS:
            launcher.DEFAULT_ARGS.remove("--enable-automation")

        self.browser = await launch(headless=self.headless, dumpio=True, autoClose=False,
                                    executablePath='chrome_win64/chrome.exe',
                                    handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False,
                                    args=['--no-sandbox', '--window-size=1920,1080', '--disable-infobars',
                                          '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'])  # 进入有头模式

        self.page = await self.browser.newPage()

        # context = await self.browser.createIncognitoBrowserContext()
        # self.page = await context.newPage()

        # 设置页面视图大小
        await self.page.setViewport({'width': 1920, 'height': 1080})
        # 是否启用JS，enabled设为False，则无渲染效果
        await self.page.setJavaScriptEnabled(enabled=True)
        # await self.page.setCookie(*self.cookies)
        try:
            await self.page.setCookie(*self.cookies)
        except:
            self.mysignal.emit(['未登录状态'],'label')
        await self.page.goto(fburl)

        await self.page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
        await asyncio.sleep(1)
        # await self.page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
        await self.page.keyboard.press('Space')

        ap = 10
        app = 1
        yichang = 0
        lie = []
        while True:
            try:
                items = await self.page.xpath('//*[contains(@id,"mount_0_0_")]/div/div[1]/div/div[3]')
                for item in items:
                    link = await item.xpath('.//a')
                    for ii in range(ap, len(link)):
                        ap = ap + 1
                        title_str1 = await (await link[ii].getProperty('textContent')).jsonValue()
                        title_link = await (await link[ii].getProperty('href')).jsonValue()
                        if title_str1 != '' and title_link != '':
                            uid = title_link.split('/')[-2]
                            if title_str1 not in lie and uid.isdigit():
                                lie.append(title_str1)
                                xixi = 'https://www.facebook.com/profile.php?id='
                                llink = str(xixi + str(uid))
                                self.mysignal.emit([uid, llink, title_str1],'table')
                                try:
                                    self.baocun(title_str1, uid, llink)
                                except:
                                    pass

                await self.page.keyboard.press('Space')
                await asyncio.sleep(1)
                await self.page.keyboard.press('Space')
                await asyncio.sleep(3)
                yichang = 0

            except:
                await asyncio.sleep(5)
                self.mysignal.emit(['Abnormal'],'label')
                # await asyncio.sleep(5)
                yichang = yichang + 1
                if yichang >= 3:
                    break

                # pass


class ins(QThread):  # 步骤1.创建一个线程实例
    mysignal = pyqtSignal(list,str)  # 创建一个自定义信号，参数

    def __init__(self,headless):
        self.headless=headless
        super(ins, self).__init__()
        conn = sqlite3.connect("HKHMINS.db")
        try:
            conn.execute("""
            CREATE TABLE STUD_INS(
            QNAME TEXT NOT NULL,
            QID TEXT,
            QURL TEXT NOT NULL,
            TIME TEXT NOT NULL)
            """)
        except:
            pass
        conn.close()

        try:
            pkl_file = open('inscook1.pkl', 'rb')
            self.cookies = pickle.load(pkl_file)
        except:
            self.mysignal.emit(['请先登录'],'label')
            pass

    def stop(self):
        # self.terminate()
        self.mysignal.emit(['停止获取'],'label')
        try:
            asyncio.new_event_loop().run_until_complete(self.guan())
        except:
            pass

    async def guan(self):
        await self.browser.close()

    def baocun(self, NAME, LJ, ID):
        conn = sqlite3.connect("HKHMINS.db")
        stime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn.execute(
            "INSERT INTO STUD_INS (QNAME,QID,QURL,TIME) VALUES ('{}','{}','{}','{}')".format(NAME, ID, LJ, stime))
        conn.commit()
        # print ("记录插入成功!")
        conn.close()

    def run(self):
        asyncio.new_event_loop().run_until_complete(self.insfs())

    async def insfs(self):
        self.mysignal.emit(['开始INS粉丝获取'],'label')
        insurl = main.lineEdit_28.text()
        print(insurl)
        insurl = str(insurl + 'followers/')
        if '--enable-automation' in launcher.DEFAULT_ARGS:
            launcher.DEFAULT_ARGS.remove("--enable-automation")

        self.browser = await launch(headless=self.headless, dumpio=True, autoClose=False,
                                    handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False,
                                    executablePath='chrome_win64/chrome.exe',
                                    args=['--no-sandbox', '--window-size=1920,1080', '--disable-infobars',
                                          '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'])  # 进入有头模式

        self.page = await self.browser.newPage()
        # 设置页面视图大小
        await self.page.setViewport({'width': 1920, 'height': 1080})
        # 是否启用JS，enabled设为False，则无渲染效果
        await self.page.setJavaScriptEnabled(enabled=True)
        try:
            await self.page.setCookie(*self.cookies)
        except:
            self.mysignal.emit(['未登录状态'],'label')
        await self.page.goto(insurl)

        await self.page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
        await asyncio.sleep(3)
        ap = 0
        piname = ''
        bk = 0
        yichang = 0
        while True:
            try:
                items = await self.page.xpath('//*[contains(@id,"mount_0_0_")]/div/div/div/div[2]')
                for item in items:
                    # title_str1 = await (await item.getProperty('textContent')).jsonValue()
                    # print(title_str1)
                    # print(type(title_str1))
                    # print('\n')

                    link = await item.xpath('.//a')

                    for ii in range(ap, len(link)):

                        ap = ap + 1
                        title_str1 = await (await link[ii].getProperty('textContent')).jsonValue()
                        title_link = await (await link[ii].getProperty('href')).jsonValue()
                        if title_str1 != '' and title_link != '':
                            # print(title_str1)
                            # print(title_link)
                            # print('-----------------------')
                            sstr = str(title_link + '\t' + title_str1)
                            self.mysignal.emit([title_str1,title_link],'table')
                            self.baocun(title_str1, title_link, title_str1)
                await asyncio.sleep(1)
                elements = await self.page.querySelectorAll('a')
                namee = await self.page.evaluate('(element) => element.textContent', elements[-1])
                print(namee)
                if namee == piname:
                    bk = bk + 1
                    if bk > 8:
                        self.mysignal.emit(['任务结束'],'label')
                        await self.browser.close()
                        break
                else:
                    bk = 0
                    piname = namee
                await self.page.evaluate('(element) => element.scrollIntoView()', elements[-1])
                await asyncio.sleep(1)
            except:
                self.mysignal.emit(['INS Abnormal'],'label')
                yichang = yichang + 1
                if yichang >= 3:
                    break
                await asyncio.sleep(2)
                pass


class zhuike(QThread):
    mysignal = pyqtSignal(str)

    def __init__(self):
        super(zhuike, self).__init__()

    def stop(self):
        self.terminate()

    def run(self):
        shulian = main.lineEdit.text()
        if shulian[0] == '1' and int(shulian[1:]) == 0:
            a = len(shulian) - 1
        else:
            a = len(shulian)
        for num in main.list_num:
            for i in range(int(shulian)):
                new_num = num[:-a] + str(i).zfill(a)
                main.list_liebian.append(num)
                self.mysignal.emit(new_num)
                time.sleep(0.001)


class google(QThread):  # 步骤1.创建一个线程实例
    mysignal = pyqtSignal(list,str)  # 创建一个自定义信号，参数

    # new_loop = asyncio.new_event_loop()
    def __init__(self,headless):
        self.headless=headless
        super(google, self).__init__()
        conn = sqlite3.connect("HKHM.db")
        try:
            conn.execute("""
            CREATE TABLE STUD_GJC(
            QGJC TEXT NOT NULL,
            QNUM TEXT NOT NULL,
            TIME TEXT NOT NULL)
            """)
        except:
            pass
        conn.close()

    def stop(self):
        # self.terminate()
        self.mysignal.emit(['STOP'],'label')

        asyncio.new_event_loop().run_until_complete(self.guan())

        # self.terminate()

    async def guan(self):
        # await self.page.evaluate("window.stop()")
        await self.browser.close()

    def baocun(self, data, gjc):
        conn = sqlite3.connect("HKHM.db")
        stime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for istr in range(0, len(data)):
            ddd = data[istr].replace(',', '')
            ddd = ddd.replace(' ', '')
            print(ddd)
            conn.execute("INSERT INTO STUD_GJC (QGJC,QNUM,TIME) VALUES ('{}','{}','{}')".format(gjc, ddd, stime))
        conn.commit()
        print("记录插入成功!")
        conn.close()

    def run(self):
        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(self.main2())

    async def main2(self):
        if '--enable-automation' in launcher.DEFAULT_ARGS:
            launcher.DEFAULT_ARGS.remove("--enable-automation")
        self.mysignal.emit(['START'],'label')
        self.browser = await launch(userDataDir=r'./fbtext', headless=self.headless, dumpio=True, autoClose=True,
                                    handleSIGINT=False, executablePath='chrome_win64/chrome.exe',
                                    handleSIGTERM=False, handleSIGHUP=False,
                                    args=['--no-sandbox', '--window-size=1920,1080', '--disable-infobars',
                                          '--log-level=3',
                                          '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'])  # 进入有头模式
        # web = await self.browser.createIncognitoBrowserContext()
        # self.page = await web.newPage()
        self.page = await self.browser.newPage()
        # await stealth(self.page)
        # 设置页面视图大小
        await self.page.setViewport({'width': 1920, 'height': 1080})
        # 是否启用JS，enabled设为False，则无渲染效果
        await self.page.setJavaScriptEnabled(enabled=True)
        # self.mysignal.emit('开始获取')
        # QH = qh.qhh
        # GJC = gjc.gjcc
        # print(GJC)
        # print(QH)
        await asyncio.sleep(2)
        url = 'https://www.google.com/'
        print('一阶段')

        await self.page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')

        pkl_file = open('renwu.pkl', 'rb')
        rw = pickle.load(pkl_file)
        pkl_file.close()
        keys = list(rw.keys())
        JD = len(keys)

        main.progressBar_10.setValue(1)

        while True:

            pkl_file = open('renwu.pkl', 'rb')
            rw = pickle.load(pkl_file)
            pkl_file.close()

            keys = list(rw.keys())
            jd = len(keys)

            rate = jd / JD

            rate_num = int(100 - int(rate * 100))
            print(rate_num)
            main.progressBar_10.setValue(rate_num)

            if len(keys) < 2:
                break

            KEY = keys[0]
            GJCx = rw[keys[0]]

            del rw[keys[0]]

            rwoutput = open('renwu.pkl', 'wb')
            pickle.dump(rw, rwoutput)
            rwoutput.close()

            await self.page.goto(url)
            await asyncio.sleep(2)
            await self.page.keyboard.type(KEY)
            await self.page.keyboard.press('Enter')

            inum = 1
            while inum < 29:
                try:
                    # await self.page.screenshot({'path': 'google1.png'})
                    # self.mysignal.emit('第{}页...'.format(inum))
                    await asyncio.sleep(3)

                    # await asyncio.sleep(10)
                    html = await self.page.content()
                    # html=brower.page_source
                    soup = BeautifulSoup(html, 'lxml')
                    # print (soup.prettify())
                    myjj = soup.find_all("div", class_="MjjYud")
                    # soup.find_all("div", class_="MjjYud")
                    biaoti = []
                    neirong = []
                    # await self.page.screenshot({'path': 'google1.png'})
                    for th in myjj:
                        # print(th.find_all('h3'))
                        try:
                            biaoti.append(th.find('h3').get_text())
                            neirong.append(th.find('div').get_text())
                        except:
                            pass

                    hao = []
                    for i in neirong:
                        # ret=re.match(r"^1(3[0-9]|5[012356789]|7[1235678]|8[0-9])\d{8}$",i)
                        i = i.replace(" ", "")
                        i = i.replace("/", "——")
                        i = i.replace(".", "——")
                        # i = i.replace("(", "")
                        # i = i.replace(")", "")
                        # print(i)

                        remove_chars = '[·’!"\#$%&\'()＃！（）*,-.:;<=>?\@，：?￥★、…．＞【】［］《》？“”‘’\[\\]^_`{|}~]'
                        i = re.sub(remove_chars, "", i)

                        # hao1 = re.findall(r"\+[0-9]+|[0-9]+", i)
                        # hao1 = re.findall(r"\+\d+|\d+", i)
                        hao1 = re.findall(r'\+{0,1}[0-9]\d*',i,re.S)
                        
                        # hao1 = re.sub(r'#.*$', "", i)
                        if hao1 != []:
                            hao.append(hao1)
                    for j in biaoti:
                        # ret=re.match(r"^1(3[0-9]|5[012356789]|7[1235678]|8[0-9])\d{8}$",i)
                        j = j.replace(" ", "")
                        j = j.replace("/", "——")
                        j = j.replace(".", "——")
                        # j = j.replace("-", "")
                        # print(i)

                        remove_chars = '[·’!"\#$%&\'()＃！（）*,-.:;<=>?\@，：?￥★、…．＞【】［］《》？“”‘’\[\\]^_`{|}~]'
                        j = re.sub(remove_chars, "", j)

                        # hao1 = re.findall(r"\+\d+|\d+", j)
                        hao1 = re.findall(r'\+{0,1}[0-9]\d*',j,re.S)

                        # hao1 = re.findall(r"\+[0-9]+|[0-9]+", i)
                        # hao1 = re.sub(r'#.*$', "", i)
                        if hao1 != []:
                            hao.append(hao1)

                    haoma = []
                    stime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    for h in hao:
                        for hh in h:
                            # print(hh)
                            if len(hh) > 7:
                                haoma.append(hh)
                                # hh3 = str('Key word: ' + GJCx + '\t Nunber: ' + hh + '\t Time: ' + stime)
                                self.mysignal.emit([GJCx, hh, stime],'table')
                    print(haoma)
                    if haoma != []:
                        self.baocun(haoma, GJCx)
                    else:
                        pass

                    if 'sorry' in self.page.url:
                        print('开始人机验证')
                        '''触发验证码'''
                        await self.page.evaluate(
                            "document.querySelectorAll('iframe')[0].contentDocument.querySelector('#recaptcha-anchor > div.recaptcha-checkbox-border').click()")
                        time.sleep(1)

                        location = ''
                        i = 0
                        while True:

                            '''查找问题'''
                            question = await self.page.evaluate(
                                "document.querySelectorAll('iframe')[2].contentDocument.querySelector('div.rc-imageselect-desc-wrapper > div > strong').textContent")
                            print(question)
                            time.sleep(1)

                            try:
                                # print('正常运行')
                                '''获取图片链接并转化编码'''
                                img_url = await self.page.evaluate('''() => {let img_ele = document.querySelectorAll('iframe')[2].contentDocument.querySelector('div.rc-image-tile-wrapper > img');
                                                                        let src = img_ele.getAttribute('src');
                                                                        return src;}
                                                                        ''')
                                # print(img_url)
                                # print('正常运行')
                                img_data = requests.get(img_url, verify=False).content
                                # print(img_data)
                                img_base64_string = base64.b64encode(img_data).decode('utf-8')
                                # print(img_base64_string)

                                '''图片识别'''
                                question_id = questions_di_dic.get(question)
                                print(question_id)
                                if question_id:
                                    data = {
                                        "clientKey": 'e9f38127af721b4a15fa28ffe59472e09e9636a211549',
                                        "task": {
                                            "confidence": 0.5,
                                            "type": "ReCaptchaV2Classification",
                                            "image": img_base64_string,
                                            "question": question_id
                                        }
                                    }
                                    try:
                                        response = requests.post('https://api.yescaptcha.com/createTask', verify=False,
                                                                 json=data)
                                        recognize_result = response.json()
                                        print(f'识别结果:{recognize_result}')
                                    except requests.RequestException:
                                        logger.exception('error occurred while recognizing captcha', exc_info=True)

                                else:
                                    '''触发验证码'''
                                    await self.page.mouse.move(x=940, y=430)  # 鼠标移动到该位置
                                    await self.page.mouse.down()  # 鼠标点击
                                    await self.page.mouse.up()  # 鼠标放开操作
                                    await self.page.evaluate(
                                        "document.querySelectorAll('iframe')[0].contentDocument.querySelector('#recaptcha-anchor > div.recaptcha-checkbox-border').click()")
                                    time.sleep(2)
                                    continue

                                recognized_results = recognize_result.get('solution', {}).get('objects')
                                print(recognized_results)  # 对应的图片标号列表

                                i += 1
                                #  判断机制，验证次数超过15次重新触发验证码
                                if i > 6:
                                    break
                                    i = 0
                                    '''触发验证码'''
                                    print('''触发验证码''')
                                    # await page.mouse.move(x=940, y=430)  # 鼠标移动到该位置
                                    # await page.mouse.down()  # 鼠标点击
                                    # await page.mouse.up()  # 鼠标放开操作
                                    # await page.evaluate("document.querySelectorAll('iframe')[0].contentDocument.querySelector('#recaptcha-anchor > div.recaptcha-checkbox-border').click()")
                                    # await page.goBack()
                                    # time.sleep(3)
                                    time.sleep(2)
                                    await self.page.evaluate(
                                        "document.querySelectorAll('iframe')[2].contentDocument.querySelector('#recaptcha-reload-button').click()")
                                    continue
                                else:
                                    pass

                                if location == recognized_results:
                                    await self.page.evaluate(
                                        "document.querySelectorAll('iframe')[2].contentDocument.querySelector('#recaptcha-reload-button').click()")
                                    continue
                                else:
                                    location = recognized_results

                                if recognized_results is None:
                                    await self.page.evaluate(
                                        "document.querySelectorAll('iframe')[2].contentDocument.querySelector('#recaptcha-verify-button').click()")
                                    await self.page.evaluate(
                                        "document.querySelectorAll('iframe')[2].contentDocument.querySelector('#recaptcha-verify-button').click()")
                                    await self.page.evaluate(
                                        "document.querySelectorAll('iframe')[2].contentDocument.querySelector('#recaptcha-verify-button').click()")
                                    time.sleep(3)
                                    continue
                                else:
                                    pass

                                '''模拟点击'''
                                for index in recognized_results:
                                    await self.page.evaluate(
                                        f"document.querySelectorAll('iframe')[2].contentDocument.querySelectorAll('#rc-imageselect-target td')[{index}].click()")

                                '''点击验证'''
                                await self.page.evaluate(
                                    "document.querySelectorAll('iframe')[2].contentDocument.querySelector('#recaptcha-verify-button').click()")
                                time.sleep(3)

                                '''验证验证是否成功'''
                                try:
                                    checked = await self.page.evaluate('''() => {let check = document.querySelectorAll('iframe')[0].contentDocument.querySelector('#recaptcha-anchor').getAttribute('aria-checked');
                                                                                             return check;}''')
                                    # print(checked)
                                    if checked == 'true':
                                        print('验证成功')
                                        break
                                    else:
                                        time.sleep(2)
                                        pass
                                except Exception as e:
                                    print(e)
                                    pass
                            except Exception as e:
                                print(e)
                                pass
                    else:

                        await self.page.keyboard.press('End')
                        await asyncio.sleep(2)
                        await self.page.click('#pnnext')
                        self.mysignal.emit(['Next...'], 'label')
                        inum = inum + 1
                        sj = int(main.sj)
                        esj = int(sj + 10)
                        time.sleep(random.choice(range(sj, esj)))

                except Exception as e:
                    self.mysignal.emit(['ADNORMAL...'], 'label')
                    print(e)
                    inum = inum + 10
                    # await self.page.screenshot({'path': 'google2.png'})
                    await asyncio.sleep(2)

                    pass


class whats(QThread):
    mysignal = pyqtSignal(int, int, str, str)

    def __int__(self):
        super(whats, self).__init__()

    def stop(self):
        # self.terminate()

        asyncio.new_event_loop().run_until_complete(self.guan())

        # self.terminate()

    async def guan(self):
        # await self.page.evaluate("window.stop()")
        await self.browser.close()

    async def main_whats(self):

        pkl_file = open('file_WS.pkl', 'rb')
        list_file = pickle.load(pkl_file)
        print(list_file)
        list_file1 = copy.deepcopy(list_file)
        pkl_file.close()
        if list_file:
            # 清空表内容
            main.tableWidget.clearContents()
            main.tableWidget.setRowCount(17)
            # 设置表行数
            if len(list_file) % 2 == 0:
                row = int(len(list_file) / 2)
                main.tableWidget.setRowCount(row)
            else:
                row = int(len(list_file) / 2 + 1)
                main.tableWidget.setRowCount(row)
            if '--enable-automation' in launcher.DEFAULT_ARGS:
                launcher.DEFAULT_ARGS.remove("--enable-automation")
            self.browser = await launch(headless=main.headless, dumpio=True, autoClose=False,
                                        handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False,
                                        args=['--no-sandbox', '--window-size=1920,1080', '--disable-infobars',
                                              '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'])  # 进入有头模式

            page = await self.browser.newPage()
            # 设置页面视图大小
            await page.setViewport({'width': 1920, 'height': 1080})
            # 是否启用JS，enabled设为False，则无渲染效果
            await page.setJavaScriptEnabled(enabled=True)
            # self.mysignal.emit('开始获取')

            url = 'https://web.whatsapp.com/'

            await page.goto(url)
            await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')

            await asyncio.sleep(3)
            time_1 = 0
            C = 0
            opened = 0
            try:
                for i in list_file:
                    num_url = "https://web.whatsapp.com/send?phone=" + i
                    await page.goto(num_url)
                    await asyncio.sleep(10)
                    while True:
                        ready = await page.evaluate("document.readyState")
                        await asyncio.sleep(5)
                        if ready == "complete":
                            break
                    header = await page.xpath(r'/html/body/div[1]/div/div/div[4]/div/header')
                    print(header)
                    if header:
                        yn = '是'
                        print(i)
                        a_txt = open(r'./WS_已开通.txt', 'a')
                        a_txt.write(i + '\n')
                        a_txt.close()
                        opened += 1
                        main.label_29.setText(str(opened) + '个')
                        del header
                    else:
                        yn = '否'
                    for j in range(2):
                        if j % 2 != 0:
                            if time_1 % 2 != 0:
                                j += 2
                            self.mysignal.emit(C, j, yn,'table')
                            time.sleep(0.001)
                        else:
                            if time_1 % 2 != 0:
                                j += 2
                            self.mysignal.emit(C, j, str(i),'table')
                            time.sleep(0.001)
                        if j == 3:
                            C += 1
                    time_1 += 1
                    list_file1.remove(i)
                    file_WS = open('file_WS.pkl', 'wb')
                    pickle.dump(list_file1, file_WS)
            except:
                pass

    def run(self):
        loop1 = asyncio.new_event_loop()
        loop1.run_until_complete(self.main_whats())


class mymainwindow(QMainWindow, pyui.Ui_MainWindow):
    def __init__(self):
        self.headless = False   # 设置无头模式
        self.list_url_xiaozu = []
        self.unEnabled_button_1 = None
        self.unEnabled_button_2 = None
        self.list_num = []
        self.list_liebian = []
        self.dic_translated = {}
        self.dit_words = {}
        self.gg_gjc = []
        self.gg_dq = []
        self.list_href_dq = []
        self.ins_listPage = []
        self.url_tw = ''
        self.url_lb = ''
        self.ZBURL = []
        super(mymainwindow, self).__init__()
        self.setupUi(self)

        # 主页面
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框
        self.pushButton_23.clicked.connect(self.on_pushButton_23_click)
        self.pushButton_24.clicked.connect(self.on_pushButton_24_click)
        self.pushButton_25.clicked.connect(self.on_pushButton_25_click)

        self.pushButton_20.clicked.connect(self.ceshi)
        self.pushButton_21.clicked.connect(self.stop1)
        # self.pushButton_22.clicked.connect(self.daochu1)

        # 公开小组挖掘
        self.pushButton_56.clicked.connect(self.open_group)
        self.pushButton_57.clicked.connect(self.stop_57)
        self.spinBox.setAlignment(Qt.AlignHCenter)

        # 谷歌地图获客
        self.pushButton_216.clicked.connect(self.lbs)
        self.pushButton_217.clicked.connect(self.stop_217)
        # self.tableWidget_3.horizontalHeader().setVisible(True)
        self.spinBox_7.setAlignment(Qt.AlignHCenter)

        # 小组成员
        self.pushButton_232.clicked.connect(self.import_232)
        self.pushButton_234.clicked.connect(self.group_number)
        self.pushButton_235.clicked.connect(self.stop235)

        # FB主页基础
        self.pushButton_84.clicked.connect(self.fb_mainPage)
        self.pushButton_85.clicked.connect(self.stop_85)

        # FB小组基础
        self.pushButton_204.clicked.connect(self.fb_mainGroup)
        self.pushButton_205.clicked.connect(self.stop_205)

        # FB直播
        self.pushButton_228.clicked.connect(self.fb_mainLives)
        self.pushButton_229.clicked.connect(self.stop_229)

        # FB主页
        self.pushButton_95.clicked.connect(self.daoru23)
        self.pushButton_96.clicked.connect(self.qidong23)
        self.pushButton_101.clicked.connect(self.qp23)
        self.pushButton_99.clicked.connect(self.stop23)

        # ins
        self.pushButton_137.clicked.connect(self.daoru137)
        self.pushButton_139.clicked.connect(self.insfs)  # 启动
        self.pushButton_140.clicked.connect(self.insdl)  # 登录
        self.pushButton_138.clicked.connect(self.instart)  # 查询
        self.pushButton_141.clicked.connect(self.insstop)  # 停止
        # self.pushButton_142.clicked.connect(self.insdc)  # 导出
        self.pushButton_143.clicked.connect(self.insqp)  # 清空

        # 小组
        self.pushButton_72.clicked.connect(self.daoru21)  # 导入
        self.pushButton_71.clicked.connect(self.huoqu21)  # 获取
        self.pushButton_13.clicked.connect(self.qidong21)  # 启动
        self.pushButton_14.clicked.connect(self.stop21)  # 登录
        self.pushButton_15.clicked.connect(self.qingchu21)  # 停止
        # self.pushButton_12.clicked.connect(self.daochu21)  # 导出
        self.pushButton_16.clicked.connect(self.ceshi21)  # 测试

        # 直播

        self.pushButton_88.clicked.connect(self.daoru22)  # 导入
        self.pushButton_89.clicked.connect(self.qidong22)  # 获取
        # self.pushButton_90.clicked.connect(self.qidong22)#启动
        # self.pushButton_91.clicked.connect(self.stop22)#登录
        self.pushButton_92.clicked.connect(self.qingchu22)  # 停止
        # self.pushButton_93.clicked.connect(self.daochu22)  # 导出
        self.pushButton_94.clicked.connect(self.qp22)

        # F粉丝
        self.pushButton_102.clicked.connect(self.daoru_102)
        self.pushButton_103.clicked.connect(self.facebook_Ffs)
        self.pushButton_106.clicked.connect(self.stop106)
        self.pushButton_108.clicked.connect(self.qp_108)

        # F地区
        self.pushButton_117.clicked.connect(self.facebook_diqu)
        self.pushButton_120.clicked.connect(self.stop120)
        self.pushButton_122.clicked.connect(self.qp_122)
        self.pushButton_153.clicked.connect(self.daoruList_153)

        # INS贴文
        self.pushButton_130.clicked.connect(self.daoru_130)
        self.pushButton_131.clicked.connect(self.IG_tiewen)
        self.pushButton_134.clicked.connect(self.stop134)
        self.pushButton_136.clicked.connect(self.qp_136)

        # INS标签
        self.pushButton_154.clicked.connect(self.daoru_154)
        self.pushButton_155.clicked.connect(self.IG_label)
        self.pushButton_158.clicked.connect(self.stop158)
        self.pushButton_160.clicked.connect(self.qp_160)

        # INS主页
        self.pushButton_144.clicked.connect(self.daoruList_144)
        self.pushButton_145.clicked.connect(self.ins_homePage)
        self.pushButton_148.clicked.connect(self.stop148)
        self.pushButton_150.clicked.connect(self.qp_150)

        # INS搜索
        self.pushButton_124.clicked.connect(self.ins_Search)
        self.pushButton_127.clicked.connect(self.stop127)
        self.pushButton_129.clicked.connect(self.qp_129)

        # 全球获客
        self.pushButton.clicked.connect(lambda: self.change(0, self.pushButton))
        self.pushButton_2.clicked.connect(lambda: self.change(1, self.pushButton_2))
        self.pushButton_3.clicked.connect(lambda: self.change(2, self.pushButton_3))
        self.pushButton_4.clicked.connect(lambda: self.change(3, self.pushButton_4))
        self.pushButton_6.clicked.connect(lambda: self.change(4, self.pushButton_6))
        self.pushButton_8.clicked.connect(lambda: self.change(5, self.pushButton_8))
        self.pushButton_9.clicked.connect(lambda: self.change(6, self.pushButton_9))

        self.pushButton_74.clicked.connect(lambda: self.change2(0, self.pushButton_74))
        self.pushButton_11.clicked.connect(lambda: self.change2(1, self.pushButton_11))
        self.pushButton_73.clicked.connect(lambda: self.change2(2, self.pushButton_73))
        self.pushButton_75.clicked.connect(lambda: self.change2(3, self.pushButton_75))
        self.pushButton_76.clicked.connect(lambda: self.change2(4, self.pushButton_76))
        self.pushButton_80.clicked.connect(lambda: self.change2(5, self.pushButton_80))
        self.pushButton_77.clicked.connect(lambda: self.change2(6, self.pushButton_77))
        self.pushButton_79.clicked.connect(lambda: self.change2(7, self.pushButton_79))
        self.pushButton_78.clicked.connect(lambda: self.change2(8, self.pushButton_78))
        self.pushButton_87.clicked.connect(lambda: self.change2(9, self.pushButton_87))
        self.button_color()

        # 万词生成
        self.childwindow_trans = None
        self.comboBox.setCurrentIndex(1)
        self.comboBox_2.setCurrentIndex(2)
        self.comboBox_3.setCurrentIndex(3)
        self.comboBox_4.setCurrentIndex(4)
        self.comboBox_6.setCurrentIndex(1)
        self.pushButton_237.clicked.connect(self.translate)
        self.pushButton_151.clicked.connect(self.make_words)
        self.pushButton_34.clicked.connect(self.on_clicked_btn_34)
        self.pushButton_152.clicked.connect(self.clear_wanci)

        # 追客获客
        self.pushButton_32.clicked.connect(self.import_num)
        self.pushButton_33.clicked.connect(self.make_num)
        self.pushButton_28.clicked.connect(self.mix_num)
        self.pushButton_27.clicked.connect(self.outPut_excel)
        self.pushButton_30.clicked.connect(self.clear_Nums)

        # WS获客
        self.tableWidget.setRowCount(17)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.pushButton_49.clicked.connect(self.stop_WS)
        self.pushButton_45.clicked.connect(self.import_WS)
        self.pushButton_46.clicked.connect(self.check_open)
        self.pushButton_50.clicked.connect(self.outPut_WS)
        self.pushButton_51.clicked.connect(self.login_WS)
        self.pushButton_5.clicked.connect(self.open_ws)

        # WS推送
        self.tableWidget_15.setRowCount(17)
        self.tableWidget_15.horizontalHeader().setVisible(True)
        self.tableWidget_15.setAlternatingRowColors(True)
        self.tableWidget_15.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.pushButton_61.clicked.connect(self.test_send)
        self.pushButton_62.clicked.connect(self.import_user_ws_tuisong)
        self.pushButton_63.clicked.connect(self.start_tuisong)
        self.pushButton_65.clicked.connect(self.stop_tuisong)

        # 云邮获客
        self.tableWidget_2.setRowCount(17)
        self.tableWidget_2.horizontalHeader().setVisible(True)
        self.tableWidget_2.setAlternatingRowColors(True)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.pushButton_52.clicked.connect(self.em_send)
        self.pushButton_47.clicked.connect(self.import_user_email_qunfa)
        self.pushButton_48.clicked.connect(self.start_qunfa)
        self.pushButton_60.clicked.connect(self.stop_qunfa)

        self.change_alltable()
        self.ws_rewrite()
        self.email_rewrite()
        self.center()

    def change_alltable(self):
        list_table = self.tabWidget.findChildren(QtWidgets.QTableWidget)
        for i in list_table:
            w = 1400
            c = i.columnCount()
            i.horizontalHeader().setVisible(True)
            i.setAlternatingRowColors(True)
            if c>1:
                i.setColumnWidth(0, 100)
                for j in range(1,c-1):
                    i.setColumnWidth(j,int((w-100)/c-1)+50)
            


    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    def on_pushButton_23_click(self):
        self.showMinimized()

    def on_pushButton_24_click(self):
        # print('24')
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def on_pushButton_25_click(self):
        que_box = QMessageBox.question(self, '退出', '你确定要退出吗？', QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.No)
        if que_box == QMessageBox.Yes:
            self.close_childWindow()
            self.close()

    def close_childWindow(self):
        qh.close()
        dq6.close()
        pt.close()
        gjc.close()
        gjc_215.close()

        dc.close()
        dc_218.close()
        dc_12.close()
        dc_93.close()
        dc_142.close()
        dc_100.close()
        dc_107.close()
        dc_121.close()
        dc_135.close()
        dc_159.close()

        list1 = psutil.pids()
        for i in list1:
            p = psutil.Process(i)
            if p.name() == "chrome.exe":
                p.terminate()

    def mousePressEvent(self, event):  # 鼠标左键按下时获取鼠标坐标,按下右键取消
        if event.button() == Qt.LeftButton:

            self.m_Position = event.globalPos() - self.pos()
            if self.m_Position.y() < 31:
                self.m_flag = True
                event.accept()
        elif event.button() == Qt.RightButton:
            self.m_flag = False

    def mouseMoveEvent(self, QMouseEvent):  # 鼠标在按下左键的情况下移动时,根据坐标移动界面
        try:
            if Qt.LeftButton and self.m_flag:
                self.move(QMouseEvent.globalPos() - self.m_Position)
                QMouseEvent.accept()
        except:
            pass

    def mouseReleaseEvent(self, QMouseEvent):  # 鼠标按键释放时,取消移动
        self.m_flag = False

    def change2(self, n, btn):
        icon_1 = QIcon(r'images/instagram-fill-round1.png')
        icon_2 = QIcon(r'images/instagram-fill-round.png')
        icon_3 = QIcon(r'images/F.png')
        icon_4 = QIcon(r'images/F(1).png')
        if self.unEnabled_button_2 in [self.pushButton_80, self.pushButton_77, self.pushButton_79, self.pushButton_78,
                                       self.pushButton_87]:
            self.unEnabled_button_2.setChecked(False)
            self.unEnabled_button_2.setIcon(icon_1)
            if btn in [self.pushButton_80, self.pushButton_77, self.pushButton_79, self.pushButton_78,
                       self.pushButton_87]:
                self.unEnabled_button_2 = btn
                self.unEnabled_button_2.setChecked(True)
                self.unEnabled_button_2.setIcon(icon_2)
            else:
                self.unEnabled_button_2 = btn
                self.unEnabled_button_2.setChecked(True)
                self.unEnabled_button_2.setIcon(icon_4)
        else:
            self.unEnabled_button_2.setChecked(False)
            self.unEnabled_button_2.setIcon(icon_3)
            if btn in [self.pushButton_80, self.pushButton_77, self.pushButton_79, self.pushButton_78,
                       self.pushButton_87]:
                self.unEnabled_button_2 = btn
                self.unEnabled_button_2.setChecked(True)
                self.unEnabled_button_2.setIcon(icon_2)
            else:
                self.unEnabled_button_2 = btn
                self.unEnabled_button_2.setChecked(True)
                self.unEnabled_button_2.setIcon(icon_4)
        self.stackedWidget_2.setCurrentIndex(n)

    def button_color(self):
        self.pushButton.setChecked(True)
        self.pushButton_74.setChecked(True)
        self.pushButton.setIcon(QIcon(r'images/diqiu(1).png'))
        self.pushButton_74.setIcon(QIcon(r'images/F(1).png'))
        self.unEnabled_button_1 = self.pushButton
        self.unEnabled_button_2 = self.pushButton_74



    def which_one(self,n):
        icon_1 = QIcon(r'images/instagram-fill-round1.png')
        icon_2 = QIcon(r'images/instagram-fill-round.png')
        icon_3 = QIcon(r'images/F.png')
        icon_4 = QIcon(r'images/F(1).png')
        icon_5 = QIcon(r'images/diqiu.png')
        icon_6 = QIcon(r'images/diqiu(1).png')
        icon_7 = QIcon(r'images/fuwudiqiu.png')
        icon_8 = QIcon(r'images/fuwudiqiu(1).png')
        icon_9 = QIcon(r'images/img.png')
        icon_10 = QIcon(r'images/img(1).png')
        if n == 0:
            self.unEnabled_button_1.setChecked(True)
            self.unEnabled_button_1.setIcon(icon_6)
        elif n == 1 or n == 6:
            self.unEnabled_button_1.setChecked(True)
            self.unEnabled_button_1.setIcon(icon_10)
        if n == 2 or n == 3 or n == 5:
            self.unEnabled_button_1.setChecked(True)
            self.unEnabled_button_1.setIcon(icon_4)
        if n == 4:
            self.unEnabled_button_1.setChecked(True)
            self.unEnabled_button_1.setIcon(icon_8)

    def change(self, n, btn):

        if self.unEnabled_button_1 == self.pushButton:
            self.unEnabled_button_1.setIcon(QIcon(r'images/diqiu.png'))
            self.unEnabled_button_1.setChecked(False)
            self.unEnabled_button_1 = btn
        elif self.unEnabled_button_1 == self.pushButton_4 or self.unEnabled_button_1 == self.pushButton_3 or self.unEnabled_button_1 == self.pushButton_8:
            self.unEnabled_button_1.setChecked(False)
            self.unEnabled_button_1.setIcon(QIcon(r'images/F.png'))
            self.unEnabled_button_1 = btn
        elif self.unEnabled_button_1 == self.pushButton_2 or self.unEnabled_button_1 == self.pushButton_9:
            self.unEnabled_button_1.setChecked(False)
            self.unEnabled_button_1.setIcon(QIcon(r'images/img.png'))
            self.unEnabled_button_1 = btn
        elif self.unEnabled_button_1 == self.pushButton_6:
            self.unEnabled_button_1.setChecked(False)
            self.unEnabled_button_1.setIcon(QIcon(r'images/fuwudiqiu.png'))
            self.unEnabled_button_1 = btn
        self.which_one(n)
        self.stackedWidget.setCurrentIndex(n)

    # 万词生成
    def get_textEdit(self):
        A_word = self.textEdit_9.toPlainText()
        B_word = self.textEdit_11.toPlainText()
        C_word = self.textEdit_10.toPlainText()
        D_word = self.textEdit_14.toPlainText()
        # A_word = self.textEdit_9.toPlainText().split('\n')
        # B_word = self.textEdit_11.toPlainText().split('\n')
        # C_word = self.textEdit_10.toPlainText().split('\n')
        # D_word = self.textEdit_14.toPlainText().split('\n')
        if A_word == ['']:
            A_word = []
        if B_word == ['']:
            B_word = []
        if C_word == ['']:
            C_word = []
        if D_word == ['']:
            D_word = []
        self.dit_words['list_1'] = A_word
        self.dit_words['list_2'] = B_word
        self.dit_words['list_3'] = C_word
        self.dit_words['list_4'] = D_word


    def translate(self):
        self.get_textEdit()
        translate_from = re.findall(r'\[(.*?)\]', self.comboBox_5.currentText())[0]
        translate_to = re.findall(r'\[(.*?)\]', self.comboBox_6.currentText())[0]
        print(self.dit_words, translate_from, translate_to)
        # dic_translated = yd.youdao_translate(self.dit_words, translate_from, translate_to)
        dic_translated = jinshan.js_translate(self.dit_words, translate_from, translate_to)

        print(dic_translated)
        self.textEdit_9.clear()
        self.textEdit_11.clear()
        self.textEdit_10.clear()
        self.textEdit_14.clear()
        part_A = '\n'.join(dic_translated["list_1"])
        part_B = '\n'.join(dic_translated["list_2"])
        part_C = '\n'.join(dic_translated["list_3"])
        part_D = '\n'.join(dic_translated["list_4"])
        self.textEdit_9.setText(part_A)
        self.textEdit_11.setText(part_B)
        self.textEdit_10.setText(part_C)
        self.textEdit_14.setText(part_D)
        self.dic_translated = dic_translated

    def make_words(self):
        list_words = []
        combo_1 = self.comboBox.currentIndex()
        combo_2 = self.comboBox_2.currentIndex()
        combo_3 = self.comboBox_3.currentIndex()
        combo_4 = self.comboBox_4.currentIndex()
        # try:

        self.get_textEdit()
        a, b, c, d = self.dit_words.values()
        if not a:
            a=['']
        else:
            a = a.split('\n')
            for i in range(len(a)):
                a[i] = ' '+a[i]
        if not b:
            b=['']
        else:
            b = b.split('\n')
            for i in range(len(b)):
                b[i] = ' '+b[i]
        if not c:
            c=['']
        else:
            c = c.split('\n')
            for i in range(len(c)):
                c[i] = ' '+c[i]
        if not d:
            d=['']
        else:
            d = d.split('\n')
            for i in range(len(d)):
                d[i] = ' '+d[i]
        print(a)
        print(b)
        print(c)
        print(d)
        lis_trans = [[''], a, b, c, d]
        word = ''
        lis = []
        combo_lis = [combo_1, combo_2, combo_3, combo_4]
        for combo in combo_lis:
            lis.append(lis_trans[combo])
        for word_A in lis[0]:
            word += word_A
            len_A = len(word)
            for word_B in lis[1]:
                word += word_B
                len_B = len(word)
                for word_C in lis[2]:
                    word += word_C
                    len_C = len(word)
                    for word_D in lis[3]:
                        word += word_D + '\n'
                        list_words.append(word.strip())
                        word = word[:len_C]
                    word = word[:len_B]
                word = word[:len_A]
            word = ''
        self.childwindow_trans = wancishengcheng.Ui_Form(list_words)
        self.childwindow_trans.show()
        # except Exception as e:
        #     print(e)

    def on_clicked_btn_34(self):
        index_1 = self.comboBox_5.currentIndex()
        index_2 = self.comboBox_6.currentIndex()
        self.comboBox_5.setCurrentIndex(index_2)
        self.comboBox_6.setCurrentIndex(index_1)

    def clear_wanci(self):
        self.textEdit_9.clear()
        self.textEdit_11.clear()
        self.textEdit_10.clear()
        self.textEdit_14.clear()

    # 公开小组挖掘
    def open_group(self):
        self.pushButton_56.setEnabled(False)
        time = self.spinBox_7.value()
        if os.path.exists('renwu2.pkl'):
            print(pt_54.ptt, gjc_55.gjcc, xz.li)
            self.GET_gp = get_group.google_group(time,self.headless)
            self.GET_gp.mysignal.connect(self.print17)
            self.print17(['START'])
            self.GET_gp.start()

    def print17(self, datalist, place='label'):
        if place == 'table':
            row_cnt = self.tableWidget_17.rowCount()
            self.tableWidget_17.insertRow(row_cnt)
            column_cnt = self.tableWidget_17.rowCount()
            self.tableWidget_17.setItem(column_cnt - 1, 0, QTableWidgetItem(str(column_cnt)))
            for i in range(len(datalist)):
                self.tableWidget_17.setItem(column_cnt - 1, i+1, QTableWidgetItem(str(datalist[i])))
            self.tableWidget_17.verticalScrollBar().setSliderPosition(column_cnt + 1)
        elif place == 'label':
            self.label_23.setText(datalist[0])


    def stop_57(self):
        try:
            self.pushButton_56.setEnabled(True)
            self.GET_gp.quit()
            self.GET_gp.stop()
            del self.GET_gp
        except:
            pass

    # 谷歌地图获客
    def lbs(self):
        if gjc_215.gjcc and self.gg_dq:
            self.pushButton_216.setEnabled(False)
            self.ggMap = gg_map.google_map(self.gg_dq, gjc_215.gjcc,self.headless)
            self.ggMap.mysignal.connect(self.print_map)
            self.ggMap.start()
            self.print_map(['START'])

    def stop_217(self):
        try:
            self.pushButton_216.setEnabled(True)
            self.ggMap.quit()
            self.ggMap.stop()
            del self.ggMap
        except:
            pass

    def print_map(self, datalist,place='label'):
        if place=='table':
            row_cnt = self.tableWidget_3.rowCount()
            self.tableWidget_3.insertRow(row_cnt)
            column_cnt = self.tableWidget_3.rowCount()
            self.tableWidget_3.setItem(column_cnt - 1, 0, QTableWidgetItem(str(column_cnt)))
            for i in range(len(datalist)):
                self.tableWidget_3.setItem(column_cnt - 1, i+1, QTableWidgetItem(str(datalist[i])))
            self.tableWidget_3.verticalScrollBar().setSliderPosition(column_cnt + 1)
        elif place == 'label':
            self.label_26.setText(datalist[0])

    # F粉丝
    def facebook_Ffs(self):
        if self.url_hy:
            self.pushButton_103.setEnabled(False)
            self.fb_Ffs = fb_friends.fb_fd(self.url_hy,self.headless)
            self.fb_Ffs.mysignal.connect(self.print5)
            self.print5(['START'])
            self.fb_Ffs.start()

    def daoru_102(self):
        self.url_hy = self.lineEdit_23.text()
        self.print5(["导入完成"])

    def stop106(self):
        try:
            self.pushButton_103.setEnabled(True)
            self.fb_Ffs.quit()
            self.fb_Ffs.stop()
            del self.fb_Ffs
        except:
            pass

    def qp_108(self):
        for rowNum in range(0, self.tableWidget_7.rowCount())[::-1]:  # 逆序删除，正序删除会有一些删除不成功
            self.tableWidget_7.removeRow(rowNum)

    # F地区
    def facebook_diqu(self):
        if self.list_href_dq == []:
            self.list_href_dq.append(self.lineEdit_25.text())
        if self.list_href_dq != []:
            self.pushButton_117.setEnabled(False)
            stop_time = self.spinBox_2.value()
            self.fb_dq = fb_diqu.fb_diqu_info(self.list_href_dq, stop_time, self.headless)
            self.fb_dq.mysignal.connect(self.print7)
            self.print7(['START'])
            self.fb_dq.start()

    def stop120(self):
        try:
            self.pushButton_117.setEnabled(True)
            self.fb_dq.quit()
            self.fb_dq.stop()
            del self.fb_dq
        except:
            pass

    def daoruList_153(self):
        filename = QFileDialog.getOpenFileName(self, '选择文件', os.getcwd(), "xlsx(*.xlsx);;文本文件(*txt)")[0]
        if "xlsx" in filename:
            try:
                df = pd.read_excel(r"{}".format(filename))
                self.list_href_dq = list(df['链接'].values)
                print(self.list_href_dq)
                self.print7(["导入完成"])
            except:
                pass
        elif '.txt' in filename:
            f1 = open(r"{}".format(filename), 'r')
            list_num = f1.readlines()
            f1.close()
            if list_num:
                df = pd.DataFrame({'链接': list_num})
                df['链接'] = df['链接'].str.replace('\n', '')
                self.list_href_dq = list(df['链接'].values)
                print(self.list_href_dq)
                self.print7(["导入完成"])

    def qp_122(self):
        for rowNum in range(0, self.tableWidget_9.rowCount())[::-1]:  # 逆序删除，正序删除会有一些删除不成功
            self.tableWidget_9.removeRow(rowNum)

    # INS贴文
    def IG_tiewen(self):
        if self.url_tw:
            self.pushButton_131.setEnabled(False)
            self.ins_tw = ins_tiewen.ins_like(self.url_tw,self.headless)
            self.ins_tw.mysignal.connect(self.print_tw)
            self.print_tw(['START'])
            self.ins_tw.start()
        else:
            self.print_tw(['请导入链接'])

    def daoru_130(self):
        self.url_tw = self.lineEdit_27.text()
        self.print_tw(["导入完成"])

    def stop134(self):
        try:
            self.pushButton_131.setEnabled(True)
            self.ins_tw.quit()
            self.ins_tw.stop()
            del self.ins_tw
        except:
            pass

    def qp_136(self):
        for rowNum in range(0, self.tableWidget_11.rowCount())[::-1]:  # 逆序删除，正序删除会有一些删除不成功
            self.tableWidget_11.removeRow(rowNum)

    # INS标签
    def IG_label(self):
        if self.url_lb:
            self.pushButton_155.setEnabled(False)
            self.ins_lb = ins_LB.ins_label(self.url_lb,self.headless)
            self.ins_lb.mysignal.connect(self.print_lb)
            self.print_lb(['START'])
            self.ins_lb.start()
        else:
            self.print_lb(['未导入链接'])

    def daoru_154(self):
        self.url_lb = self.lineEdit_30.text()
        self.print_lb(["导入完成"])

    def stop158(self):
        try:
            self.pushButton_155.setEnabled(True)
            self.ins_lb.quit()
            self.ins_lb.stop()
            del self.ins_lb
        except:
            pass

    def qp_160(self):
        for rowNum in range(0, self.tableWidget_14.rowCount())[::-1]:  # 逆序删除，正序删除会有一些删除不成功
            self.tableWidget_14.removeRow(rowNum)

    def print_lb(self, datalist, place='label'):
        if place == 'table':
            row_cnt = self.tableWidget_14.rowCount()
            self.tableWidget_14.insertRow(row_cnt)
            column_cnt = self.tableWidget_14.rowCount()
            self.tableWidget_14.setItem(column_cnt - 1, 0, QTableWidgetItem(str(column_cnt)))
            for i in range(len(datalist)):
                self.tableWidget_14.setItem(column_cnt - 1, i+1, QTableWidgetItem(str(datalist[i])))
            self.tableWidget_14.verticalScrollBar().setSliderPosition(column_cnt + 1)
        elif place=='label':
            self.label_22.setText(datalist[0])

    # 追客获客
    def import_num(self):
        filename = QFileDialog.getOpenFileName(self, '选择文件', os.getcwd(), "xlsx(*.xlsx);;文本文件(*txt)")[0]
        if '获客' in filename:
            res = []
            self.textEdit_12.clear()
            if ".xlsx" in filename:
                try:
                    df = pd.read_excel(r"{}".format(filename))
                    res = np.array(df['手机号'])
                except:
                    self.textEdit_12.setText(str('格式不符，请导入含有“手机号”表头的xlsx文件'))
        elif '.txt' in filename:
            f1 = open(r"{}".format(filename), 'r')
            list_num = f1.readlines()
            f1.close()
            if list_num:
                df = pd.DataFrame({'手机号': list_num})
                df['手机号'] = df['手机号'].str.replace('\n', '')
                res = np.array(df['手机号'])
        else:
            pass
        text = ''
        for i in res:
            text = text + f'{i}' + '\n'
        self.textEdit_12.setText(text)
        self.change_label()

    def make_num(self):
        self.list_num = []
        nums = self.textEdit_12.toPlainText()
        self.list_num = nums.split('\n')
        if self.list_num[-1] == '':
            self.list_num = self.list_num[:-1]
        print(nums,self.list_num)
        self.zhuike1 = zhuike()
        self.zhuike1.mysignal.connect(self.textBrowser_22.append)  # 自定义信号连接
        self.zhuike1.start()
        self.change_label()

    def mix_num(self):
        numbers = self.textBrowser_22.toPlainText().split('\n')
        self.textBrowser_22.clear()
        if numbers[-1] == '':
            numbers = numbers[:-1]
        if numbers:
            random.shuffle(numbers)
            nums = ''
            for i in numbers:
                nums = nums + i + '\n'
            self.textBrowser_22.setText(nums)

    # 导出总追客
    def outPut_excel(self):
        try:
            if self.list_liebian:
                dir_path = QFileDialog.getExistingDirectory(self, "请选择文件夹", "D:\\")
                print(dir_path)

                data = pd.DataFrame(data=self.list_liebian, columns=["手机号"])

                path = dir_path + '/' + '追客' + re.sub(r'[^0-9]', '',
                                                        datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + '.xlsx'
                with pd.ExcelWriter(path) as writer:
                    data.to_excel(writer, sheet_name='手机号')
                main.print1('The task is completed')
                main.print1(str(path))
        except:
            main.print9('Please re-enter')

    def clear_Nums(self):
        self.textBrowser_22.clear()
        self.list_liebian = []
        self.change_label()

    def change_label(self):
        if self.list_liebian:
            self.label_13.setText(str(len(self.list_liebian)) + '个')
        else:
            if self.list_num:
                self.label_13.setText(str(len(self.list_num)) + '个')

    def daochu21(self):
        dir_path = QFileDialog.getExistingDirectory(None, "请选择文件夹", "D:\\")
        print(dir_path)

        conn = sqlite3.connect('HKHMFB.db')
        cursor = conn.execute("SELECT * from STUD_FB")
        print("NAME\tCONTACT\t\tEMAIL\tTIME")
        bi = 1
        biao = pd.DataFrame(data=None, columns=["用户名", "小组ID", "链接", "时间"])
        for row in cursor:
            print([row[0], row[1], row[2], row[3]])
            biao.loc[bi] = [row[0], row[1], row[2], row[3]]
            bi = bi + 1
        conn.close()

        print(biao)
        path = dir_path + '/' + '小组' + re.sub(r'[^0-9]', '',
                                                datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + '.xlsx'

        with pd.ExcelWriter(path) as writer:
            biao.to_excel(writer, sheet_name='小组ID')
        self.print21([path])

    def daochu22(self):
        dir_path = QFileDialog.getExistingDirectory(None, "请选择文件夹", "D:\\")
        print(dir_path)

        conn = sqlite3.connect('HKHMZB.db')
        cursor = conn.execute("SELECT * from STUD_ZB")
        # print("NAME\tCONTACT\t\tEMAIL\tTIME")
        bi = 1
        biao = pd.DataFrame(data=None, columns=["用户名", "ID", "链接", "时间"])
        for row in cursor:
            # print ("{}\t{}\t{}\t{}".format(row[0],row[1],row[2],row[3]))
            biao.loc[bi] = [row[0], row[1], row[2], row[3]]
            bi = bi + 1
        conn.close()

        print('biao')
        path = dir_path + '/' + '直播' + re.sub(r'[^0-9]', '',
                                                datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + '.xlsx'

        with pd.ExcelWriter(path) as writer:
            biao.to_excel(writer, sheet_name='直播ID')

        self.print22([path])

    def print21(self, datalist, place='label'):
        if place=='table':
            row_cnt = self.tableWidget_4.rowCount()
            self.tableWidget_4.insertRow(row_cnt)
            column_cnt = self.tableWidget_4.rowCount()
            self.tableWidget_4.setItem(column_cnt - 1, 0, QTableWidgetItem(str(column_cnt)))
            for i in range(len(datalist)):
                self.tableWidget_4.setItem(column_cnt - 1, i+1, QTableWidgetItem(str(datalist[i])))
            self.tableWidget_4.verticalScrollBar().setSliderPosition(column_cnt + 1)
        elif place=='label':
            self.label_46.setText(datalist[0])
    def print22(self, datalist, place='label'):
        if place == 'table':
            row_cnt = self.tableWidget_5.rowCount()
            self.tableWidget_5.insertRow(row_cnt)
            column_cnt = self.tableWidget_5.rowCount()
            self.tableWidget_5.setItem(column_cnt - 1, 0, QTableWidgetItem(str(column_cnt)))
            for i in range(len(datalist)):
                self.tableWidget_5.setItem(column_cnt - 1, i+1, QTableWidgetItem(str(datalist[i])))
            self.tableWidget_5.verticalScrollBar().setSliderPosition(column_cnt + 1)
        elif place == 'label':
            self.label_47.setText(datalist[0])
    def ceshi21(self):
        self.qp21()

    def ceshi22(self):
        self.qp22()

    def huoqu21(self):
        try:
            if self.LJURL != []:
                self.pushButton_89.setEnabled(False)
                self.my_fb = facebook(self.headless)  # 步骤2. 主线程连接子线
                self.my_fb.mysignal.connect(self.print21)  # 自定义信号连接
                self.print21(['START'])
                self.my_fb.start()
            else:
                print('无链接')
                self.print21(['无链接'])
        except:
            self.print21(['无链接'])
            pass

    def huoqu22(self):
        try:
            self.my_zb.start()
        except:
            pass

    def stop21(self):
        try:
            self.pushButton_13.setEnabled(True)
            self.my_fbid.quit()
            self.my_fbid.stop()
            del self.my_fbid
        except:
            pass

    def stop22(self):
        try:
            self.pushButton_89.setEnabled(True)
            self.my_zb.quit()
            self.my_zb.stop()
            del self.my_zb
        except:
            pass

    def stop23(self):
        try:
            self.pushButton_96.setEnabled(True)
            self.my_fbzy.quit()
            self.my_fbzy.stop()
            del self.my_fbzy
        except:
            pass

    def qidong21(self):

        # self.print21('任务开始')
        self.pushButton_13.setEnabled(False)
        self.my_fbid = fbid()  # 步骤2. 主线程连接子线
        self.my_fbid.mysignal.connect(self.print21)  # 自定义信号连接
        self.print21(['LOGIN'])
        self.my_fbid.start()  # 步骤3 子线程开始执行run函数

    def qidong22(self):

        if self.ZBURL != []:
            self.pushButton_89.setEnabled(False)
            self.print22(['任务开始'])
            self.my_zb = zhibo(self.headless)  # 步骤2. 主线程连接子线
            self.my_zb.mysignal.connect(self.print22)  # 自定义信号连接
            self.print22(['START'])
            self.my_zb.start()  # 步骤3 子线程开始执行run函数
        else:
            self.print22(['请输入链接'])
            print('请输入链接')

    def qidong23(self):

        # self.print21('任务开始')
        self.pushButton_96.setEnabled(False)
        self.my_fbzy = fbzhuye(self.headless)  # 步骤2. 主线程连接子线
        self.my_fbzy.mysignal.connect(self.print23)  # 自定义信号连接
        self.print23(['START'])
        self.my_fbzy.start()  # 步骤3 子线程开始执行run函数

    def qp21(self):
        for rowNum in range(0, self.tableWidget_4.rowCount())[::-1]:  # 逆序删除，正序删除会有一些删除不成功
            self.tableWidget_4.removeRow(rowNum)

    def qp22(self):
        for rowNum in range(0, self.tableWidget_5.rowCount())[::-1]:  # 逆序删除，正序删除会有一些删除不成功
            self.tableWidget_5.removeRow(rowNum)

    def qp23(self):
        for rowNum in range(0, self.tableWidget_6.rowCount())[::-1]:  # 逆序删除，正序删除会有一些删除不成功
            self.tableWidget_6.removeRow(rowNum)

    def qingchu21(self):
        try:
            # self.textBrowser.clear()
            self.pushButton_72.setEnabled(True)
            self.my_fb.stop()
        except:
            pass

    def qingchu22(self):
        # self.textBrowser_3.clear()
        try:
            self.pushButton_89.setEnabled(True)
            self.my_zb.stop()
        except:
            pass

    def daoru21(self):

        self.LJURL = []
        ljtext = self.lineEdit_19.text()

        if ljtext != '':
            # print(QH)
            # print(GJC)
            print(ljtext)
            self.print21([ljtext])
            self.LJURL.append(ljtext)


        else:
            self.print21(['清输入链接'])
            print('清输入链接')

    def daoru22(self):

        self.ZBURL = []
        zbtext = self.lineEdit_21.text()

        if zbtext != '':
            # print(QH)
            # print(GJC)
            print(zbtext)
            self.print22([zbtext])
            self.ZBURL.append(zbtext)


        else:
            self.print22(['清输入链接'])
            print('清输入链接')

    def daoru23(self):

        self.ZYURL = []
        zytext = self.lineEdit_22.text()

        if zytext != '':
            # print(QH)
            # print(GJC)
            print(zytext)
            self.print23([zytext])
            self.ZYURL.append(zytext)
        else:
            self.print23(['清输入链接'])
            print('清输入链接')

    def insqp(self):
        self.tableWidget_12.clear()

    def insdc(self):
        try:
            dir_path = QFileDialog.getExistingDirectory(None, "请选择文件夹", "D:\\")
            print(dir_path)

            conn = sqlite3.connect('HKHMINS.db')
            cursor = conn.execute("SELECT * from STUD_INS")
            print("NAME\tCONTACT\t\tEMAIL\tTIME")
            bi = 1
            biao = pd.DataFrame(data=None, columns=["用户名", "ID", "链接", "时间"])
            for row in cursor:
                # print ("{}\t{}\t{}\t{}".format(row[0],row[1],row[2],row[3]))
                biao.loc[bi] = [row[0], row[1], row[2], row[3]]
                bi = bi + 1
            conn.close()

            # print(biao)
            path = dir_path + '/' + 'INS粉丝' + re.sub(r'[^0-9]', '',
                                                       datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + '.xlsx'

            with pd.ExcelWriter(path) as writer:
                biao.to_excel(writer, sheet_name='INS粉丝')
            self.print9(['导出成功'])
        except:
            self.print9(['重新输入'])
            pass

    def insstop(self):
        try:
            self.pushButton_138.setEnabled(True)
            self.my_ins.stop()
        except:
            pass

    def daoru137(self):
        self.insurl = self.lineEdit_28.text()
        if self.insurl:
            self.print9(['导入成功'])

    def instart(self):

        try:
            if self.insurl:
                self.pushButton_138.setEnabled(False)
                self.my_ins = ins(self.headless)
                self.my_ins.mysignal.connect(self.print9)
                self.print9(['START'])
                self.my_ins.start()

        except:
            self.print9(['请导入链接'])

    def insfs(self):
        # self.my_ins = ins()
        # self.my_ins.mysignal.connect(self.print9)
        self.pushButton_139.setEnabled(False)
        self.my_insid = insid()
        self.my_insid.mysignal.connect(self.print9)
        self.print9(['LOGIN'])

        self.my_insid.start()

    def insdl(self):
        # self.my_ins = ins()
        # self.my_ins.mysignal.connect(self.print9)

        try:
            self.pushButton_139.setEnabled(True)
            self.my_insid.stop()
        except:
            pass

    def daochu1(self):
        try:
            dir_path = QFileDialog.getExistingDirectory(None, "请选择文件夹", "D:\\")
            print(dir_path)

            conn = sqlite3.connect('HKHM.db')
            cursor = conn.execute("SELECT * from STUD_GJC")
            print("NAME\tCONTACT\t\tEMAIL")
            bi = 1
            biao = pd.DataFrame(data=None, columns=["关键词", "号码", "时间"])
            for row in cursor:
                # print ("{}\t{}\t{}".format(row[0],row[1],row[2]))
                biao.loc[bi] = [row[0], row[1], row[2]]
                bi = bi + 1
            conn.close()
            print(biao)
            path = dir_path + '/' + '获客' + re.sub(r'[^0-9]', '',
                                                    datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + '.xlsx'
            with pd.ExcelWriter(path) as writer:
                biao.to_excel(writer, sheet_name='号码')
            self.print1(['The task is completed'])
        except:
            self.print1(['Please re-enter'])
            pass
    def ceshi(self):
        self.pushButton_20.setEnabled(False)
        self.sj = self.spinBox.text()
        # print(int(self.sj)+10)
        self.my_go = google(self.headless)  # 步骤2. 主线程连接子线
        self.my_go.mysignal.connect(self.print1)  # 自定义信号连接
        self.print1(['START'])
        self.my_go.start()
    def stop1(self):
        try:
            self.pushButton_20.setEnabled(True)
            self.my_go.quit()
            self.my_go.stop()
            del self.my_go
        except:
            pass

    def print23(self, datalist, place='label'):
        if place=='table':
            row_cnt = self.tableWidget_6.rowCount()
            self.tableWidget_6.insertRow(row_cnt)
            column_cnt = self.tableWidget_6.rowCount()
            self.tableWidget_6.setItem(column_cnt - 1, 0, QTableWidgetItem(str(column_cnt)))
            for i in range(len(datalist)):
                self.tableWidget_6.setItem(column_cnt - 1, i+1, QTableWidgetItem(str(datalist[i])))
            self.tableWidget_6.verticalScrollBar().setSliderPosition(column_cnt + 1)
        elif place=='label':
            self.label_48.setText(datalist[0])
    def print1(self, datalist, place='label'):
        if place == 'table':
            row_cnt = self.tableWidget_16.rowCount()
            self.tableWidget_16.insertRow(row_cnt)
            column_cnt = self.tableWidget_16.rowCount()
            self.tableWidget_16.setItem(column_cnt - 1, 0, QTableWidgetItem(str(column_cnt)))
            for i in range(len(datalist)):
                self.tableWidget_16.setItem(column_cnt - 1, i+1, QTableWidgetItem(str(datalist[i])))
            self.tableWidget_16.verticalScrollBar().setSliderPosition(column_cnt + 1)
        elif place=='label':
            self.label_45.setText(datalist[0])

    def print9(self, datalist, place='label'):
        if place == 'table':
            row_cnt = self.tableWidget_12.rowCount()
            self.tableWidget_12.insertRow(row_cnt)
            column_cnt = self.tableWidget_12.rowCount()
            self.tableWidget_12.setItem(column_cnt - 1, 0, QTableWidgetItem(str(column_cnt)))
            for i in range(len(datalist)):
                self.tableWidget_12.setItem(column_cnt - 1, i+1, QTableWidgetItem(str(datalist[i])))
            self.tableWidget_12.verticalScrollBar().setSliderPosition(column_cnt + 1)
        elif place=='label':
            self.label_54.setText(datalist[0])
    def print5(self, datalist, place='label'):
        if place == 'table':
            row_cnt = self.tableWidget_7.rowCount()
            self.tableWidget_7.insertRow(row_cnt)
            column_cnt = self.tableWidget_7.rowCount()
            self.tableWidget_7.setItem(column_cnt - 1, 0, QTableWidgetItem(str(column_cnt)))
            for i in range(len(datalist)):
                self.tableWidget_7.setItem(column_cnt - 1, i+1, QTableWidgetItem(str(datalist[i])))
            self.tableWidget_7.verticalScrollBar().setSliderPosition(column_cnt + 1)
        elif place=='label':
            self.label_49.setText(datalist[0])

    def print7(self, datalist, place='label'):
        if place == 'table':
            row_cnt = self.tableWidget_9.rowCount()
            self.tableWidget_9.insertRow(row_cnt)
            column_cnt = self.tableWidget_9.rowCount()
            self.tableWidget_9.setItem(column_cnt - 1, 0, QTableWidgetItem(str(column_cnt)))
            for i in range(len(datalist)):
                self.tableWidget_9.setItem(column_cnt - 1, i+1, QTableWidgetItem(str(datalist[i])))
            self.tableWidget_9.verticalScrollBar().setSliderPosition(column_cnt + 1)
        elif place=='label':
            self.label_49.setText(datalist[0])

    def print_tw(self, datalist, place='label'):
        if place == 'table':
            row_cnt = self.tableWidget_11.rowCount()
            self.tableWidget_11.insertRow(row_cnt)
            column_cnt = self.tableWidget_11.rowCount()
            self.tableWidget_11.setItem(column_cnt - 1, 0, QTableWidgetItem(str(column_cnt)))
            for i in range(len(datalist)):
                self.tableWidget_11.setItem(column_cnt - 1, i+1, QTableWidgetItem(str(datalist[i])))
            self.tableWidget_11.verticalScrollBar().setSliderPosition(column_cnt + 1)
        elif place=='label':
            self.label_53.setText(datalist[0])

    # WS获客
    def import_WS(self):
        open('WS_已开通.txt', 'w').close()
        filename = QFileDialog.getOpenFileName(self, '选择文件', os.getcwd(), "xlsx(*.xlsx);;文本文件(*txt)")[0]
        res = []
        self.textEdit_5.clear()
        if "xlsx" in filename:
            try:
                df = pd.read_excel(r"{}".format(filename))
                res = np.array(df['手机号'])
            except:
                self.textEdit_5.setText(str('格式不符，请导入含有“手机号”表头的xlsx文件'))
        elif '.txt' in filename:
            f1 = open(r"{}".format(filename), 'r')
            list_num = f1.readlines()
            f1.close()
            if list_num:
                df = pd.DataFrame({'手机号': list_num})
                df['手机号'] = df['手机号'].str.replace('\n', '')
                res = np.array(df['手机号'])
        else:
            pass
        text = ''
        for i in res:
            text = text + f'{i}' + '\n'
        self.textEdit_5.setText(text)
        self.label_30.setText(str(len(res)) + '个')

        # else:
        #     pass
        # text = ''
        # self.list_num_WS = []
        # for i in res:
        #     text = text + f'目标号码：{i[0]}' + '\n'
        #     self.list_num_WS.append(i[0])
        # file_WS = open('file_WS.pkl', 'wb')
        # pickle.dump(self.list_num_WS, file_WS)
        # self.textEdit_5.setText(text)
        # self.label_30.setText(str(len(res)) + '个')

    def check_open(self):
        self.list_num_WS = []
        nums = self.textEdit_5.toPlainText()
        self.list_num_WS = nums.split('\n')
        if self.list_num_WS[-1] == '':
            self.list_num_WS = self.list_num_WS[:-1]
        file_WS = open('file_WS.pkl', 'wb')
        pickle.dump(self.list_num_WS, file_WS)
        self.whats_1 = whats()
        self.whats_1.mysignal.connect(self.input_item)
        self.whats_1.start()

    def input_item(self, c, j, yn):
        qt = QTableWidgetItem(yn)
        self.tableWidget.setItem(c, j, qt)

    def outPut_WS(self):
        try:
            dir_path = QFileDialog.getExistingDirectory(self, "请选择文件夹", "D:\\")
            print(dir_path)

            path = dir_path + '/' + 'WS_已开通' + re.sub(r'[^0-9]', '',
                                                         datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + '.xlsx'
            with open('WS_已开通.txt', 'r') as opened:
                list_num = opened.readlines()
            opened.close()
            df = pd.DataFrame({'手机号': list_num})
            df['手机号'] = df['手机号'].str.replace('\r\n', '')
            df.to_excel(path)
            open('WS_已开通.txt', 'w').close()
        except:
            pass

    def stop_WS(self):
        try:
            self.whats_1.quit()
            self.whats_1.stop()
            del self.whats_1
        except:
            pass

    def open_ws(self):
        try:
            self.browser_ws = WS_login.login()
            self.browser_ws.start()
        except Exception as e:
            print(e)

    def login_WS(self):
        try:
            self.browser_ws.stop()
        except Exception as e:
            print(e)

    async def open_browser(self):
        try:
            if '--enable-automation' in launcher.DEFAULT_ARGS:
                launcher.DEFAULT_ARGS.remove("--enable-automation")
            browser = await launch(headless=False, userDataDir=r'./wstext', executablePath='chrome_win64/chrome.exe', dumpio=True, autoClose=False,
                                   handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False,
                                   args=['--no-sandbox', '--window-size=1920,1080', '--disable-infobars',
                                         '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'])  # 进入有头模式

            page = await browser.newPage()
            page1 = await browser.newPage()
            # 设置页面视图大小
            await page.setViewport({'width': 1920, 'height': 1080})
            await page1.setViewport({'width': 1920, 'height': 1080})
            # 是否启用JS，enabled设为False，则无渲染效果
            await page.setJavaScriptEnabled(enabled=True)
            await page1.setJavaScriptEnabled(enabled=True)
            # self.mysignal.emit('开始获取')

            url = 'https://web.whatsapp.com/'
            url1 = 'https://id.zalo.me/account?continue=https://chat.zalo.me'
            await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
            await page1.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
            await page.goto(url)
            await page1.goto(url1)
        except:
            pass

    # WS推送
    # 初始化用户信息
    def ws_rewrite(self):
        if os.path.exists("WS_user_info.pkl"):
            pkl_file = open('WS_user_info.pkl', 'rb')
            list_file = pickle.load(pkl_file)
            pkl_file.close()
            self.lineEdit_2.setText(list_file[0])
            self.lineEdit_3.setText(list_file[1])
            self.lineEdit_4.setText(list_file[2])
            self.textEdit.setText(list_file[3])

    # 获取用户输入记录
    def ws_getdata(self):
        from_user = self.lineEdit_2.text()
        model_name = self.lineEdit_3.text()
        api = self.lineEdit_4.text()
        model_text = self.textEdit.toPlainText()
        model_lg = self.comboBox_7.currentText()
        print([from_user, model_name, api, model_text, model_lg])
        self.tuisong_Edit = [from_user,  model_name, api, model_text, model_lg]
        self.tuisong_Numbers = self.textEdit_7.toPlainText().replace("+", "").split('\n')
        if self.tableWidget_15.rowCount() > 34:
            self.tableWidget_15.setRowCount(len(self.tuisong_Numbers) / 2)

    # 测试推送
    def test_send(self):
        self.ws_getdata()
        if os.path.exists("WS_user_info.pkl"):
            os.remove('WS_user_info.pkl')
        f = open('WS_user_info.pkl', 'wb')
        pickle.dump(self.tuisong_Edit, f)
        f.close()

        self.WS_send = ws_tuisong.ws_send(self.tuisong_Edit,self.tuisong_Numbers)
        self.WS_send.mysignal.connect(self.print_ws_tuisong)
        self.WS_send.start()

    # 导入用户
    def import_user_ws_tuisong(self):
        filename = QFileDialog.getOpenFileName(self, '选择文件', os.getcwd(), "xlsx(*.xlsx);;文本文件(*txt)")[0]
        res = []
        self.textEdit_7.clear()
        if "xlsx" in filename:
            try:
                df = pd.read_excel(r"{}".format(filename))
                res = np.array(df['手机号'])
            except:
                self.textEdit_7.setText(str('格式不符，请导入含有“手机号”表头的xlsx文件'))
        elif '.txt' in filename:
            f1 = open(r"{}".format(filename), 'r')
            list_num = f1.readlines()
            f1.close()
            if list_num:
                df = pd.DataFrame({'手机号': list_num})
                df['手机号'] = df['手机号'].str.replace('\n', '')
                res = np.array(df['手机号'])
        else:
            pass
        text = ''
        for i in res:
            text = text + f'{i}' + '\n'
        self.textEdit_7.setText(text)
        self.label_36.setText(str(len(res)) + '个')

    # 启动推送
    def start_tuisong(self):
        self.ws_getdata()
        self.label_38.setText("0个")
        if self.tuisong_Edit and self.tuisong_Numbers:
            self.pushButton_63.setEnabled(False)
            self.WS_send = ws_tuisong.ws_send(self.tuisong_Edit, self.tuisong_Numbers)
            self.WS_send.mysignal.connect(self.print_ws_tuisong)
            self.WS_send.start()

    # 停止推送
    def stop_tuisong(self):
        try:
            if self.WS_send:
                self.pushButton_63.setEnabled(True)
                self.WS_send.quit()
                self.WS_send.stop()
                del self.WS_send
        except:
            pass

    # 输出
    def print_ws_tuisong(self, c, j, yn):
        if yn == '是':
            num = int(self.label_38.text()[:-1])
            num += 1
            self.label_38.setText(str(num) + "个")
        qt = QTableWidgetItem(yn)
        self.tableWidget_15.setItem(c, j, qt)
        self.tableWidget_15.verticalScrollBar().setSliderPosition(c)

    # 云邮获客
    # 初始化用户信息
    def email_rewrite(self):
        if os.path.exists("email_user_info.pkl"):
            pkl_file = open('email_user_info.pkl', 'rb')
            list_file = pickle.load(pkl_file)
            pkl_file.close()
            self.lineEdit_8.setText(list_file[0])
            self.lineEdit_9.setText(list_file[1])
            self.lineEdit_10.setText(list_file[2])
            self.textEdit_3.setText(list_file[3])

    # 获取用户输入记录
    def email_getdata(self):
        from_user = self.lineEdit_8.text()
        email_name = self.lineEdit_9.text()
        api = self.lineEdit_10.text()
        email_text = self.textEdit_3.toPlainText()
        print([from_user, email_name, api, email_text])
        self.qunfa_Edit = [from_user, email_name, api, email_text]
        self.qunfa_Numbers = self.textEdit_6.toPlainText().split('\n')
        print(self.qunfa_Numbers)
        if self.tableWidget_2.rowCount() > 17:
            self.tableWidget_2.setRowCount(len(self.qunfa_Numbers))

    # 测试群发
    def em_send(self):
        self.email_getdata()
        if os.path.exists("email_user_info.pkl"):
            os.remove('email_user_info.pkl')
        f = open('email_user_info.pkl', 'wb')
        pickle.dump(self.qunfa_Edit, f)
        f.close()
        self.email_send = email_qunfa.send(self.qunfa_Edit,self.qunfa_Numbers)
        self.email_send.mysignal.connect(self.print_email_qunfa)
        self.email_send.start()

    # 导入用户
    def import_user_email_qunfa(self):
        filename = QFileDialog.getOpenFileName(self, '选择文件', os.getcwd(), "xlsx(*.xlsx);;文本文件(*txt)")[0]
        res = []
        self.textEdit_6.clear()
        if "xlsx" in filename:
            try:
                df = pd.read_excel(r"{}".format(filename))
                res = np.array(df['邮箱'])
            except:
                self.textEdit_6.setText(str('格式不符，请导入含有“邮箱”表头的xlsx文件'))
        elif '.txt' in filename:
            f1 = open(r"{}".format(filename), 'r')
            list_num = f1.readlines()
            f1.close()
            if list_num:
                df = pd.DataFrame({'邮箱': list_num})
                df['邮箱'] = df['邮箱'].str.replace('\n', '')
                res = np.array(df['邮箱'])
        else:
            pass
        text = ''
        for i in res:
            text = text + f'{i}' + '\n'
        self.textEdit_6.setText(text)
        self.label_32.setText(str(len(res)) + '个')

    # 输出打印
    def print_email_qunfa(self, c, j, yn):
        if yn == '是':
            num = int(self.label_34.text()[:-1])
            num += 1
            self.label_34.setText(str(num) + "个")
        qt = QTableWidgetItem(yn)
        self.tableWidget_2.setItem(c, j, qt)
        self.tableWidget_2.verticalScrollBar().setSliderPosition(c)

    # 启动群发
    def start_qunfa(self):
        self.email_getdata()
        self.label_34.setText("0个")
        if self.qunfa_Edit and self.qunfa_Numbers:
            self.pushButton_48.setEnabled(False)
            self.email_send = email_qunfa.send(self.qunfa_Edit, self.qunfa_Numbers)
            self.email_send.mysignal.connect(self.print_email_qunfa)
            self.email_send.start()

    # 停止群发
    def stop_qunfa(self):
        try:
            if self.email_send:
                self.pushButton_48.setEnabled(True)
                self.email_send.quit()
                self.email_send.stop()
                print(self.email_send.tz)
                del self.email_send
        except:
            pass

    # 小组成员挖掘
    def import_232(self):
        filename = QFileDialog.getOpenFileName(self, '选择文件', os.getcwd(), "xlsx(*.xlsx);;文本文件(*txt)")[0]
        res = []
        self.textEdit_6.clear()
        if "xlsx" in filename:
            try:
                df = pd.read_excel(r"{}".format(filename))
                res = np.array(df['链接'])
            except:
                pass
        elif '.txt' in filename:
            f1 = open(r"{}".format(filename), 'r')
            list_num = f1.readlines()
            f1.close()
            if list_num:
                df = pd.DataFrame({'链接': list_num})
                df['链接'] = df['链接'].str.replace('\n', '')
                res = np.array(df['链接'])
        else:
            pass
        for i in res:
            self.list_url_xiaozu.append(i)
        print(self.list_url_xiaozu)
        self.print_group_munber(['导入小组成功'])

    def group_number(self):
        lis_xz = xz_231.li
        if lis_xz:
            self.pushButton_234.setEnabled(False)
            self.print_group_munber(['START'])
            self.WS_grp = group_munber.munber(self.list_url_xiaozu, lis_xz, self.headless)
            self.WS_grp.mysignal.connect(self.print_group_munber)
            self.print_group_munber(['START'])
            self.WS_grp.start()

    def print_group_munber(self, datalist, place='label'):
        if place=='table':
            row_cnt = self.tableWidget_23.rowCount()
            self.tableWidget_23.insertRow(row_cnt)
            column_cnt = self.tableWidget_23.rowCount()
            self.tableWidget_23.setItem(column_cnt - 1, 0, QTableWidgetItem(str(column_cnt)))
            for i in range(len(datalist)):
                self.tableWidget_23.setItem(column_cnt - 1, i+1, QTableWidgetItem(str(datalist[i])))
            self.tableWidget_23.verticalScrollBar().setSliderPosition(column_cnt + 1)
        elif place=='label':
            self.label_44.setText(datalist[0])

    def stop235(self):
        try:
            if self.WS_grp:
                self.pushButton_234.setEnabled(True)
                self.print_group_munber(['STOP'])
                self.WS_grp.quit()
                self.WS_grp.stop()
                del self.WS_grp
        except:
            pass
    # fb主页基础挖掘
    def fb_mainPage(self):
        print(gjc_83.gjcc)
        if gjc_83.gjcc:
            self.pushButton_84.setEnabled(False)
            self.fb_page = fb_pages.pages(gjc_83.gjcc,self.headless)
            self.fb_page.mysignal.connect(self.print_fbPages)
            self.print_fbPages(['START'])
            self.fb_page.start()


    def print_fbPages(self,datalist,place='label'):
        if place == 'table':
            row_cnt = self.tableWidget_18.rowCount()
            self.tableWidget_18.insertRow(row_cnt)
            column_cnt = self.tableWidget_18.rowCount()
            self.tableWidget_18.setItem(column_cnt - 1, 0, QTableWidgetItem(str(column_cnt)))
            for i in range(len(datalist)):
                self.tableWidget_18.setItem(column_cnt - 1, i+1, QTableWidgetItem(str(datalist[i])))
            self.tableWidget_18.verticalScrollBar().setSliderPosition(column_cnt + 1)
        elif place == 'label':
            self.label_24.setText(datalist[0])

    def stop_85(self):
        try:
            self.pushButton_84.setEnabled(True)
            self.fb_page.quit()
            self.fb_page.stop()
            del self.fb_page
        except:
            pass
    # fb小组基础挖掘
    def fb_mainGroup(self):
        if gjc_203.gjcc:
            self.pushButton_204.setEnabled(False)
            self.fb_group = fb_groups.groups(gjc_203.gjcc, self.headless)
            self.fb_group.mysignal.connect(self.print_fbGroups)
            self.print_fbGroups(['START'])
            self.fb_group.start()

    def print_fbGroups(self,datalist,place='label'):
        if place == 'table':
            row_cnt = self.tableWidget_19.rowCount()
            self.tableWidget_19.insertRow(row_cnt)
            column_cnt = self.tableWidget_19.rowCount()
            self.tableWidget_19.setItem(column_cnt - 1, 0, QTableWidgetItem(str(column_cnt)))
            for i in range(len(datalist)):
                self.tableWidget_19.setItem(column_cnt - 1, i+1, QTableWidgetItem(str(datalist[i])))
            self.tableWidget_19.verticalScrollBar().setSliderPosition(column_cnt + 1)
        elif place == 'label':
            self.label_25.setText(datalist[0])

    def stop_205(self):
        try:
            self.pushButton_204.setEnabled(True)
            self.fb_group.quit()
            self.fb_group.stop()
            del self.fb_group
        except:
            pass

    # fb直播基础挖掘
    def fb_mainLives(self):
        if gjc_227.gjcc:
            self.pushButton_228.setEnabled(False)
            self.fb_live = fb_lives.lives(gjc_227.gjcc, self.headless)
            self.fb_live.mysignal.connect(self.print_fbLives)
            self.print_fbLives(['START'])
            self.fb_live.start()


    def print_fbLives(self,datalist,place='label'):
        if place == 'table':
            row_cnt = self.tableWidget_22.rowCount()
            self.tableWidget_22.insertRow(row_cnt)
            column_cnt = self.tableWidget_22.rowCount()
            self.tableWidget_22.setItem(column_cnt - 1, 0, QTableWidgetItem(str(column_cnt)))
            for i in range(len(datalist)):
                self.tableWidget_22.setItem(column_cnt - 1, i+1, QTableWidgetItem(str(datalist[i])))
            self.tableWidget_22.verticalScrollBar().setSliderPosition(column_cnt + 1)
        elif place == 'label':
            self.label_43.setText(datalist[0])

    def stop_229(self):
        try:
            self.pushButton_228.setEnabled(True)
            self.fb_live.quit()
            self.fb_live.stop()
            del self.fb_live
        except:
            pass

    def ins_homePage(self):

        if self.ins_listPage != []:
            self.pushButton_145.setEnabled(False)
            self.ins_page = ins_homePage.ins_hp(self.ins_listPage,self.headless)
            self.ins_page.mysignal.connect(self.print_ins_homePage)
            self.print_ins_homePage(['START'])
            self.ins_page.start()

    def print_ins_homePage(self, datalist, place='label'):
        if place == 'table':
            row_cnt = self.tableWidget_13.rowCount()
            self.tableWidget_13.insertRow(row_cnt)
            column_cnt = self.tableWidget_13.rowCount()
            self.tableWidget_13.setItem(column_cnt - 1, 0, QTableWidgetItem(str(column_cnt)))
            for i in range(len(datalist)):
                self.tableWidget_13.setItem(column_cnt - 1, i+1, QTableWidgetItem(str(datalist[i])))
            self.tableWidget_13.verticalScrollBar().setSliderPosition(column_cnt + 1)
        elif place == 'label':
            self.label_55.setText(datalist[0])

    def daoruList_144(self):
        filename = QFileDialog.getOpenFileName(self, '选择文件', os.getcwd(), "xlsx(*.xlsx);;文本文件(*txt)")[0]
        if "xlsx" in filename:
            try:
                df = pd.read_excel(r"{}".format(filename))
                print(df)
                self.ins_listPage = list(df['链接'].values)
                print(self.ins_listPage)
                self.print_ins_homePage(["导入完成"])
            except:
                pass
        elif '.txt' in filename:
            f1 = open(r"{}".format(filename), 'r')
            list_num = f1.readlines()
            f1.close()
            if list_num:
                df = pd.DataFrame({'链接': list_num})
                df['链接'] = df['链接'].str.replace('\n', '')
                self.ins_listPage = list(df['链接'].values)
                print(self.ins_listPage)
                self.print_ins_homePage(["导入完成"])

    def stop148(self):
        try:
            self.pushButton_145.setEnabled(True)
            self.ins_page.quit()
            self.ins_page.stop()
            del self.ins_page
        except:
            pass

    def qp_150(self):
        for rowNum in range(0, self.tableWidget_6.rowCount())[::-1]:  # 逆序删除，正序删除会有一些删除不成功
            self.tableWidget_13.removeRow(rowNum)

    def ins_Search(self):
        if gjc_123.gjcc:
            self.pushButton_124.setEnabled(False)
            self.ins_SC = ins_search.ins_sc(gjc_123.gjcc,self.headless)
            self.ins_SC.mysignal.connect(self.print_insSearch)
            self.print_insSearch(['START'])
            self.ins_SC.start()


    def print_insSearch(self,datalist,place='label'):
        if place == 'table':
            row_cnt = self.tableWidget_10.rowCount()
            self.tableWidget_10.insertRow(row_cnt)
            column_cnt = self.tableWidget_10.rowCount()
            self.tableWidget_10.setItem(column_cnt - 1, 0, QTableWidgetItem(str(column_cnt)))
            for i in range(len(datalist)):
                self.tableWidget_10.setItem(column_cnt - 1, i+1, QTableWidgetItem(str(datalist[i])))
            self.tableWidget_10.verticalScrollBar().setSliderPosition(column_cnt + 1)
        elif place == 'label':
            self.label_52.setText(datalist[0])

    def stop127(self):
        try:
            self.pushButton_124.setEnabled(True)
            self.ins_SC.quit()
            self.ins_SC.stop()
            del self.ins_SC
        except:
            pass
    def qp_129(self):
        for rowNum in range(0, self.tableWidget_6.rowCount())[::-1]:  # 逆序删除，正序删除会有一些删除不成功
            self.tableWidget_10.removeRow(rowNum)

class qhwindow(QDialog, qh1.Ui_Form):

    def __init__(self):
        self.ye = 0
        self.unEnabled_button = None
        super(qhwindow, self).__init__()
        self.setupUi(self)
        self.qhh = []
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏边框
        self.pushButton_14.clicked.connect(self.get_chk)
        self.pushButton_15.clicked.connect(self.quanxuan)
        self.pushButton_16.clicked.connect(self.qingkong)
        self.pushButton_21.clicked.connect(lambda: self.change(0, self.pushButton_21))
        self.pushButton_22.clicked.connect(lambda: self.change(1, self.pushButton_22))
        self.pushButton_18.clicked.connect(lambda: self.change(2, self.pushButton_18))
        self.pushButton_19.clicked.connect(lambda: self.change(3, self.pushButton_19))
        self.pushButton_20.clicked.connect(lambda: self.change(4, self.pushButton_20))
        self.pushButton.clicked.connect(self.on_pushButtonMinimized)
        self.pushButton_3.clicked.connect(self.on_pushButtonClose)
        self.button_color()

        # self.pushButton_3.clicked.connect( self.btnclick) #按钮事件绑定
    def mousePressEvent(self, event):  # 鼠标左键按下时获取鼠标坐标,按下右键取消
        if event.button() == Qt.LeftButton:
            self.m_Position = event.globalPos() - self.pos()
            if self.m_Position.y() < 31:
                self.m_flag = True
                event.accept()
        elif event.button() == Qt.RightButton:
            self.m_flag = False

    def mouseMoveEvent(self, QMouseEvent):  # 鼠标在按下左键的情况下移动时,根据坐标移动界面
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):  # 鼠标按键释放时,取消移动
        self.m_flag = False

    def on_pushButtonMinimized(self):
        self.showMinimized()

    def on_pushButtonClose(self):
        self.close()

    def button_color(self):
        self.pushButton_21.setEnabled(False)
        self.unEnabled_button = self.pushButton_21

    def change(self, page, btn):
        self.ye = page
        self.unEnabled_button.setEnabled(True)
        self.unEnabled_button = btn
        self.unEnabled_button.setEnabled(False)
        self.stackedWidget.setCurrentIndex(page)

    def qingkong(self):
        n = self.ye
        if n == 0:

            self.Item = self.groupBox.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(False)
        if n == 1:

            self.Item = self.groupBox_2.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(False)
        if n == 2:

            self.Item = self.groupBox_3.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(False)
        if n == 3:

            self.Item = self.groupBox_4.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(False)
        if n == 4:

            self.Item = self.groupBox_5.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(False)
        else:
            pass

    def quanxuan(self):
        n = self.ye
        if n == 0:
            # print('1')

            self.Item = self.groupBox.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(True)
        if n == 1:
            # print('2')
            self.Item = self.groupBox_2.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(True)
        if n == 2:
            # print('3')
            self.Item = self.groupBox_3.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(True)
        if n == 3:
            # print('4')
            self.Item = self.groupBox_4.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(True)
        if n == 4:
            # print('5')
            self.Item = self.groupBox_5.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(True)
        else:
            pass

    def get_chk(self):
        # print(qhtext)
        self.qhh = []

        self.sItem = self.stackedWidget.findChildren(QtWidgets.QGroupBox)
        for sit in self.sItem:
            self.Item = sit.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                if it.isChecked() == True:
                    # print(it.text())
                    qh = re.findall(r"\d+", it.text())
                    # print(qh[0])
                    self.qhh.append(qh[0])
                else:
                    pass
        self.close()
        qhtext = self.lineEdit.text()

        if qhtext != '':
            self.qhh.append(qhtext)
        else:
            pass

        if len(self.qhh) != 0:

            print(self.qhh)
            main.print1(['地区导入成功'])
        else:
            main.print1(['请输入地区'])
            pass


class dq6window(QDialog, dq6.Ui_Form):

    def __init__(self):
        self.ye = 0
        self.unEnabled_button = None
        super(dq6window, self).__init__()
        self.setupUi(self)
        self.qhh = []
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏边框
        self.pushButton_14.clicked.connect(self.get_chk)
        self.pushButton_15.clicked.connect(self.quanxuan)
        self.pushButton_16.clicked.connect(self.qingkong)
        self.pushButton_21.clicked.connect(lambda: self.change(0, self.pushButton_21))
        self.pushButton_22.clicked.connect(lambda: self.change(1, self.pushButton_22))
        self.pushButton_18.clicked.connect(lambda: self.change(2, self.pushButton_18))
        self.pushButton_19.clicked.connect(lambda: self.change(3, self.pushButton_19))
        self.pushButton_20.clicked.connect(lambda: self.change(4, self.pushButton_20))
        self.pushButton.clicked.connect(self.on_pushButtonMinimized)
        self.pushButton_3.clicked.connect(self.on_pushButtonClose)
        self.button_color()

        # self.pushButton_3.clicked.connect( self.btnclick) #按钮事件绑定


    def mousePressEvent(self, event):  # 鼠标左键按下时获取鼠标坐标,按下右键取消
        if event.button() == Qt.LeftButton:
            self.m_Position = event.globalPos() - self.pos()
            if self.m_Position.y() < 31:
                self.m_flag = True
                event.accept()
        elif event.button() == Qt.RightButton:
            self.m_flag = False


    def mouseMoveEvent(self, QMouseEvent):  # 鼠标在按下左键的情况下移动时,根据坐标移动界面
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()


    def mouseReleaseEvent(self, QMouseEvent):  # 鼠标按键释放时,取消移动
        self.m_flag = False


    def on_pushButtonMinimized(self):
        self.showMinimized()


    def on_pushButtonClose(self):
        self.close()

        # self.pushButton_3.clicked.connect( self.btnclick) #按钮事件绑定

    def button_color(self):
        self.pushButton_21.setEnabled(False)
        self.unEnabled_button = self.pushButton_21

    def change(self, page, btn):
        self.ye = page
        self.unEnabled_button.setEnabled(True)
        self.unEnabled_button = btn
        self.unEnabled_button.setEnabled(False)
        self.stackedWidget.setCurrentIndex(page)

    def qingkong(self):
        n = self.ye
        if n == 0:

            self.Item = self.groupBox.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(False)
        if n == 1:

            self.Item = self.groupBox_2.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(False)
        if n == 2:

            self.Item = self.groupBox_3.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(False)
        if n == 3:

            self.Item = self.groupBox_4.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(False)
        if n == 4:

            self.Item = self.groupBox_5.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(False)
        else:
            pass

    def quanxuan(self):
        n = self.ye
        if n == 0:
            # print('1')

            self.Item = self.groupBox.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(True)
        if n == 1:
            # print('2')
            self.Item = self.groupBox_2.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(True)
        if n == 2:
            # print('3')
            self.Item = self.groupBox_3.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(True)
        if n == 3:
            # print('4')
            self.Item = self.groupBox_4.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(True)
        if n == 4:
            # print('5')
            self.Item = self.groupBox_5.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(True)
        else:
            pass

    def get_chk(self):
        self.close()
        qhtext = self.lineEdit.text()
        # print(qhtext)
        self.qhh = []

        self.sItem = self.stackedWidget.findChildren(QtWidgets.QGroupBox)
        for sit in self.sItem:
            self.Item = sit.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                if it.isChecked() == True:
                    self.qhh.append(it.text())
                else:
                    pass
                if qhtext:
                    if qhtext not in self.qhh:
                        self.qhh.append(qhtext)
        self.cnToen()

    def cnToen(self):
        li_dq = []
        print(self.qhh)
        with open('LocList.json','r',encoding='utf-8') as f:
            data = json.loads(f.read())
        for i in self.qhh:
            for j in data['Location']['CountryRegion']:
                if j["@cn_Name"] == i:
                    print(j['@Name'])
                    try:
                        if type(j["State"]) is list:
                            for states in j["State"]:
                                try:
                                    if type(states['City']) is list:
                                        for cities in states['City']:
                                            city = j['@Name']+' '+cities["@Name"]
                                            li_dq.append(city)
                                    else:
                                        li_dq.append(j['@Name']+' '+states['City']["@Name"].replace(u'\xa0',' '))
                                except Exception as e:
                                    print('错误：',e)
                                    li_dq.append(j['@Name']+' '+states['@Name'].replace(u'\xa0',' '))
                        else:
                            for city in j["State"]["City"]:
                                li_dq.append(j['@Name']+' '+city["@Name"].replace(u'\xa0',' '))
                    except Exception as e:
                        print('错误：',e)
                        li_dq.append(j['@Name'].replace(u'\xa0',' '))
                    break
        print(li_dq)
        main.gg_dq = li_dq
        main.print_map(['地区选择成功'])


class ptwindow(QDialog, pt1.Ui_Form):

    def __init__(self, id):
        self.ye = 0
        self.id = id
        self.unEnabled_button = None
        super(ptwindow, self).__init__()
        self.setupUi(self)
        self.ptt = []
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏边框
        self.pushButton_14.clicked.connect(self.get_chk)
        self.pushButton_15.clicked.connect(self.quanxuan)
        self.pushButton_16.clicked.connect(self.qingkong)
        self.pushButton_21.clicked.connect(lambda: self.change(0, self.pushButton_21))
        self.pushButton_22.clicked.connect(lambda: self.change(1, self.pushButton_22))
        self.pushButton_18.clicked.connect(lambda: self.change(2, self.pushButton_18))
        self.pushButton_19.clicked.connect(lambda: self.change(3, self.pushButton_19))
        self.pushButton.clicked.connect(self.on_pushButtonMinimized)
        self.pushButton_3.clicked.connect(self.on_pushButtonClose)
        self.button_color()

        # self.pushButton_3.clicked.connect( self.btnclick) #按钮事件绑定


    def mousePressEvent(self, event):  # 鼠标左键按下时获取鼠标坐标,按下右键取消
        if event.button() == Qt.LeftButton:
            self.m_Position = event.globalPos() - self.pos()
            if self.m_Position.y() < 31:
                self.m_flag = True
                event.accept()
        elif event.button() == Qt.RightButton:
            self.m_flag = False


    def mouseMoveEvent(self, QMouseEvent):  # 鼠标在按下左键的情况下移动时,根据坐标移动界面
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()


    def mouseReleaseEvent(self, QMouseEvent):  # 鼠标按键释放时,取消移动
        self.m_flag = False


    def on_pushButtonMinimized(self):
        self.showMinimized()


    def on_pushButtonClose(self):
        self.close()

    def button_color(self):
        self.pushButton_21.setEnabled(False)
        self.unEnabled_button = self.pushButton_21

    def change(self, page, btn):
        self.ye = page
        self.unEnabled_button.setEnabled(True)
        self.unEnabled_button = btn
        self.unEnabled_button.setEnabled(False)
        self.stackedWidget.setCurrentIndex(page)

    def mousePressEvent(self, event):  # 鼠标左键按下时获取鼠标坐标,按下右键取消
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
        elif event.button() == Qt.RightButton:
            self.m_flag = False

    def mouseMoveEvent(self, QMouseEvent):  # 鼠标在按下左键的情况下移动时,根据坐标移动界面
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):  # 鼠标按键释放时,取消移动
        self.m_flag = False

    def qingkong(self):
        n = self.ye
        if n == 0:

            self.Item = self.groupBox.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(False)
        if n == 1:

            self.Item = self.groupBox_2.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(False)
        if n == 2:

            self.Item = self.groupBox_3.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(False)
        if n == 3:

            self.Item = self.groupBox_4.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(False)
        else:
            pass

    def quanxuan(self):
        n = self.ye
        if n == 0:

            self.Item = self.groupBox.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(True)
        if n == 1:

            self.Item = self.groupBox_2.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(True)
        if n == 2:

            self.Item = self.groupBox_3.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(True)
        if n == 3:

            self.Item = self.groupBox_4.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                it.setChecked(True)
        else:
            pass

    def get_chk(self):
        if self.id == '全球活跃挖掘':
            self.get_chk1()
        elif self.id == '公开小组挖掘':
            self.get_chk2()

    def get_chk1(self):
        pttext = self.lineEdit.text()
        # print(qhtext)
        self.ptt = []
        if pttext:
            self.ptt.append(pttext)
        self.sItem = self.stackedWidget.findChildren(QtWidgets.QGroupBox)
        for sit in self.sItem:
            self.Item = sit.findChildren(QtWidgets.QCheckBox)
            for it in self.Item:
                if it.isChecked() == True:
                    # print(it.text())
                    self.ptt.append(it.text())
                else:
                    pass
        self.ptt = list(set(self.ptt))
        self.close()
        print(self.ptt)
        main.print1(['平台导入成功'])
        # self.pushButton_3.clicked.connect( self.btnclick) #按钮事件绑定

    def get_chk2(self):
        pttext = self.lineEdit.text()
        self.ptt = []
        if pttext:
            self.ptt.append(pttext)
        self.Item = self.groupBox.findChildren(QtWidgets.QCheckBox)
        for it in self.Item:
            if it.isChecked() == True:
                # print(it.text())
                self.ptt.append(it.text())
            else:
                pass
        self.ptt = list(set(self.ptt))
        self.close()
        print(self.ptt)
        main.print17(['平台导入成功'])


class gjcwindow(QDialog, gjc.Ui_Form):

    def __init__(self, id):
        self.id = id
        super(gjcwindow, self).__init__()
        self.setupUi(self)
        self.gjcc = []
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏边框
        self.pushButton_14.clicked.connect(self.zhantie)
        self.pushButton_15.clicked.connect(self.queren)
        self.pushButton_16.clicked.connect(self.qingchu)
        self.pushButton.clicked.connect(self.on_pushButtonMinimized)
        self.pushButton_3.clicked.connect(self.on_pushButtonClose)

        # self.pushButton_3.clicked.connect( self.btnclick) #按钮事件绑定


    def mousePressEvent(self, event):  # 鼠标左键按下时获取鼠标坐标,按下右键取消
        if event.button() == Qt.LeftButton:
            self.m_Position = event.globalPos() - self.pos()
            if self.m_Position.y() < 31:
                self.m_flag = True
                event.accept()
        elif event.button() == Qt.RightButton:
            self.m_flag = False


    def mouseMoveEvent(self, QMouseEvent):  # 鼠标在按下左键的情况下移动时,根据坐标移动界面
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()


    def mouseReleaseEvent(self, QMouseEvent):  # 鼠标按键释放时,取消移动
        self.m_flag = False


    def on_pushButtonMinimized(self):
        self.showMinimized()

    def on_pushButtonClose(self):
        self.close()

    def mousePressEvent(self, event):  # 鼠标左键按下时获取鼠标坐标,按下右键取消
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
        elif event.button() == Qt.RightButton:
            self.m_flag = False

    def mouseMoveEvent(self, QMouseEvent):  # 鼠标在按下左键的情况下移动时,根据坐标移动界面
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):  # 鼠标按键释放时,取消移动
        self.m_flag = False

    def zhantie(self):
        # print('1')
        self.qingchu()
        self.gjcc = []
        text = QApplication.clipboard().text()
        rows = text.split('\n')
        # print(rows)
        for row in rows:
            self.textEdit.append(row)
            self.gjcc.append(row)
        print(self.gjcc)

    def queren(self):
        if self.id == "全球活跃挖掘":
            self.daoru_1()
        else:
            self.daoru_2()

    def daoru_1(self):
        self.gjcc = []
        text_edit_text = self.textEdit.toPlainText()
        lis_gjc = text_edit_text.strip().split("\n")
        print("lis_gjc", lis_gjc)
        self.gjcc = lis_gjc
        self.close()

        QH = qh.qhh
        GJC = gjc.gjcc
        PT = pt.ptt
        Opt = []
        Dpt = ['facebook', 'instagram', 'Linkedin', 'Twitter', 'Tiktok', 'Youtube']
        for t in Dpt:
            if t in PT:
                Opt.append(t)
        if len(Opt) == 0:
            Opt.append('facebook')
        print(Opt)

        yy = ['']
        # yy = [chr(y) for y in range(97, 123)]
        for y in range(97, 123):
            yy.append(chr(y))
        # print(yy)

        print(QH)
        print(GJC)
        fbkeys = {}
        if QH != [] and GJC != []:
            # print(QH)
            # print(GJC)
            # self.print1('任务开始')

            for qq in QH:
                # print(qq)
                for p in Opt:
                    for key in GJC:
                        keys = str(key)
                        fbkey = 'call +' + qq + ' ' + '\'' + keys + '\'' + ' site:{}.com'.format(p)
                        fbkeys[fbkey] = key

                        fbkey = 'whatsapp +' + qq + ' ' + '\'' + keys + '\'' + ' site:{}.com'.format(p)
                        fbkeys[fbkey] = key
            print(fbkeys)
            rwoutput = open('renwu.pkl', 'wb')
            pickle.dump(fbkeys, rwoutput)
            rwoutput.close()
            main.print1(['关键词导入成功'])
        else:
            main.print1(['请先输入区号、关键词'])
            print('请先输入区号、关键词')

    def daoru_2(self):
        self.close()
        self.gjcc = []
        text_edit_text = self.textEdit.toPlainText()
        lis_gjc = text_edit_text.strip().split("\n")
        print("lis_gjc", lis_gjc)
        self.gjcc = lis_gjc
        if self.id == "公开小组挖掘":
            lis_words = []
            dic_words = {}
            XZ = xz.li
            PT = ['facebook', 'instagram']
            print(XZ, PT, self.gjcc)
            if XZ != [] and PT != [] and self.gjcc != []:
                for c in self.gjcc:
                    if c:
                        for x in XZ:
                            for t in PT:
                                word = f"site:www.{t}.com '{c}' {x}"
                                lis_words.append(word)
                        dic_words[c] = lis_words
                print(dic_words)
                rwoutput = open('renwu2.pkl', 'wb')
                pickle.dump(dic_words, rwoutput)
                rwoutput.close()
                main.print17(['关键词导入成功'])
            else:
                main.print17(['请先输入区号、关键词'])
                print('请先输入区号、关键词')
        elif self.id == '谷歌地图获客':
            main.print_map(['关键词导入成功'])
        elif self.id == '主页基础挖掘':
            main.print_fbPages(['关键词导入成功'])
        elif self.id == '小组基础挖掘':
            main.print_fbGroups(['关键词导入成功'])
        elif self.id == 'in指定搜索挖掘':
            main.print_insSearch(['关键词导入成功'])

    def qingchu(self):
        # print('3')
        self.textEdit.clear()

        # self.pushButton_3.clicked.connect( self.btnclick) #按钮事件绑定


class xzwindow(QDialog, xz1.Ui_Form):
    def __init__(self, id):
        self.id = id
        self.li = []
        super(xzwindow, self).__init__()
        self.setupUi(self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏边框
        self.pushButton_14.clicked.connect(self.queren)
        self.pushButton_15.clicked.connect(self.quanxuan)
        self.pushButton_16.clicked.connect(self.qingchu)
        self.pushButton.clicked.connect(self.on_pushButtonMinimized)
        self.pushButton_3.clicked.connect(self.on_pushButtonClose)

        # self.pushButton_3.clicked.connect( self.btnclick) #按钮事件绑定

    def mousePressEvent(self, event):  # 鼠标左键按下时获取鼠标坐标,按下右键取消
        if event.button() == Qt.LeftButton:
            self.m_Position = event.globalPos() - self.pos()
            if self.m_Position.y() < 31:
                self.m_flag = True
                event.accept()
        elif event.button() == Qt.RightButton:
            self.m_flag = False

    def mouseMoveEvent(self, QMouseEvent):  # 鼠标在按下左键的情况下移动时,根据坐标移动界面
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):  # 鼠标按键释放时,取消移动
        self.m_flag = False

    def on_pushButtonMinimized(self):
        self.showMinimized()

    def on_pushButtonClose(self):
        self.close()

    def mousePressEvent(self, event):  # 鼠标左键按下时获取鼠标坐标,按下右键取消
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
        elif event.button() == Qt.RightButton:
            self.m_flag = False

    def mouseMoveEvent(self, QMouseEvent):  # 鼠标在按下左键的情况下移动时,根据坐标移动界面
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):  # 鼠标按键释放时,取消移动
        self.m_flag = False

    def queren(self):
        self.close()
        self.li = []
        whatsapp = self.checkBox_2.isChecked()
        zalo = self.checkBox_3.isChecked()
        if whatsapp:
            self.li.append('https://chat.whatsapp.com')
        if zalo:
            self.li.append('https://zalo.me/g/')
        main.xz = self.li
        print(self.li)
        if self.id == '小组活跃挖掘':
            main.print17(['小组选择成功'])
        elif self.id == '小组成员挖掘':
            main.print_group_munber(['小组选择成功'])

    def quanxuan(self):
        self.checkBox_2.setChecked(True)
        self.checkBox_3.setChecked(True)

    def qingchu(self):
        self.checkBox_2.setChecked(False)
        self.checkBox_3.setChecked(False)


class childWindow_daochu1(QWidget, huoke_daochu.Ui_Form):
    def __init__(self, database, header):
        self.datas = None  # 未修改过的数据
        self.table = None  # 变动的数据
        self.Header = header
        self.database = database
        QWidget.__init__(self)
        self.child = huoke_daochu.Ui_Form()
        self.child.setupUi(self)
        # self.show_data()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框
        self.child.tableWidget.setColumnCount(len(self.Header))
        self.child.tableWidget.setHorizontalHeaderLabels(self.Header)
        self.child.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.child.tableWidget.setAlternatingRowColors(True)
        self.child.pushButton_4.clicked.connect(self.duplicate_removal)
        self.child.pushButton_2.clicked.connect(self.search_data)
        self.child.checkBox.clicked.connect(self.change_clickBox)
        self.child.pushButton_3.clicked.connect(self.clear_tabel)
        self.child.pushButton.clicked.connect(self.outPut_excel)
        self.child.pushButton_5.clicked.connect(self.refresh)
        self.child.pushButton_6.clicked.connect(self.on_pushButton_6_click)
        self.child.pushButton_7.clicked.connect(self.on_pushButton_7_click)


    def mousePressEvent(self, event):  # 鼠标左键按下时获取鼠标坐标,按下右键取消
        if event.button() == Qt.LeftButton:
            self.m_Position = event.globalPos() - self.pos()
            if self.m_Position.y() < 31:
                self.m_flag = True
                print(self.m_Position, event.globalPos(), self.pos(), self.m_Position.y())
                event.accept()
        elif event.button() == Qt.RightButton:
            self.m_flag = False

    def mouseMoveEvent(self, QMouseEvent):  # 鼠标在按下左键的情况下移动时,根据坐标移动界面
        try:
            if Qt.LeftButton and self.m_flag:
                self.move(QMouseEvent.globalPos() - self.m_Position)
                QMouseEvent.accept()
        except:
            pass

    def mouseReleaseEvent(self, QMouseEvent):  # 鼠标按键释放时,取消移动
        self.m_flag = False

    def on_pushButton_6_click(self):
        self.showMinimized()

    def on_pushButton_7_click(self):
        self.close()

    # 展示数据
    def show_data(self):
        self.remove_tabel()
        con = sqlite3.connect(self.database)
        cur = con.cursor()
        t_name = cur.execute("select name from sqlite_master where type='table'").fetchone()[0]
        cursor = cur.execute('select * from {}'.format(t_name))
        if cursor is not None:
            biao = pd.DataFrame(data=cursor, columns=self.Header)

            # print(biao)

            self.datas = copy.deepcopy(biao)
            self.table = biao
            self.load_data()
            self.change_comboBox()
        con.close()

    # 根据手机号去重
    def duplicate_removal(self):
        if self.datas is not None and self.database == 'HKHM.db':
            self.table = self.table.drop_duplicates(subset=["手机号"])

        elif self.datas is not None and self.database == 'HKLBS.db':
            self.table = self.table.drop_duplicates(subset=["商店名"])

        elif self.datas is not None and self.database == 'HKGKXZ.db':
            self.table = self.table.drop_duplicates(subset=["链接"])
            # print(self.table[self.table['链接'].str.len() == 1])
            # print(self.table[self.table['链接'].str.len() == 27])
            self.table = self.table[(self.table['链接'].str.len() == 48) | (self.table['链接'].str.len() == 27)]

        elif self.datas is not None and self.database == 'HKFBZY.db':
            self.table = self.table.drop_duplicates(subset=['链接'])

        elif self.datas is not None and self.database == 'HKFBXZ.db':
            self.table = self.table.drop_duplicates(subset=['链接'])

        elif self.datas is not None and self.database == 'HKXZCY.db':
            self.table = self.table.drop_duplicates(subset=["手机号/用户名"])

        elif self.datas is not None and self.database == 'INSPAGE.db':
            self.table = self.table.drop_duplicates(subset=["用户名"])
        self.remove_tabel()
        self.load_data()

    # 清空列表展示
    def remove_tabel(self):
        for rowNum in range(0, self.child.tableWidget.rowCount())[::-1]:  # 逆序删除，正序删除会有一些删除不成功
            self.child.tableWidget.removeRow(rowNum)

    # 加载数据展示
    def load_data(self):
        n = np.array(self.table)
        print(self.table)
        for i in range(len(n)):
            row_count = self.child.tableWidget.rowCount()
            self.child.tableWidget.insertRow(row_count)
            for j in range(len(self.Header)):
                self.child.tableWidget.setItem(i, j, QTableWidgetItem(str(n[i][j])))
        data_num = self.child.tableWidget.rowCount()
        self.child.label_2.setText(str(data_num))

    # 条件查询
    def search_data(self):
        if self.datas is not None:
            current_index = self.child.comboBox.currentIndex()
            current_text = self.child.comboBox.currentText()
            tm = re.findall(r'[0-9]{4}-[0-9]{2}-[0-9]{2}',current_text,re.S)
            print(current_index)
            time = self.child.comboBox.currentText()
            # print(type(time))
            if self.database == 'HKHM.db':
                print(self.child.spinBox.value())
                len_num = self.child.spinBox.value()
                self.table = self.datas[self.datas['手机号'].str.len() >= len_num]
                if current_index != 0:
                    self.table = self.table[self.table['时间'].str[:10].values == time]
                if self.child.checkBox.isChecked():
                    self.table = self.table[self.table['手机号'].str[0].values == '+']
            if self.database == 'HKXZCY.db':
                if current_index != 0 and tm!=[]:
                    self.table = self.datas[self.datas['时间'].str[:10].values == time]
                elif not tm:
                    self.table = self.datas[self.datas['平台'].values == current_text]
            else:
                self.table = self.datas[self.datas['时间'].str[:10].values == time]
            self.remove_tabel()
            self.load_data()

    # 动态加载comboBox
    def change_comboBox(self):
        if self.datas is not None:
            times = list(set(self.datas['时间'].str[:10].values))
            self.child.comboBox.addItems(times)
            if self.database == 'HKGKXZ.db' or self.database == 'HKLBS.db':
                words = list(set(self.datas['关键词'].str[:10].values))
                self.child.comboBox.addItems(words)
            elif self.database == 'HKXZCY.db':
                words = list(set(self.datas['平台']))
                self.child.comboBox.addItems(words)

    # 改变clickBox
    def change_clickBox(self):
        print('点击clickBox')
        if self.datas is not None and self.database == 'HKHM.db' or self.database == 'HKLBS.db':
            if self.child.checkBox.isChecked():
                self.table['手机号'] = self.table['手机号'].str.replace(r"^(\d)", r"+\1", regex=True)
                self.remove_tabel()
                self.load_data()
            else:
                self.table = self.datas
                self.search_data()

    # 清空表数据
    def clear_tabel(self):
        que_box = QMessageBox.question(self, '警告', '是否清空表', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if que_box == QMessageBox.Yes and self.datas is not None:
            self.remove_tabel()
            con = sqlite3.connect(self.database)
            cur = con.cursor()
            t_name = cur.execute("select name from sqlite_master where type='table'").fetchone()[0]
            cur.execute('DELETE from {}'.format(t_name))
            con.commit()
            con.close()
            self.table = []
            self.datas = []
        else:
            pass

    # 导出到excel
    def outPut_excel1(self):
        data = pd.DataFrame(self.table)
        filepath = QFileDialog.getSaveFileName(self, '文件保存', './', 'xlsx(*.xlsx')[0]
        if filepath is True:
            data.to_excel(r'{}'.format(filepath), sheet_name='Sheet1', index=False)

    def outPut_excel(self):
        try:
            dir_path = QFileDialog.getExistingDirectory(None, "请选择文件夹", "D:\\")
            print(dir_path)

            data = pd.DataFrame(self.table)
            if self.database == "HKHM.db":
                path = dir_path + '/' + '获客' + re.sub(r'[^0-9]', '',
                                                        datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + '.xlsx'
                with pd.ExcelWriter(path) as writer:
                    data.to_excel(writer, sheet_name='号码')
                main.print1(['导出成功'])
                main.print1([str(path)])
            elif self.database == 'HKLBS.db':
                path = dir_path + '/' + '谷歌地图' + re.sub(r'[^0-9]', '',
                                                            datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + '.xlsx'
                with pd.ExcelWriter(path) as writer:
                    data.to_excel(writer, sheet_name='号码')
                main.print_map(['导出成功'])
                main.print_map([str(path)])
            elif self.database == "HKGKXZ.db":
                path = dir_path + '/' + '公开小组' + re.sub(r'[^0-9]', '',
                                                            datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + '.xlsx'
                with pd.ExcelWriter(path) as writer:
                    data.to_excel(writer)
                main.print17(['导出成功'])
                main.print17([str(path)])
            elif self.database == 'HKXZCY.db':
                path = dir_path + '/' + '小组成员' + re.sub(r'[^0-9]', '',
                                                            datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + '.xlsx'
                with pd.ExcelWriter(path) as writer:
                    data.to_excel(writer)
                main.print_group_munber(['导出成功'])
                main.print_group_munber([str(path)])
            elif self.database == 'HKFBZY.db':
                path = dir_path + '/' + '主页基础' + re.sub(r'[^0-9]', '',
                                                            datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + '.xlsx'
                with pd.ExcelWriter(path) as writer:
                    data.to_excel(writer)
                main.print_fbPages(['导出成功'])
                main.print_fbPages([str(path)])
            elif self.database == 'HKFBXZ.db':
                path = dir_path + '/' + '小组基础' + re.sub(r'[^0-9]', '',
                                                            datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + '.xlsx'
                with pd.ExcelWriter(path) as writer:
                    data.to_excel(writer)
                main.print_fbGroups(['导出成功'])
                main.print_fbGroups([str(path)])
            elif self.database == 'HKFBZB.db':
                path = dir_path + '/' + '直播基础' + re.sub(r'[^0-9]', '',
                                                            datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + '.xlsx'
                with pd.ExcelWriter(path) as writer:
                    data.to_excel(writer)
                main.print_fbLives(['导出成功'])
                main.print_fbLives([str(path)])
            elif self.database == 'INSPAGE.db':
                path = dir_path + '/' + 'ins主页详情' + re.sub(r'[^0-9]', '',
                                                            datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + '.xlsx'
                with pd.ExcelWriter(path) as writer:
                    data.to_excel(writer)
                main.print_ins_homePage(['导出成功'])
                main.print_ins_homePage([str(path)])
            elif self.database == 'INSSEARCH.db':
                path = dir_path + '/' + 'ins指定搜索' + re.sub(r'[^0-9]', '',
                                                               datetime.datetime.now().strftime(
                                                                   "%Y%m%d%H%M%S")) + '.xlsx'
                with pd.ExcelWriter(path) as writer:
                    data.to_excel(writer)
                main.print_insSearch(['导出成功'])
                main.print_insSearch([str(path)])
        except:
            main.print9(['Please re-enter'])
            pass

    def refresh(self):
        try:
            self.child.comboBox.clear()
            self.child.comboBox.addItem('全部')
            self.show_data()
        except:
            pass


class childWindow_daochu2(QWidget, xiaozu_daochu.Ui_Form):
    def __init__(self, database, bname):
        self.datas = None
        self.table = None
        self.database = database
        self.bname = bname
        QWidget.__init__(self)
        self.child = xiaozu_daochu.Ui_Form()
        self.child.setupUi(self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框
        self.child.tableWidget.setColumnWidth(0, 150)
        self.child.tableWidget.setColumnWidth(1, 150)
        self.child.tableWidget.setColumnWidth(2, 500)
        self.child.tableWidget.setColumnWidth(3, 170)
        self.child.tableWidget.setAlternatingRowColors(True)
        self.child.pushButton_4.clicked.connect(self.duplicate_removal)
        self.child.pushButton_5.clicked.connect(self.refresh)
        self.child.pushButton_2.clicked.connect(self.search_data)
        self.child.pushButton_3.clicked.connect(self.clear_tabel)
        self.child.pushButton.clicked.connect(self.outPut_excel)
        self.setFixedSize(1005, 725)
        self.child.pushButton_6.clicked.connect(self.on_pushButton_6_click)
        self.child.pushButton_7.clicked.connect(self.on_pushButton_7_click)

    def mousePressEvent(self, event):  # 鼠标左键按下时获取鼠标坐标,按下右键取消
        if event.button() == Qt.LeftButton:
            self.m_Position = event.globalPos() - self.pos()
            if self.m_Position.y() < 31:
                self.m_flag = True
                event.accept()
        elif event.button() == Qt.RightButton:
            self.m_flag = False

    def mouseMoveEvent(self, QMouseEvent):  # 鼠标在按下左键的情况下移动时,根据坐标移动界面
        try:
            if Qt.LeftButton and self.m_flag:
                self.move(QMouseEvent.globalPos() - self.m_Position)
                QMouseEvent.accept()
        except:
            pass

    def mouseReleaseEvent(self, QMouseEvent):  # 鼠标按键释放时,取消移动
        self.m_flag = False

    def on_pushButton_6_click(self):
        self.showMinimized()

    def on_pushButton_7_click(self):
        self.close()

    def show_data(self):
        con = sqlite3.connect(r'{}'.format(self.database))
        cur = con.cursor()
        t_name = cur.execute("select name from sqlite_master where type='table'").fetchone()[0]
        cursor = cur.execute('select * from {}'.format(t_name))
        if cursor is not None:
            biao = pd.DataFrame(data=cursor, columns=["用户名", "ID", "链接", "时间"])
            con.close()
            self.datas = copy.deepcopy(biao)
            self.table = biao
            self.load_data()
            self.change_comboBox()
        con.close()

    def search_data(self):
        if self.datas is not None:
            current_index = self.child.comboBox.currentIndex()
            time = self.child.comboBox.currentText()
            if current_index != 0:
                self.table = self.datas[self.datas['时间'].str[:10].values == time]
            else:
                self.table = self.datas
            self.remove_tabel()
            self.load_data()

    def load_data(self):
        n = np.array(self.table)
        for i in range(len(n)):
            row_count = self.child.tableWidget.rowCount()
            self.child.tableWidget.insertRow(row_count)
            for j in range(4):
                self.child.tableWidget.setItem(i, j, QTableWidgetItem(str(n[i][j])))
        data_num = self.child.tableWidget.rowCount()
        self.child.label_2.setText(str(data_num))

    def duplicate_removal(self):
        if self.datas is not None:
            if self.database[-9:] == 'HKHMZY.db' or self.database[-9:] == 'HYDQWJ.db':
                self.table = self.table.drop_duplicates(subset=["用户名"])
            elif self.database[-10:] == 'HKHMINS.db':
                self.table = self.table.drop_duplicates(subset=["ID"])
                self.table = self.table[~self.table["用户名"].str.contains('分钟')]
                self.table = self.table[~self.table["用户名"].str.contains('小时')]
            elif self.database[-10:] == 'INSLIKE.db' or self.database[-8:] == 'FTHFS.db' or self.database[
                                                                                            -11:] == 'INSLABEL.db':
                self.table = self.table.drop_duplicates(subset=["链接"])
            else:
                self.table = self.table[self.table['ID'].str.isdecimal()]
                self.table = self.table.drop_duplicates(subset=["ID"])
                self.table = self.table[~self.table["用户名"].str.contains('分钟')]
                self.table = self.table[~self.table["用户名"].str.contains('小时')]
            self.remove_tabel()
            self.load_data()

    def remove_tabel(self):
        for rowNum in range(0, self.child.tableWidget.rowCount())[::-1]:  # 逆序删除，正序删除会有一些删除不成功
            self.child.tableWidget.removeRow(rowNum)

    # 动态加载comboBox
    def change_comboBox(self):
        if self.datas is not None:
            times = list(set(self.datas['时间'].str[:10].values))
            self.child.comboBox.addItems(times)

    def refresh(self):
        self.child.comboBox.clear()
        self.child.comboBox.addItem('全部')
        self.remove_tabel()
        self.show_data()

    # 清空表数据
    def clear_tabel(self):
        que_box = QMessageBox.question(self, '警告', '是否清空表', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if que_box == QMessageBox.Yes and self.datas is not None:
            self.remove_tabel()
            con = sqlite3.connect(r'{}'.format(self.database))
            cur = con.cursor()
            t_name = cur.execute("select name from sqlite_master where type='table'").fetchone()[0]
            cur.execute('DELETE from {}'.format(t_name))
            con.commit()
            con.close()
            self.table = []
            self.datas = []
        else:
            pass

    # 导出到excel
    def outPut_excel1(self):
        data = pd.DataFrame(self.table)
        filepath = QFileDialog.getSaveFileName(self, '选择保存路径', './', 'xlsx(*.xlsx)')[0]
        if filepath is not None:
            data.to_excel(r'{}'.format(filepath))

    def outPut_excel(self):
        try:
            dir_path = QFileDialog.getExistingDirectory(None, "请选择文件夹", "D:\\")
            # print(dir_path)

            data = pd.DataFrame(self.table)

            # print(self.database.split('.')[0])

            path = dir_path + '/' + '{}'.format(self.bname) + re.sub(r'[^0-9]', '', datetime.datetime.now().strftime(
                "%Y%m%d%H%M%S")) + '.xlsx'

            with pd.ExcelWriter(path) as writer:
                data.to_excel(writer, sheet_name='号码')
            print(path)

            if self.bname == 'F小组':
                main.print21(['The task is completed'])
                main.print21([str(path)])
            if self.bname == 'F直播':
                main.print22(['The task is completed'])
                main.print22([str(path)])
            if self.bname == 'INS粉丝':
                main.print9(['The task is completed'])
                main.print9([str(path)])
            if self.bname == 'F主页':
                main.print23(['The task is completed'])
                main.print23([str(path)])
            if self.bname == 'INS贴文':
                main.print_tw(['The task is completed'])
                main.print_tw([str(path)])
            if self.bname == 'INS标签':
                main.print_lb(['The task is completed'])
                main.print_lb([str(path)])
        except:
            # mian.print9('Please re-enter')
            pass


class childWindow_daochu3(QWidget, F_diqu.Ui_Form):
    def __init__(self, database, bname):
        self.datas = None
        self.table = None
        self.bname = bname
        self.database = database
        QWidget.__init__(self)
        self.child = F_diqu.Ui_Form()
        self.child.setupUi(self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框
        self.child.tableWidget.setColumnWidth(0, 100)
        self.child.tableWidget.setColumnWidth(1, 50)
        self.child.tableWidget.setColumnWidth(2, 100)
        self.child.tableWidget.setColumnWidth(3, 100)
        self.child.tableWidget.setColumnWidth(4, 150)
        self.child.tableWidget.setColumnWidth(5, 150)
        self.child.tableWidget.setColumnWidth(6, 100)
        self.child.tableWidget.setColumnWidth(7, 50)
        self.child.tableWidget.setColumnWidth(8, 250)
        self.child.tableWidget.setColumnWidth(9, 150)
        self.setFixedSize(1230, 725)
        self.child.tableWidget.setAlternatingRowColors(True)
        self.child.pushButton_4.clicked.connect(self.duplicate_removal)
        self.child.pushButton_5.clicked.connect(self.refresh)
        self.child.pushButton_2.clicked.connect(self.search_data)
        self.child.pushButton_3.clicked.connect(self.clear_tabel)
        self.child.pushButton.clicked.connect(self.outPut_excel)
        self.child.pushButton_6.clicked.connect(self.on_pushButton_6_click)
        self.child.pushButton_7.clicked.connect(self.on_pushButton_7_click)

    def mousePressEvent(self, event):  # 鼠标左键按下时获取鼠标坐标,按下右键取消
        if event.button() == Qt.LeftButton:
            self.m_Position = event.globalPos() - self.pos()
            if self.m_Position.y() < 31:
                self.m_flag = True
                event.accept()
        elif event.button() == Qt.RightButton:
            self.m_flag = False

    def mouseMoveEvent(self, QMouseEvent):  # 鼠标在按下左键的情况下移动时,根据坐标移动界面
        try:
            if Qt.LeftButton and self.m_flag:
                self.move(QMouseEvent.globalPos() - self.m_Position)
                QMouseEvent.accept()
        except:
            pass

    def mouseReleaseEvent(self, QMouseEvent):  # 鼠标按键释放时,取消移动
        self.m_flag = False

    def on_pushButton_6_click(self):
        self.showMinimized()

    def on_pushButton_7_click(self):
        self.close()

    def show_data(self):
        con = sqlite3.connect(r'{}'.format(self.database))
        cur = con.cursor()
        t_name = cur.execute("select name from sqlite_master where type='table'").fetchone()[0]
        cursor = cur.execute('select * from {}'.format(t_name))
        if cursor is not None:
            biao = pd.DataFrame(data=cursor,
                                columns=["用户名", "性别", "工作", "教育", "居中地", "来自", "婚姻", "好友数", "链接",
                                         "时间"])
            con.close()
            self.datas = copy.deepcopy(biao)
            self.table = biao
            self.load_data()
            self.change_comboBox()
        con.close()

    def search_data(self):
        if self.datas is not None:
            current_index = self.child.comboBox.currentIndex()
            time = self.child.comboBox.currentText()
            if current_index != 0:
                self.table = self.datas[self.datas['时间'].str[:10].values == time]
            else:
                self.table = self.datas
            self.remove_tabel()
            self.load_data()

    def load_data(self):
        n = np.array(self.table)
        for i in range(len(n)):
            row_count = self.child.tableWidget.rowCount()
            self.child.tableWidget.insertRow(row_count)
            for j in range(10):
                self.child.tableWidget.setItem(i, j, QTableWidgetItem(str(n[i][j])))
        data_num = self.child.tableWidget.rowCount()
        self.child.label_2.setText(str(data_num))

    def duplicate_removal(self):
        if self.datas is not None:
            self.table = self.table.drop_duplicates(subset=["链接"])
            self.remove_tabel()
            self.load_data()

    def remove_tabel(self):
        for rowNum in range(0, self.child.tableWidget.rowCount())[::-1]:  # 逆序删除，正序删除会有一些删除不成功
            self.child.tableWidget.removeRow(rowNum)

    # 动态加载comboBox
    def change_comboBox(self):
        if self.datas is not None:
            times = list(set(self.datas['时间'].str[:10].values))
            self.child.comboBox.addItems(times)

    def refresh(self):
        self.child.comboBox.clear()
        self.child.comboBox.addItem('全部')
        self.remove_tabel()
        self.show_data()

    # 清空表数据
    def clear_tabel(self):
        que_box = QMessageBox.question(self, '警告', '是否清空表', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if que_box == QMessageBox.Yes and self.datas is not None:
            self.remove_tabel()
            con = sqlite3.connect(r'{}'.format(self.database))
            cur = con.cursor()
            t_name = cur.execute("select name from sqlite_master where type='table'").fetchone()[0]
            cur.execute('DELETE from {}'.format(t_name))
            con.commit()
            con.close()
            self.table = []
            self.datas = []
        else:
            pass

    # 导出到excel
    def outPut_excel1(self):
        data = pd.DataFrame(self.table)
        filepath = QFileDialog.getSaveFileName(self, '选择保存路径', './', 'xlsx(*.xlsx)')[0]
        if filepath is not None:
            data.to_excel(r'{}'.format(filepath))

    def outPut_excel(self):
        try:
            dir_path = QFileDialog.getExistingDirectory(None, "请选择文件夹", "D:\\")

            data = pd.DataFrame(self.table)

            path = dir_path + '/' + '{}'.format(self.bname) + re.sub(r'[^0-9]', '', datetime.datetime.now().strftime(
                "%Y%m%d%H%M%S")) + '.xlsx'

            with pd.ExcelWriter(path) as writer:
                data.to_excel(writer, sheet_name='号码')
            main.print7(['The task is completed'])
            main.print7([str(path)])
        except:
            # mian.print9('Please re-enter')
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(r"images/img_1.ico"))  # 设置界面左上角图标
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

    main = mymainwindow()

    qh = qhwindow()
    dq6 = dq6window()
    pt = ptwindow("全球活跃挖掘")
    gjc = gjcwindow("全球活跃挖掘")
    gjc_215 = gjcwindow("谷歌地图获客")
    pt_54 = ptwindow("公开小组挖掘")
    gjc_55 = gjcwindow("公开小组挖掘")
    gjc_83 = gjcwindow("主页基础挖掘")
    gjc_203 = gjcwindow('小组基础挖掘')
    gjc_227 = gjcwindow('直播基础挖掘')
    gjc_123 = gjcwindow('in指定搜索挖掘')
    xz = xzwindow('小组活跃挖掘')
    xz_231 = xzwindow('小组成员挖掘')

    dc = childWindow_daochu1(r'HKHM.db', ["关键词", "手机号", "时间"])
    dc_218 = childWindow_daochu1(r'HKLBS.db', ["商店名", '手机号', '地址', '链接', '时间'])
    dc_236 = childWindow_daochu1(r'HKXZCY.db', ["平台", "手机号/用户名", "时间"])
    dc_12 = childWindow_daochu2(r'HKHMFB.db', 'F小组')
    dc_93 = childWindow_daochu2(r'HKHMZB.db', 'F直播')
    dc_142 = childWindow_daochu2(r'HKHMINS.db', 'INS粉丝')
    dc_100 = childWindow_daochu2(r'HKHMZY.db', 'F主页')
    dc_107 = childWindow_daochu2(r'FTHFS.db', 'F粉丝')
    dc_121 = childWindow_daochu3(r'HYDQWJ.db', 'F地区')
    dc_135 = childWindow_daochu2(r'INSLIKE.db', 'INS贴文')
    dc_159 = childWindow_daochu2(r'INSLABEL.db', 'INS标签')
    dc_58 = childWindow_daochu1(r"HKGKXZ.db", ["关键词", "链接", "时间"])
    dc_86 = childWindow_daochu1(r'HKFBZY.db', ['用户名','类别','链接','时间'])
    dc_206 = childWindow_daochu1(r'HKFBXZ.db',['小组名','链接','时间'])
    dc_230 = childWindow_daochu1(r'HKFBZB.db',['小组名','链接','时间'])
    dc_149 = childWindow_daochu1(r'INSPAGE.db',['用户名','签名','行业/职业','简介','链接','手机号','时间'])
    dc_128 = childWindow_daochu1(r'INSSEARCH.db',['关键词','用户名','签名','链接','时间'])

    btn_12 = main.pushButton_12
    btn_12.clicked.connect(dc_12.show)
    btn_93 = main.pushButton_93
    btn_93.clicked.connect(dc_93.show)
    btn_142 = main.pushButton_142
    btn_142.clicked.connect(dc_142.show)
    btn_135 = main.pushButton_135
    btn_135.clicked.connect(dc_135.show)

    btn_121 = main.pushButton_121
    btn_121.clicked.connect(dc_121.show)

    btn_107 = main.pushButton_107
    btn_107.clicked.connect(dc_107.show)

    btn_100 = main.pushButton_100
    btn_100.clicked.connect(dc_100.show)

    btn_236 = main.pushButton_236
    btn_236.clicked.connect(dc_236.show)

    btn17 = main.pushButton_17  # 主窗体按钮事件绑定
    btn17.clicked.connect(qh.show)

    btn18 = main.pushButton_18  # 主窗体按钮事件绑定
    btn18.clicked.connect(pt.show)

    btn19 = main.pushButton_19  # 主窗体按钮事件绑定
    btn19.clicked.connect(gjc.show)

    btn215 = main.pushButton_215
    btn215.clicked.connect(gjc_215.show)

    btn213 = main.pushButton_213
    btn213.clicked.connect(dq6.show)

    btn218 = main.pushButton_218
    btn218.clicked.connect(dc_218.show)

    btn159 = main.pushButton_159
    btn159.clicked.connect(dc_159.show)

    btn53 = main.pushButton_53
    btn53.clicked.connect(xz.show)

    btn54 = main.pushButton_54
    btn54.clicked.connect(pt_54.show)

    btn55 = main.pushButton_55
    btn55.clicked.connect(gjc_55.show)

    btn58 = main.pushButton_58
    btn58.clicked.connect(dc_58.show)

    btn231 = main.pushButton_231
    btn231.clicked.connect(xz_231.show)

    btn_83 = main.pushButton_83
    btn_83.clicked.connect(gjc_83.show)

    btn_86 = main.pushButton_86
    btn_86.clicked.connect(dc_86.show)

    btn_203 = main.pushButton_203
    btn_203.clicked.connect(gjc_203.show)

    btn_206 = main.pushButton_206
    btn_206.clicked.connect(dc_206.show)

    btn_227 = main.pushButton_227
    btn_227.clicked.connect(gjc_227.show)

    btn_230 = main.pushButton_230
    btn_230.clicked.connect(dc_230.show)

    btn_149 = main.pushButton_149
    btn_149.clicked.connect(dc_149.show)

    btn_123 = main.pushButton_123
    btn_123.clicked.connect(gjc_123.show)

    btn_128 = main.pushButton_128
    btn_128.clicked.connect(dc_128.show)

    main.pushButton_22.clicked.connect(dc.show)

    main.show()
    sys.exit(app.exec_())
