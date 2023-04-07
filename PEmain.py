# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 15:56:41 2023

@author: Administrator
"""

import time
import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth
from pyppeteer import launcher
import nest_asyncio
nest_asyncio.apply()

async def main():
        if '--enable-automation' in launcher.DEFAULT_ARGS:
            launcher.DEFAULT_ARGS.remove("--enable-automation")
            # userDataDir=r'./fbtext',executablePath='chrome_win64/chrome.exe',
        browser = await launch( headless=False, dumpio=True, autoClose=True,
                                    handleSIGINT=False, 
                                    handleSIGTERM=False, handleSIGHUP=False,
                                    args=['--no-sandbox', '--window-size=1920,1080', '--disable-infobars',
                                          '--log-level=3',
                                          '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'])  # 进入有头模式
        # web = await self.browser.createIncognitoBrowserContext()
        # self.page = await web.newPage()
        page = await browser.newPage()
        await stealth(page)
        # 设置页面视图大小
        await page.setViewport({'width': 1920, 'height': 1080})
        # 是否启用JS，enabled设为False，则无渲染效果
        await page.setJavaScriptEnabled(enabled=True)

        await asyncio.sleep(2)
        url = 'https://new.qq.com/ch/digi/'
        print('一阶段')

        await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
        
        await page.goto(url)
        await asyncio.sleep(2)
        # await page.keyboard.type(KEY)
        await page.keyboard.press('Space')
        
        await asyncio.sleep(20)
        
asyncio.get_event_loop().run_until_complete(main())
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%




# from pyppeteer import launch
# from pyppeteer import launcher
# import asyncio
# import nest_asyncio
# nest_asyncio.apply()

# import pyppeteer

# print(pyppeteer.__chromium_revision__)  # 查看版本号
# print(pyppeteer.executablePath())  # 查看 Chromium 存放路径
# # 588429
# # C:\Users\Administrator\AppData\Local\pyppeteer\pyppeteer\local-chromium\588429\chrome-win32\chrome.exe

import time
import asyncio
from pyppeteer import launch
import nest_asyncio
nest_asyncio.apply()

async def main1():
    browser = await launch(headless=False)  # 关闭无头浏览器
    page = await browser.newPage()
    await page.goto('https://www.baidu.com/')  # 跳转
    await page.screenshot({'path': 'example.png'})  # 截图
    time.sleep(10)
    await browser.close()  # 关闭


asyncio.get_event_loop().run_until_complete(main1())
