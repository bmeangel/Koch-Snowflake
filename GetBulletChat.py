from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
import datetime

#设置请求头
headers={
    "User-Agent":"",
    "Connection": "keep-alive",
    # 这个cookie的获取方法在文档中已说明（开发者模式）
    "Cookie":""
}
sets=124  # 最新一期的数字

dates=[]  # 日期数组，用于填充url
# 遍历日期  包括begin和end的日期  生成类似2020-05-03的格式的日期
begin = datetime.date(2020,5,3) #设置开始日期
end = datetime.date(2020,6,9)   #设置结束日期
d = begin
delta = datetime.timedelta(days=1) #设置时间差为一天
while d <= end:
    dates.append(str(d.strftime("%Y-%m-%d"))) #把格式化的日期存入列表中
    d += delta #日期加一天
'''
通过以上操作，把2020-05-03到2020-06-09之间的日期都放到了列表中
'''

Cids=[]  # Cid数组，用于填充url
with open('Urls/Cid.txt', 'r') as f: #打开存储Cid的文件
    for line in f.readlines(): #逐行读取文件并生成一个列表，遍历列表元素，得到Cid
        Cids.append(line.strip()) #把每一行Cid放到列表中,strip()用于去除首尾空格

for cid in Cids:
    # 每次都要重置这些数据
    dm_data = []  # 弹幕数据
    dm_text = []  # 弹幕本体
    # 弹幕的八个参数和弹幕本体
    DM_time = [] #1.弹幕在视频中出现的时间，以s为单位
    DM_mode = [] #2.弹幕的模式（滚动、顶端、底端等）
    DM_font = [] #3.弹幕的字体
    DM_color = [] #4.弹幕的颜色编号
    DM_realTime = [] #5.时间戳
    DM_pool = [] #6.弹幕池的编号
    DM_userID = [] #7.发送者的ID
    DM_id = [] #8.数据库ID
    DM_text = [] #弹幕文本
    print("正在爬取第" + str(sets) + "期的《睡前消息》弹幕...")
    for date in dates:
        #获取存储弹幕的网址（讲一下查看弹幕API的方法）
        url="https://api.bilibili.com/x/v2/dm/history?type=1&oid="+cid+"&date="+date
        html=requests.get(url=url,headers=headers) #返回文本信息
        html.encoding='utf8'
        soup=BeautifulSoup(html.text,'lxml') #建立soup对象

        all=soup.find_all("d") #获取网页上的所有文本
        for d in all: #遍历网页文本
            # 弹幕数据（获取弹幕的八个参数）
            dm_data.append(str(d.get("p")).split(","))
            # 弹幕本体（获取弹幕文本）
            dm_text.append(d.get_text())

    # 分别把数据存进这几个数组
    for i in dm_data: #分别把各个参数存入各自对应的列表
        DM_time.append(i[0])
        DM_mode.append(i[1])
        DM_font.append(i[2])
        DM_color.append(i[3])
        DM_realTime.append(i[4])
        DM_pool.append(i[5])
        DM_userID.append(i[6])
        DM_id.append(i[7])
    for i in dm_text: #把弹幕文本存到列表
        DM_text.append(i)
#建立一个字典，把所有元素名称及元素（组成键值对）存到字典里
    dt={"DM_time":DM_time,"DM_mode":DM_mode,"DM_font":DM_font,"DM_color":DM_color,
        "DM_realTime":DM_realTime,"DM_pool":DM_pool,"DM_userID":DM_userID,"DM_id":DM_id,"DM_text":DM_text}

    d=pd.DataFrame(dt) #通过Pandas的DataFrame数据结构，从字典创建一个类似于Excel的二维表

    d.to_csv('./Danmu/Danmu-'+str(sets)+'.csv',encoding='utf-8-sig') #生成CSV文件，存储弹幕信息
    print("已将弹幕放入到Danmu-"+str(sets)+".csv文件中")
    sets-=1

    # 每抓完一个网页休眠7秒
    print("缓冲中...")
    time.sleep(7)

print("已将《睡前消息》第110-124期的弹幕爬取完毕")







