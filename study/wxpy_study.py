#!/usr/bin/env python
# -*- coding: utf-8 -*-


from threading import Timer
from wxpy import *
import requests

#机器人
bot = Bot(cache_path=True)

def get_news():
    url = "http://open.cicba.com/dsapi/"
    r = requests.get(url)
    content = r.json()['content']
    note = r.json()['note']
    return content,note

def send_news(str):
    try:
        contents = ['已实现自动发送！！！',2,3]
        #好友列表  备注显示
        #print(bot.friends())
        print(bot.friends().search(u'信息通知群'))
        all_group = bot.groups().search('信息通知群')



        # 微信昵称，不是账号
        my_friend = bot.friends().search(u'信息通知群')[0]
        #发送
        my_friend.send(contents[0])
        #发送图片
        #my_friend.send_image("C:\\Users\\Administrator.000\\Desktop\\intiloading.png")
        # 发送视频
        #my_friend.send_video('my_video.mov')
        # 发送文件
        #my_friend.send_file('my_file.zip')
        # 以动态的方式发送图片   没啥用
        # my_friend.send('@img@C:\\Users\\Administrator.000\\Desktop\\intiloading.png')
        # t = Timer(86400,send_news("kaishi"))
        # t.start()

        print(bot.groups)#<bound method Bot.groups of <Bot: 灵魂攻城狮>>
        #bot对象里含有chats，friends，groups，mps等方法，分别可以获取当前机器人的聊天对象、好友、群聊、公众号等信息
        all_group = bot.groups()
        print("type all:",type(all_group))
        print(all_group)  #[<Group: 兑换狂人软件开发内部交流群>, <Group: 自足智能科技，百事通>]
        for i in all_group:
            Group = str(i)
            group = Group.replace("<Group: ","").replace(">","")
            #send=bot.groups().search(group)[0].send_image("1.jpg")
            print(Group)
            print(group)
            # print(send)

        #不能发给自己会报错
        # my = bot.friends().search(u'灵魂攻城狮')[0]
        # my.send("发送")
    except :
        my = bot.friends().search(u'哥哥')[0]
        my.send("发送失败了")

if __name__ == '__main__':
    # str = input("输入q退出")
    # if str == "q":
    #     exit(0)
    # else:
    send_news(str)

    #sys.exit()







bot = Bot(cache_path=True)
found = bot.friends().search('信息通知群')
print("Done")

@bot.register(found)
def message(msg):
    ret = "你好"
    return ret


