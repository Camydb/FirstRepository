# Social Media & News Aggregation Toolkit

一个集成了新闻聚合、社交媒体数据采集、AI 摘要生成和 API 服务的 Python 工具集。

## 项目概述

本项目包含多个模块，用于从 Google News、Twitter/X、Facebook、Instagram、抖音等平台采集数据，并通过 OpenAI GPT 进行新闻摘要、翻译和 AI 配图生成，最终通过 Flask API 对外提供服务。

## 项目结构

```
├── main.py                 # PyQt5 桌面 GUI 主程序（社交媒体数据采集客户端）
├── google.py               # Google News 爬虫 + GPT 摘要 + 数据入库
├── g_news.py               # Google News Flask API 服务
├── sql_api.py              # 核心 REST API 服务（新闻/用户/评论/收藏等）
├── api_app.py              # Flask Web 应用（新闻展示页面）
├── Flask_socketIO.py       # WebSocket 实时推送服务
├── sock_sql.py             # 数据库批量翻译/更新脚本
├── twitter.py              # Twitter/X 数据采集（Selenium）
├── twitter_API.py          # Twitter API 凭证（已废弃）
├── douyin.py               # 抖音视频下载（Selenium）
├── chatGPT.py              # OpenAI API 调用示例
├── ChatGPT_news.py         # GPT 新闻摘要 + DeepL 翻译示例
├── alibaba.py              # 阿里巴巴相关脚本
├── cred.py                 # 数据库连接配置（⚠️ 含敏感信息）
├── dbconnect.py            # 数据库连接工具
├── db_check.py             # 数据库检查脚本
├── langchina.py            # LangChain 相关实验
├── Py_spacy.py             # spaCy NLP 处理
├── send_img.py             # 图片上传工具
├── webs.py                 # Web 相关工具
├── Websocket.py            # WebSocket 客户端
├── test_sck.py             # Socket 测试
├── mp.py                   # 多进程工具
├── PEmain.py               # PE 相关主程序
├── SCmain.py               # SC 相关主程序
├── SVBmain.py              # SVB 相关主程序
├── gl_test.py              # 测试脚本
├── api_test.py             # API 测试脚本
├── yan.txt                 # 验证码图片 URL 列表
├── GOOGLE.db               # SQLite 本地数据库
├── lx_API/                 # API 服务部署版本
│   ├── main.py             # Flask API 入口
│   ├── api_app.py          # Web 应用
│   ├── sql_api.py          # REST API
│   ├── google.py           # 新闻爬虫
│   ├── g_news.py           # 新闻 API
│   ├── Flask_socketIO.py   # WebSocket 服务
│   ├── sock_sql.py         # 数据库脚本
│   ├── templates/          # HTML 模板
│   └── b0323/              # 备份版本（2023.03.23）
└── notebooks/              # 笔记本/数据文件
```

## 核心功能

### 1. Google News 聚合 (`google.py`)
- 抓取 Google News 话题页面的新闻标题和链接
- 使用 GPT-3.5 生成新闻摘要、提取关键词、判断地点
- 使用 GPT 翻译为中文
- 使用 DALL·E 生成 AI 配图
- 数据存入 MySQL (AWS RDS)

### 2. 社交媒体采集 (`main.py`)
- **Facebook**: 群组成员、主页粉丝、直播观众采集
- **Instagram**: 粉丝列表采集
- 基于 PyQt5 的桌面 GUI
- 使用 Pyppeteer 进行浏览器自动化
- Cookie 持久化登录

### 3. Twitter/X 采集 (`twitter.py`)
- 基于关键词搜索推文
- 采集推文内容、互动数据（转发/点赞/评论/浏览）
- 使用 Selenium 进行页面渲染
- 数据存入 SQLite

### 4. REST API 服务 (`sql_api.py`)
- 新闻列表/详情接口
- 用户注册/登录/个人信息管理
- 收藏/点赞/评论/分享功能
- 图片上传/获取
- 版本检查

### 5. WebSocket 推送 (`Flask_socketIO.py`)
- 基于 Flask-SocketIO 的实时消息推送
- 支持定时推送

## 技术栈

- **后端**: Flask, Flask-SocketIO, SQLAlchemy, PyMySQL
- **爬虫**: Requests, BeautifulSoup, Selenium, Pyppeteer
- **AI**: OpenAI GPT-3.5, DALL·E, spaCy
- **数据库**: MySQL (AWS RDS), SQLite
- **桌面 GUI**: PyQt5
- **翻译**: DeepL API, Lark/飞书翻译 API
- **其他**: Pandas, newspaper3k, shortuuid

## 环境要求

- Python 3.8+
- Chrome 浏览器（用于 Selenium/Pyppeteer）

## 安装依赖

```bash
pip install flask flask-socketio flask-mysqldb
pip install openai requests beautifulsoup4 lxml
pip install selenium pyppeteer pyppeteer-stealth
pip install PyQt5 pandas openpyxl numpy
pip install pymysql sqlalchemy shortuuid
pip install newspaper3k spacy pillow
pip install fake-useragent nest-asyncio loguru pyautogui
```

## 配置

1. 在 `cred.py` 中配置数据库连接信息
2. 在相关脚本中配置 OpenAI API Key
3. 准备 Chrome 浏览器可执行文件（`chrome_win64/chrome.exe`）

## 运行

```bash
# 启动 REST API 服务
python sql_api.py

# 启动 Web 应用
python api_app.py

# 启动 WebSocket 服务
python Flask_socketIO.py

# 启动桌面 GUI
python main.py

# 运行新闻采集
python google.py
```

## ⚠️ 注意事项

- 本项目为个人学习/实验项目，代码风格较为随意
- 部分 API Key 和数据库凭证已硬编码在代码中（已失效），生产环境请使用环境变量
- 社交媒体采集功能需遵守各平台的使用条款
- `lx_API/` 目录为服务器部署版本，`b0323/` 为历史备份

## License

MIT
