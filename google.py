# from multiprocessing import Pool
import re
import time
from datetime import datetime
import openai
import pandas as pd
import pymysql
import requests
import shortuuid
import spacy
from bs4 import BeautifulSoup
from newspaper import Article
from sqlalchemy import create_engine

# HOST="120.48.49.157"
AWS = '''database-1.cwrdah6vau2j.us-east-1.rds.amazonaws.com'''
# token = 't-g20543cGFYKVK4SE343FV4WVIOTEN2P457JJWTLC'

openai.api_key = "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"


def get_CLASS_ID(url):
    # db = pymysql.connect(
    #     host=HOST, 
    #     port=3306,
    #     user='root',    #在这里输入用户名
    #     password='root123321',     #在这里输入密码
    #     charset='utf8mb4' ,
    #     database='GOOGLE'
    #     ) #连接数据库
    # cursor = db.cursor()

    # 创建数据库连接
    db = create_engine('mysql+pymysql://admin:Aa123321@{}:3306/GOOGLE'.format(AWS))

    # 查询数据
    # df = pd.read_sql_query('SELECT * FROM table_name', engine)

    df = pd.read_sql_query('''SELECT THEME_URL,TH_ID FROM GL_NEWS  ''', db)
    # db.close()
    df = df.drop_duplicates('THEME_URL')  # .sort_index()
    urls = list(df['THEME_URL'])
    new_url = url + '&so=1'
    if new_url in urls:
        # print("in")
        result = df.loc[df['THEME_URL'] == new_url, 'TH_ID'].iloc[0]
        print(result)
        return (result)
    else:
        result = shortuuid.ShortUUID().random(length=9)
        print('not in')
        return (result)


def sun_twi_title():
    # db = pymysql.connect(
    #     host=HOST, 
    #     port=3306,
    #     user='root',    #在这里输入用户名
    #     password='root123321',     #在这里输入密码
    #     charset='utf8mb4' ,
    #     database='GOOGLE'
    #     ) #连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    # cursor = db.cursor()
    # 使用pandas的read_sql函数读取数据
    # db = create_engine('mysql+pymysql://root:root123321@{}:3306/GOOGLE'.format(HOST))
    db = create_engine('mysql+pymysql://admin:Aa123321@{}:3306/GOOGLE'.format(AWS))
    df = pd.read_sql_query('''SELECT PINGL FROM Twitter  ''', db)
    # db.close()
    df = df.drop_duplicates('PINGL')  # .sort_index()
    return (list(df["PINGL"]))


def sun_news_title():
    # db = pymysql.connect(
    #     host=HOST, 
    #     port=3306,
    #     user='root',    #在这里输入用户名
    #     password='root123321',     #在这里输入密码
    #     charset='utf8mb4' ,
    #     database='GOOGLE'
    #     ) #连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    # cursor = db.cursor()
    # 使用pandas的read_sql函数读取数据
    # db = create_engine('mysql+pymysql://root:root123321@{}:3306/GOOGLE'.format(HOST))
    db = create_engine('mysql+pymysql://admin:Aa123321@{}:3306/GOOGLE'.format(AWS))

    df = pd.read_sql_query('''SELECT TITLE FROM GL_NEWS  ''', db)
    # db.close()
    df = df.drop_duplicates('TITLE')  # .sort_index()
    return (list(df["TITLE"]))


# print(sun_news_title())

def split_list(list, thread_num):
    list_total = []
    num = thread_num  # 线程数量
    x = len(list) // num  # 将参数进行分批（5批）方便传参
    count = 1  # 计算这是第几个列表
    for i in range(0, len(list), x):
        if count < num:
            list_total.append(list[i:i + x])
            count += 1
        else:
            list_total.append(list[i:])  # 多余的参数全部放在最后一个列表中
            break
    return list_total


def shijian(timeStamp):
    # 转换成localtime
    time_local = time.localtime(timeStamp)
    # 转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt


def gpt_output(df):
    prompt = """As an experienced news editor, you need to summarize news based on various news outlets' titles and your intended readers are first-year college students. Output three results: 1. News summarized in a few sentences. 2. News summarized into one short news title. 3. Express the central topic in no more than two words. 4. Where the news happened
                Desired Output Format:
                1. Summary: -||-
                2. Title: -||-
                3. Topic: -||-
                4. Location: -||-
                News Input presented in table format:'''
                {}
                '''
                """

    prompt = prompt.format(df.to_string())
    result = gpt_title(prompt)

    # 保存
    try:
        summary = re.findall("1\.\ Summary:\ (.*)2\.", result)[0]
    except Exception as e:
        print(e)
        summary = ''

    try:
        title = re.findall("2\.\ Title:\ (.*)3\.", result)[0]
    except Exception as e:
        print(e)
        title = ''

    try:
        topic = re.findall("3\.\ Topic:\ (.*)4\.", result)[0]
    except Exception as e:
        print(e)
        topic = ''

    try:
        location = re.findall("4\.\ Location:\ (.*)$", result)[0]
    except Exception as e:
        print(e)
        location = ''

    return (summary, title, topic, location)


def context(summary):
    """
    输入新闻的三句话总结，输出相关背景知识
    """
    prompt = """ As an experienced news editor, you need to provide explanations for certain ideas in news articles so that middle school students can better understand the news. This will help the students comprehend news stories and keep them informed about current events. Please provide background information for this news:'{}'
    """.format(summary)
    result = gpt_title(prompt)
    return result


# url = 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lkdkxYeEJoRjE4RkNSSU5pYUVpZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1'
def title_sum(url, one_tit, CLASS_ID):
    wbdata = requests.get(url, headers=request_header())
    if wbdata.status_code == 200:
        # data = response.json()
        # 对获取到的文本进行解析
        soup = BeautifulSoup(wbdata.text, 'lxml')
        # print(soup.title.text)
        # 获取文章 内容
        # tx = soup.title.text
        # print(tx)
        # twitter(soup)
        # lj = soup.find_all(attrs={'aria-label':'Full Coverage'})
        js = soup.find_all(attrs={'class': 'xrnccd'})
        # uurl = js.find_all(attrs={'class':'VDXfz'})
        # news = 'Help me summarize all the news headlines in three sentences.\n\n'

        # key_word = "Help me extract one keyword.\n\n"

        df = pd.DataFrame(columns=['title', 'TIME'])
        for j in js:
            try:
                title = j.h3.text
                # new_url = 'https://news.google.com/'+j.a['href'][2:]
                new_time = j.time['datetime']
                print(title)
                # print(new_url)
                print(new_time)
                # news = news + '\n' + title
                # key_word = key_word + '\n' + title
                # jurl = j.find(attrs={'class':'ipQwMb ekueJc RD0gLb'})
                # # surl = 'https://news.google.com/'+uu['href'][2:]
                # j_title = jurl.text
                # j_url = 'https://news.google.com/'+jurl['href'][2:]

                # df = pd.DataFrame(columns=['title', 'TIME'])
                # for row in cur.execute('SELECT NEWS_ID,TITLE,TIME FROM GL_NEWS where TH_ID = "{}" '.format(th_id) ):
                # df = df.append({'title': row[1], 'TIME': row[2]}, ignore_index=True)
                df = pd.concat([df, pd.DataFrame({'title': [title], 'TIME': [new_time]})], ignore_index=True)

                # print(j_title)
                # print(j_url)
                # get_news(surl,tx)
                # time.sleep(3)
                # print(uu.href)
            except Exception as e:
                # logging.error(e, exc_info=True)
                print(e)
            print('-----------------')
        # summary,title,topic,location
        two, one_title, three, location = gpt_output(df)
        print(two, title, three, location)

        context1 = context(two)
        img_url = ai_img(two)
        context2 = deepl(context1)
        CT_ID = shortuuid.ShortUUID().random(length=8)

        print(img_url)

        context1 = context1.replace("\"", "\'")
        context2 = context2.replace("\"", "\'")
        # three = gpt_title(key_word)
        # print(two)
        # print(three)
        TH_ZH = deepl(one_title).replace("\"", "\'")
        KW_ZH = deepl(three).replace("\"", "\'")
        GT_ZH = deepl(two).replace("\"", "\'")

        if TH_ZH.startswith("“") and TH_ZH.endswith("”"):
            # Remove the quotation marks using string slicing
            TH_ZH = TH_ZH[1:-1]

        if TH_ZH.startswith("'") and TH_ZH.endswith("'"):
            # Remove the quotation marks using string slicing
            TH_ZH = TH_ZH[1:-1]

        if TH_ZH[-1] == "。":
            TH_ZH = TH_ZH[:-1]
        elif TH_ZH[-2] == "。":
            TH_ZH = TH_ZH[:-2] + TH_ZH[-1]

        # print(gpt_translate(th))
        print('-----------------')
        # TH_ID = shortuuid.ShortUUID().random(length=9)

        for j in js:
            try:
                title = j.h3.text
                new_url = 'https://news.google.com/' + j.a['href'][2:]
                new_time = j.time['datetime']
                # print(title)
                print(new_url)
                print(new_time)

                img = j.img['src']
                print(img)

                img_name = j.img['alt']
                print(img_name)

                # jurl = j.find(attrs={'class':'ipQwMb ekueJc RD0gLb'})
                # # surl = 'https://news.google.com/'+uu['href'][2:]
                # j_title = jurl.text
                # j_url = 'https://news.google.com/'+jurl['href'][2:]
                # print(j_title)
                # print(j_url)
                get_news(title, new_url, new_time, two, one_title, url, three, location, CLASS_ID, context1, context2,
                         img_url, TH_ZH, KW_ZH, GT_ZH, CT_ID, img, img_name)
                # time.sleep(3)
                # print(uu.href)
            except Exception as e:
                print(e)
            print('-----------------')
    return 0


def gpt_title(text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            # {"role": "user", "content": "Can you help me summarize a piece of news?"},
            # {"role": "assistant", "content": "Sure, please provide me with the piece of news you would like me to summarize."},
            {"role": "user", "content": text}
        ]
    )

    # print(completion.choices[0].message.content)
    return (completion.choices[0].message.content.replace('\n\n', '\n'))


def gpt_sum(title, timet, content):
    prompt = '''Task: Summarize the news article "{}" published on {}. Provide details about this news. 
    Here is the whole article:
    """
    {}
    """
    '''.format(title, timet, content)
    # print(gpt_title(prompt))
    return (gpt_title(prompt))

    # completion = openai.ChatCompletion.create(
    #   model="gpt-3.5-turbo",
    #   messages=[
    #     {"role": "user", "content": "Task: Extract 5 key points from this news article.\n\n News: {}".format(text)}
    #     # {"role": "assistant", "content": "Sure, please provide me with the piece of news you would like me to summarize."},
    #     # {"role": "user", "content": text}
    #   ]
    # )

    # # print(completion.choices[0].message.content)
    # return(completion.choices[0].message.content.strip("\n").replace("\n\n","\n"))


def request_header():
    headers = {
        # 'User-Agent': UserAgent().random ,#常见浏览器的请求头伪装（如：火狐,谷歌）
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        # 'User-Agent': UserAgent().Chrome #谷歌浏览器
    }
    return headers


def get_token():
    url = 'https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal'
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = {"app_id": "cli_a49073a33638100a", "app_secret": "b4zYuiq7HPT5Ly1OACGwGzQROKmZU1Li"}
    response = requests.post(url, headers=headers, json=data)
    print('get_token')
    return (response.json()["tenant_access_token"])


def deepl(text):
    try:
        prompt = '''Translate this from English to Chinese: "{}" '''.format(text)
        return (gpt_title(prompt))
        # url = 'https://api-free.deepl.com/v2/translate'
        # auth_key = 'df628d3e-e50e-be55-6ad3-a43df1fbf411:fx'
        # # text = 'Hello, world!'
        # target_lang = 'ZH'

        # payload = {'text': text, 'target_lang': target_lang}
        # headers = {'Authorization': f'DeepL-Auth-Key {auth_key}'}

        # response = requests.post(url, data=payload, headers=headers)

        # # print(response.json()['translations'][0]['text'])
        # return(response.json()['translations'][0]['text'])
    except Exception as e:
        print(e)
        return text


def ai_img(article):
    try:
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(article)

        # iterate over each entity in the document
        for ent in doc.ents:
            # if the entity is a location, remove it from the text
            if ent.label_ == 'GPE':
                article = article.replace(ent.text, 'it')
            # if the entity is a person, remove it from the text
            if ent.label_ == 'PERSON':
                article = article.replace(ent.text, 'someone')
        response = openai.Image.create(
            prompt=article,
            n=1,
            size="512x512"
        )
        image_url = response['data'][0]['url']
        # print(image_url)
        name2 = image_url.split('?')[0].split('/')[-1]
        print(name2)
        response = requests.get(image_url)
        # path2 = "D:/WS8801/img/"+name2
        path2 = "/home/ubuntu/img/" + name2
        with open(path2, 'wb') as f:
            f.write(response.content)

        url = 'http://120.48.49.157:5000/chuan?name={}'.format(name2)
        files = {'file': open(path2, 'rb')}
        response = requests.get(url, files=files)
        print(response.text)

        return (name2)
    except Exception as e:
        print("Error:", e)
        return ('')


# =============================================================================
# def lark(text):
#     global token
#     url = 'https://open.larksuite.com/open-apis/translation/v1/text/translate'
#     # headers = {'Authorization': 'Bearer t-g2053n6c7EF4YVHPSO3QWKJ5CWD6ULMUE3ZSKENR', 'Content-Type': 'application/json; charset=utf-8'}
#     headers = {'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json; charset=utf-8'}
#     data = {
#         "source_language": "en",
#         "text": ''' {} '''.format(text),
#         "target_language": "zh",
#         "glossary": [
#             {
#                 "from": "Lark",
#                 "to": "Lark"
#             }
#         ]
#     }
#     try:
#         response = requests.post(url, headers=headers, json=data)
#         if response.status_code==200:
#             print(response.status_code)
#             return(response.json()['data']['text'])
#         else:
#             token = get_token()
#             time.sleep(1)
#             return(text)
#     
#     except Exception as e:
#         print(e)
#         print('重新请求')
#         token = get_token()
#         print(token)
#         # print(response.text)
#         # print(text)
#         # time.sleep(1)
#         return(text)
# =============================================================================

def save(db, TITLE, AUTHOR, CONTENT, TIME, THEME, THEME_URL, GPT3_TITLE, GPT3_TEXT, NEWS_URL, PIC_URL, REMARKS, three,
         TH_ID, context1, context2, img_url, TH_ZH, KW_ZH, GT_ZH, CT_ID, img, img_name):
    # conn = sqlite3.connect(db)
    # print(db)
    SAVE_TIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    NEWS_ID = shortuuid.uuid()

    date1 = datetime.strptime(str(TIME), "%Y-%m-%dT%H:%M:%SZ")
    s_t = time.strptime(str(date1), "%Y-%m-%d %H:%M:%S")
    S_TIME = int(time.mktime(s_t))

    try:
        print("开始存储")
        conn = pymysql.connect(
            host=AWS,
            port=3306,
            user='admin',  # 在这里输入用户名
            password='Aa123321',  # 在这里输入密码
            # charset='utf8mb4' ,
            database='GOOGLE'
        )  # 连接数据库
        cur = conn.cursor()

        # TH_ZH = deepl(THEME)
        # KW_ZH = deepl(three)
        # GT_ZH = deepl(GPT3_TITLE)

        ZH_CN = deepl(GPT3_TEXT).replace("\"", "\'")
        T_ZH = deepl(TITLE).replace("\"", "\'")

        if T_ZH.startswith("“") and T_ZH.endswith("”"):
            # Remove the quotation marks using string slicing
            T_ZH = T_ZH[1:-1]

        if T_ZH.startswith("'") and T_ZH.endswith("'"):
            # Remove the quotation marks using string slicing
            T_ZH = T_ZH[1:-1]

        if T_ZH[-1] == "。":
            T_ZH = T_ZH[:-1]
        elif T_ZH[-2] == "。":
            T_ZH = T_ZH[:-2] + T_ZH[-1]

        print("翻译完成")
        # T_ZH,TH_ZH,KW_ZH,GT_ZH,ZH_CN
        sensitive = str(TITLE + THEME + three + GPT3_TITLE + GPT3_TEXT + REMARKS).lower()
        if "china" in sensitive or "taiwan" in sensitive or "jinping" in sensitive:
            print("敏感数据")
            pass
        else:
            cur.execute(
                '''INSERT INTO GL_NEWS (NEWS_ID,TITLE,AUTHOR,CONTENT,TIME,S_TIME,SAVE_TIME,THEME,KEY_WORD,THEME_URL,GPT3_TITLE,GPT3_TEXT,NEWS_URL,PIC_URL,REMARKS,TH_ID,T_ZH,TH_ZH,KW_ZH,GT_ZH,ZH_CN,context,context_ZH,AI_img,CT_ID,img,img_name) 
                VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'''.format(
                    NEWS_ID, TITLE, AUTHOR, CONTENT, TIME, S_TIME, SAVE_TIME, THEME, three, THEME_URL, GPT3_TITLE,
                    GPT3_TEXT, NEWS_URL, PIC_URL, REMARKS, TH_ID, T_ZH, TH_ZH, KW_ZH, GT_ZH, ZH_CN, context1, context2,
                    img_url, CT_ID, img, img_name));
            conn.commit()
            print("记录插入成功!")

        # try:
        #     cur.execute('''UPDATE GL_NEWS SET T_ZH = ?,TH_ZH = ?,KW_ZH = ?,GT_ZH = ?,ZH_CN = ? WHERE NEWS_ID = ?''', (T_ZH,TH_ZH,KW_ZH,GT_ZH,ZH_CN,NEWS_ID))
        #     conn.commit()
        # except Exception as e:
        #     conn.rollback()
        #     print(e)


    except Exception as e:
        conn.rollback()
        print(e)
    conn.close()


def get_news(title, news_url, new_time, two, one_tit, one_url, three, location, TH_ID, context1, context2, img_url,
             TH_ZH, KW_ZH, GT_ZH, CT_ID, img, img_name):
    # get_news(title,new_url,new_time,two,one_tit)
    # 目标新闻网址
    # goo = 'https://news.google.com/articles/CBMiUWh0dHBzOi8vd3d3LmNic25ld3MuY29tL25ld3Mvc2lsaWNvbi12YWxsZXktYmFuay1mYWlsdXJlLXdvcmxkd2lkZS1yZXBlcmN1c3Npb25zL9IBVWh0dHBzOi8vd3d3LmNic25ld3MuY29tL2FtcC9uZXdzL3NpbGljb24tdmFsbGV5LWJhbmstZmFpbHVyZS13b3JsZHdpZGUtcmVwZXJjdXNzaW9ucy8?hl=en-US&amp;gl=US&amp;ceid=US%3Aen'
    # url = 'https://www.cbsnews.com/news/silicon-valley-bank-failure-worldwide-repercussions/'
    # url = 'https://www.nytimes.com/2023/03/12/business/janet-yellen-silicon-valley-bank.html'
    # url = 'https://www.cnn.com/2023/03/13/investing/svb-panic-china-companies-tycoons-intl-hnk/index.html'
    # url = 'https://apnews.com/article/silicon-valley-bank-bailout-yellen-deposits-failure-94f2185742981daf337c4691bbb9ec1e'
    # url = 'https://www.fdic.gov/news/press-releases/2023/pr23016.html'
    news = Article(news_url, language='en')
    news.download()  # 加载网页
    news.parse()  # 解析网页
    # print('题目：',news.title)       # 新闻题目
    # print('正文：\n',news.text)      # 正文内容
    # print(news.publish_date) # 发布日期
    news_text = news.text.replace("\"", "\'")
    news_title = title.replace("\"", "\'")

    one_tit = one_tit.replace("\"", "\'")
    two = two.replace("\"", "\'")
    three = three.replace("\"", "\'")
    location = location.replace("\"", "\'")

    # news_text = escape_string(news_text)
    # news_title = escape_string(news_title)

    # news_authors = news.authors.replace("\"","\'")
    sql_title = sun_news_title()
    if news_title not in sql_title:

        gpt_text = gpt_sum(news_title, new_time, news_text)
        gpt_text = gpt_text.replace("\"", "\'")

        # Check if the title starts and ends with quotation marks
        if news_title.startswith("'") and news_title.endswith("'"):
            # Remove the quotation marks using string slicing
            news_title = news_title[1:-1]

        # gpt_text = ''
        if news_text != '' and 'cookie' not in news_text.lower():
            try:
                save("D:/T_py/GOOGLE.db", news_title, news.authors, news_text, new_time, one_tit, one_url, two,
                     gpt_text, news_url, news.top_image, location, three, TH_ID, context1, context2, img_url, TH_ZH,
                     KW_ZH, GT_ZH, CT_ID, img, img_name)
                # save(               db,TITLE,     AUTHOR,      CONTENT,  TIME,    THEME,  THEME_URL,GPT3_TITLE,GPT3_TEXT,NEWS_URL,PIC_URL,REMARKS)
            except Exception as e:
                print(e)
        else:
            print('no news')
            pass
    else:
        print("重复新闻")


def twitter(url):
    CLASS_ID = get_CLASS_ID(url)
    wbdata = requests.get(url, headers=request_header())
    if wbdata.status_code == 200:
        soup = BeautifulSoup(wbdata.text, 'lxml')
        # print(soup.title.text)
        # 获取文章 内容
        # tx = soup.title.text
        # print(tx)
        # twitter(soup)

        title = soup.title.text
        artical = soup.find_all(attrs={'class': 'ifw3f'})
        for para in artical:
            fu = para.parent

            di = fu.find(attrs={'class': 'js5zDf'})
            print(di.text)

            print(para.text)
            pt = para.text.replace("\"", "\'")

            # xiong = fu.find(attrs={'class':'eGzQsf'})
            # tm = xiong.time.text
            # if len(tm)<9:
            #     now = datetime.datetime.now().strftime('%m/%d/23')
            #     tm = now+' '+tm
            # print(tm)

            date = str(fu.time['datetime'])
            tm = shijian(int(date[:-3]))
            print(tm)

            # conn = sqlite3.connect("D:/T_py/GOOGLE.db")
            # print(db)
            stime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # cursor = conn.cursor()
            # ZH_CN = lark(pt).replace("\"","\'")
            # P_ZH = lark(di.text).replace("\"","\'")

            twi_title = sun_twi_title()
            conn = pymysql.connect(
                host=AWS,
                port=3306,
                user='amin',  # 在这里输入用户名
                password='Aa123321',  # 在这里输入密码
                # charset='utf8mb4' ,
                database='GOOGLE'
            )  # 连接数据库
            cur = conn.cursor()

            print("++++++++++++++")
            print(pt)
            print("++++++++++++++")
            if pt not in twi_title:
                try:
                    ZH_CN = deepl(pt).replace("\"", "\'")
                    P_ZH = deepl(di.text).replace("\"", "\'")

                    cur.execute(
                        '''INSERT INTO Twitter (PINGL,ZH_CN,PEOPLE,P_ZH,TIME,BJ_TIME,S_TIME,CLASS,CLASS_URL,CLASS_ID) VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'''.format(
                            pt, ZH_CN, di.text, P_ZH, tm, stime, date[:-3], title, url, CLASS_ID));
                    conn.commit()
                    print("记录插入成功!")
                except Exception as e:
                    conn.rollback()
                    print(e)
            else:
                print("评论重复")
                pass
            conn.close()
            print('-----------------')
        return (title, CLASS_ID)


# so = 'https://news.google.com/stories/CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2lVdjZQX0JoSERzdzZ4bmJLeVJTZ0FQAQ?hl=en-US&gl=US&ceid=US%3Aen&so=1'
# one_tit = "E3 2023 canceled"
# title_sum(so,one_tit)


if __name__ == "__main__":
    url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen'
    # url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen'
    print('OK')
    while True:
        urls = []
        wbdata = requests.get(url, headers=request_header())
        if wbdata.status_code == 200:
            # data = response.json()
            # 对获取到的文本进行解析
            soup = BeautifulSoup(wbdata.text, 'lxml')
            # print(soup.title.text)
            # 获取文章 内容
            # tx = soup.title.text
            # print(tx)
            # twitter(soup)

            lj = soup.find_all(attrs={'aria-label': 'Full Coverage'})

            # js = soup.find(attrs={'jsname':'gKDw6b'})
            # uurl = js.find_all(attrs={'class':'VDXfz'})
            for uu in lj:
                try:
                    surl = 'https://news.google.com/' + uu['href'][2:]
                    # print(surl)
                    # get_news(surl,tx)
                    one_tit, CLASS_ID = twitter(surl)
                    print(one_tit)

                    so = surl + '&so=1'
                    urls.append(so)
                    # time.sleep(3)
                    # print(so)
                    print('-+-+-+-+-+-+-+-+-+-+-+')
                    title_sum(so, one_tit, CLASS_ID)
                    # print('-+-+-+-+-+-+-+-+-+-+-+')
                except Exception as e:
                    print(e)
                print('-----------------')

        print(urls)
        print(len(urls))
