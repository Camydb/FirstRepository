# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 14:34:46 2023

@author: Administrator
"""

import openai


#%%%%%%%%%%%%%%%%%

news='''
People look at signs posted outside of an entrance to Silicon Valley Bank in Santa Clara, Calif., Friday, March 10, 2023. From winemakers in California to startups across the Atlantic Ocean, companies are scrambling to figure out how to manage their finances after their bank, Silicon Valley Bank, suddenly shut down on Friday. The meltdown means distress not only for businesses but also for all their workers whose paychecks may get tied up in the chaos. (AP Photo/Jeff Chiu)

People look at signs posted outside of an entrance to Silicon Valley Bank in Santa Clara, Calif., Friday, March 10, 2023. From winemakers in California to startups across the Atlantic Ocean, companies are scrambling to figure out how to manage their finances after their bank, Silicon Valley Bank, suddenly shut down on Friday. The meltdown means distress not only for businesses but also for all their workers whose paychecks may get tied up in the chaos. (AP Photo/Jeff Chiu)

NEW YORK (AP) — The U.S. government took extraordinary steps Sunday to stop a potential banking crisis after the historic failure of Silicon Valley Bank, assuring all depositors at the failed institution that they could access all their money quickly, even as another major bank was shut down.

The announcement came amid fears that the factors that caused the Santa Clara, California-based bank to fail could spread. Regulators had worked all weekend to try to find a buyer for the bank, which was the second-largest bank failure in history. Those efforts appeared to have failed Sunday.

In a sign of how fast the financial bleeding was occurring, regulators announced that New York-based Signature Bank had also failed and was being seized on Sunday. At more than $110 billion in assets, Signature Bank is the third-largest bank failure in U.S. history.

The near-financial crisis that U.S. regulators had to intervene to prevent left Asian markets jittery as trading began Monday. Japan’s benchmark Nikkei 225 sank 1.6% in morning trading, Australia’s S&P/ASX 200 lost 0.3% and South Korea’s Kospi shed 0.4%. But Hong Kong’s Hang Seng rose 1.4% and the Shanghai Composite increased 0.3%.

ADVERTISEMENT

In an effort to shore up confidence in the banking system, the Treasury Department, Federal Reserve and FDIC said Sunday that all Silicon Valley Bank clients would be protected and able to access their money. They also announced steps that are intended to protect the bank’s customers and prevent additional bank runs.

“This step will ensure that the U.S. banking system continues to perform its vital roles of protecting deposits and providing access to credit to households and businesses in a manner that promotes strong and sustainable economic growth,” the agencies said in a joint statement.

Under the plan, depositors at Silicon Valley Bank and Signature Bank, including those whose holdings exceed the $250,000 insurance limit, will be able to access their money on Monday.

Also Sunday, another beleaguered bank, First Republic Bank, announced that it had bolstered its financial health by gaining access to funding from the Fed and JPMorgan Chase.

In a separate announcement, the Fed late Sunday announced an expansive emergency lending program that’s intended to prevent a wave of bank runs that would threaten the stability of the banking system and the economy as a whole. Fed officials characterized the program as akin to what central banks have done for decades: Lend freely to the banking system so that customers would be confident that they could access their accounts whenever needed.

ADVERTISEMENT

The lending facility will allow banks that need to raise cash to pay depositors to borrow that money from the Fed, rather than having to sell Treasuries and other securities to raise the money. Silicon Valley Bank had been forced to dump some of its Treasuries at at a loss to fund its customers’ withdrawals. Under the Fed’s new program, banks can post those securities as collateral and borrow from the emergency facility.

ADVERTISEMENT

The Treasury has set aside $25 billion to offset any losses incurred under the Fed’s emergency lending facility. Fed officials said, however, that they do not expect to have to use any of that money, given that the securities posted as collateral have a very low risk of default.

Analysts said the Fed’s program should be enough to calm financial markets on Monday.

“Monday will surely be a stressful day for many in the regional banking sector, but today’s action dramatically reduces the risk of further contagion,” economists at Jefferies, an investment bank, said in a research note.

Though Sunday’s steps marked the most extensive government intervention in the banking system since the 2008 financial crisis, its actions are relatively limited compared with what was done 15 years ago. The two failed banks themselves have not been rescued, and taxpayer money has not been provided to the banks.

President Joe Biden said Sunday evening as he boarded Air Force One back to Washington that he would speak about the bank situation on Monday. In a statement, Biden also said he was “firmly committed to holding those responsible for this mess fully accountable and to continuing our efforts to strengthen oversight and regulation of larger banks so that we are not in this position again.”

ADVERTISEMENT

Regulators had to rush to close Silicon Valley Bank, a financial institution with more than $200 billion in assets, on Friday when it experienced a traditional run on the bank where depositors rushed to withdraw their funds all at once. It is the second-largest bank failure in U.S. history, behind only the 2008 failure of Washington Mutual.

Some prominent Silicon Valley executives feared that if Washington didn’t rescue the failed bank, customers would make runs on other financial institutions in the coming days. Stock prices plunged over the last few days at other banks that cater to technology companies, including First Republic Bank and PacWest Bank.

Among the bank’s customers are a range of companies from California’s wine industry, where many wineries rely on Silicon Valley Bank for loans, and technology startups devoted to combating climate change. Sunrun, which sells and leases solar energy systems, had less than $80 million of cash deposits with Silicon Valley. Stitchfix, the clothing retail website, disclosed recently that it had a credit line of up to $100 million with Silicon Valley Bank and other lenders.

ADVERTISEMENT

Tiffany Dufu, founder and CEO of The Cru, a New York-based career coaching platform and community for women, posted a video Sunday on LinkedIn from an airport bathroom, saying the bank crisis was testing her resiliency . Given that her money was tied up at Silicon Valley Bank, she had to pay her employees out of her personal bank account. With two teenagers to support who will be heading to college, she said she was relieved to hear that the government’s intent is to make depositors whole.

“Small businesses and early-stage startups don’t have a lot of access to leverage in a situation like this, and we’re often in a very vulnerable position, particularly when we have to fight so hard to get the wires into your bank account to begin with, particularly for me, as a Black female founder,” Dufu told The Associated Press.

Silicon Valley Bank began its slide into insolvency when its customers, largely technology companies that needed cash as they struggled to get financing, started withdrawing their deposits. The bank had to sell bonds at a loss to cover the withdrawals, leading to the largest failure of a U.S. financial institution since the height of the financial crisis.

Treasury Secretary Janet Yellen pointed to rising interest rates, which have been increased by the Federal Reserve to combat inflation, as the core problem for Silicon Valley Bank. Many of its assets, such as bonds or mortgage-backed securities, lost market value as rates climbed.

Sheila Bair, who was chairwoman of the FDIC during the 2008 financial crisis, recalled that with nearly all the bank failures then, “we sold a failed bank to a healthy bank. And usually, the healthy acquirer would also cover the uninsured because they wanted the franchise value of those large depositors so optimally, that’s the best outcome.”

But with Silicon Valley Bank, she told NBC’s “Meet the Press,” “this was a liquidity failure, it was a bank run, so they didn’t have time to prepare to market the bank. So they’re having to do that now, and playing catch-up.”

___

Rugaber and Megerian reported from Washington. Sweet and Bussewitz reported from New York.

Associated Press Writers Hope Yen in Washington and Jennifer McDermott in Providence, Rhode Island, contributed to this report.
'''




# import os
import openai


completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
   # model="gpt-4",
  messages=[
    {"role": "user", "content": "Can you help me summarize a piece of news?"},
    {"role": "assistant", "content": "Sure, please provide me with the piece of news you would like me to summarize."},
    {"role": "user", "content": news}
  ]
)

print(completion.choices[0].message.content)

#%%%%%%%%%%%%%%%%%%%%%
print(completion.choices[0].message.content)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai

openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Can you help me summarize a piece of news?"},
        {"role": "assistant", "content": "Sure, I'd be happy to help. Please provide me with the news article or a link to it."},
        {"role": "user", "content": "The Federal Deposit Insurance Corporation (FDIC) is an independent agency created by the Congress to maintain stability and public confidence in the nation's financial system. The FDIC insures deposits; examines and supervises financial institutions for safety, soundness, and consumer protection; makes large and complex financial institutions resolvable; and manages receiverships."}
    ]
)
print(completion.choices[0].message)
# print(completion)

#%%%%%%%%%%%%%%%%%%%%

import openai

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo", 
  messages=[{"role": "user", "content": "Tell the world about the ChatGPT API in the style of a pirate."}]
)

print(completion.choices[0].message)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

import os
import openai



response = openai.Completion.create(
  model="text-davinci-003",
  prompt="I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Unknown\".\n\nQ: What is human life expectancy in the United States?\nA: Human life expectancy in the United States is 78 years.\n\nQ: Who was president of the United States in 1955?\nA: Dwight D. Eisenhower was president of the United States in 1955.\n\nQ: Which party did he belong to?\nA: He belonged to the Republican Party.\n\nQ: What is the square root of banana?\nA: Unknown\n\nQ: How does a telescope work?\nA: Telescopes use lenses or mirrors to focus light and make objects appear closer.\n\nQ: Where were the 1992 Olympics held?\nA: The 1992 Olympics were held in Barcelona, Spain.\n\nQ: How many squigs are in a bonk?\nA: Unknown\n\nQ: Where is the Valley of Kings?\nA:",
  temperature=0,
  max_tokens=100,
  top_p=1,
  frequency_penalty=0.0,
  presence_penalty=0.0,
  stop=["\n"]
)

message = response.choices[0].text

print(message)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import os
import openai



response = openai.Completion.create(
  model="text-davinci-003",
  prompt="Convert my short hand into a first-hand account of the meeting:\n\nTom: Profits up 50%\nJane: New servers are online\nKjel: Need more time to fix software\nJane: Happy to help\nParkman: Beta testing almost done",
  temperature=0,
  max_tokens=64,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)

message = response.choices[0].text

print(message)

#%%%%%%%%%%%%%%%%%%%%%%%%

# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai



response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
)

msg = response['choices'][0]['message']['content']

print(msg)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


NEWS = '''
但是，他们的选择也是有其自身的道理的。他们认为，自己的时间和精力，更应该放在攒钱上，而不是放在自我提升上。因为他们认为，只有攒够了钱，才能够让自己有更多的自由，才能够让自己有更多的选择。总结：近日，“上海30+夫妻用300万提前退休过躺平生活”的词条冲上热搜，引发网友热议。陈女士夫妻俩在失业之后，发现自己有300万的存款，光靠理财每个月就能有1万元的收入，决定提前退休，享受自由。另一对夫妻则是用5年时间攒下100万，他们认为只有攒够了钱，才能够让自己有更多的自由，才能够让自己有更多的选择。这两对夫妻都有自己的“屏蔽力”，他们的选择也是有其自身的道理的。面对这些质疑，汪景从来不在意，也不会为这些评价去打乱自己的计划。他说：“我只是想过一种自己喜欢的生活，不管别人怎么说，我都会坚持自己的想法。”他也深知，自己的选择可能会有风险，但他也不会因此而改变自己的想法。他认为，只要自己能够控制好自己的消费，就能够把自己的财富维持到一定的水平，这样就能够实现自己的“FIRE”梦想。每个人都有自己的生活方式，每个人都有自己的选择。汪景选择了“退休生活”，蔡志忠选择了“隐居”，而亚历克斯霍诺德则选择了“徒手攀岩”。他们都在屏蔽掉无效的社交圈，把自己有限的时间最大化，更好地寻找到自己的价值和热爱。在这个快节奏的社会，我们也应该学会屏蔽掉对自己生活不利的信息，以最好的状态去计划，才能有更多的时间提升自己。
'''

print(len(NEWS))
new = NEWS.split('\n')

print(new[1])


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

###总结说明
import os
import openai



# model_engine = "text-davinci-002"
model_engine = "text-davinci-003"
# model_engine = "gpt-3.5-turbo"


response = openai.Completion.create(
  model=model_engine,
  prompt='''
  事实上，中亚五国跟美国合作，有着诸多难点。首先，中亚五国的政治体制，跟美国的价值观有着很大的冲突，美国政府一直强调民主自由，而中亚五国的政治体制大多是独裁政权，美国政府很难接受。其次，中亚五国的经济发展水平也不高，经济基础薄弱，美国投资者很难承受风险，也不愿意投资。此外，中亚五国的地理位置也不利于美国，距离欧洲很远，运输成本高，美国投资者也不愿意承担这样的成本。最后，中亚五国的政治稳定性也不高，经常发生内部动乱，美国投资者也不愿意把资金投入这样的环境中。总之，中亚五国跟美国合作，存在着诸多难点，美国投资者也不愿意把资金投入这样的环境中，因此，中亚五国跟美国合作的可能性并不大。哈萨克斯坦想要摆脱俄罗斯的影响，需要付出巨大的努力。由于哈萨克斯坦与俄罗斯的经济联系深厚，以及俄罗斯在哈萨克斯坦的投资和武器装备的依赖，使得哈萨克斯坦很难在短时间内实现脱离俄罗斯的目标。因此，哈萨克斯坦最好的选择是保持中立，保持大国平衡，避免被大国牵制。
  ''',
  temperature=0,
  max_tokens=1200,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)

# 获取 ChatGPT 的回复
message = response.choices[0].text

print(message)


#%%%%%%%%%%%%%%%%

###总结说明
import os
import openai


# 设置请求参数
##问答
model_engine = "text-davinci-002"

# proxies = {'http': "http://127.0.0.1:4780",'https': "http://127.0.0.1:4780"}
# proxies = {'http': "http://172.16.2.60:4780",'https': "http://172.16.2.60:4780"}

# openai.proxy = proxies

prompt = "请用‘盛夏’、‘蝉鸣’、‘少年’、‘橘子味汽水’四个词语造句"

completions = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=3000,
    n=2,
    stop=None,
    temperature=0.5)

# 获取 ChatGPT 的回复
message = completions.choices[0].text

print(message)


#%%%%%%%%%%%%%%%%%%%

##二年级翻译



response = openai.Completion.create(
  model="text-davinci-003",
  prompt='''
  
  ''',
  temperature=0.7,
  max_tokens=64,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)


# 获取 ChatGPT 的回复
message = completions.choices[0].text

print(message)


#%%%%%%%%%%%%%%


import openai
def gpt_chat(content):
    """
    输入：含有标题和时间的df
    输出：总结（包含标题，三句话总结等）及新闻背景
    """


    message = [{"role": "system", "content": "You are an experienced news editor and your readers are first-year college students."},
          {"role": "user", "content": """As an experienced news editor, you need to summarize news based on various news outlets' titles and your intended readers are first-year college students. Output three results: 1. News summarized in a few sentences. 2. News summarized into one short news title. 3. Express the central topic in no more than two words. 4. Where the news happened
    Desired Output Format:
    1. Summary: -||-
    2. Title: -||-
    3. Topic: -||-
    4. Location: -||-
    News Input presented in table format:'''{}'''
              """}]
    
    # 输出总结
    message[-1]["content"] = message[-1]["content"].format(content)
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=message,
      temperature = 0
    )
    summary = completion.choices[0].message.content.replace('\n','')

    # 输出新闻背景
    message.append({"role": "assistant", "content": summary})
    message.append({"role": "user", "content": "Please provide background information about this news event that will help readers better understand news stories and keep them informed about current events. "})
    completion = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=message,
          temperature = 0
        )
    context = completion.choices[0].message.content.replace('\n','')

    return summary, context
    
summary, context = gpt_chat(df[["title", "time"]])
print(summary, context, sep = "\n\n")