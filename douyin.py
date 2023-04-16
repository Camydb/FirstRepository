# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 01:22:55 2023

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
import time
from collections import deque
from selenium.webdriver import ChromeOptions
import requests
from selenium import webdriver
# author :香菜
# 下载视频
def downVideo(url,title):
    r = requests.get(url)
    filepath = 'video/' + title + '.mp4'
    with open(filepath, 'wb') as fp:
        fp.write(r.content)
    print('%s已下载' % title)
# 主函数
if __name__ == '__main__':
    # 实例化对象
    option = ChromeOptions()
    # option.add_experimental_option('excludeSwitches',['enable-automation'])# 开启实验性功能
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    # chrome_options = Options()
    # chrome_options.add_argument('--Headless')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument(
    #     'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"')
    # 下载的驱动的地址
    driver = webdriver.Chrome(options=option)
    driver.get('https://www.douyin.com/user/MS4wLjABAAAAvOU5GclmETa4jehXAEspnMfYJQZAbwcJzfUFhZk4cP8')
    #选择网页元素
    # 防止滑动完之后能渠道之前的视频，做了一个已访问集合
    hasVisit = set()
    urlList = driver.find_elements(By.XPATH, value='//*[@id="root"]/div/div[2]/div/div[4]/div[1]/div[2]/ul/li/a/div/div[1]/img')

    # 因为使用了selenium ,导致网页识别到是爬虫，总会出现验证码，我手动点一下，待解决
    time.sleep(10)
    i = 0
    ph = driver.window_handles[0]
    # 我选择一个队列，因为有下拉的动作
    dq = deque(urlList)
    while True:
        urlEl = dq.pop()
        if urlEl is None:
            break
        if urlEl in hasVisit:
            continue
        hasVisit.add(urlEl)
        # 点击主页的视频，进入子界面
        urlEl.click()
        # 取出新打开的句柄，切换当前页面到详情页
        detailHandle = driver.window_handles.pop()
        driver.switch_to.window(detailHandle)
        # 获取视频的标签
        video = driver.find_element(By.XPATH, value='//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div[1]/div[2]/video')
        # 终于取到视频的真实地址
        videoUrl = video.get_attribute("src")
        # 下载视频
        downVideo(videoUrl,str(i))
        # 关闭当前页面
        driver.close()
        i = i + 1
        # 回到主页
        driver.switch_to.window(ph)
        # 每下载三个视频，将主页往下滚动311 像素，这个不精确，待解决
        if i%3 == 0:
            y = i//3*311
            sc = 'window.scrollBy(0,' + str(y)+')'
            driver.execute_script(sc)
            # 将滑动之后的新的标签加入到队列待访问
            urlListNew = driver.find_elements(By.XPATH, value='//*[@id="root"]/div/div[2]/div/div[4]/div[1]/div[2]/ul/li/a/div/div[1]/img')
            for s in urlListNew:
                if s not in hasVisit:
                    dq.append(s)