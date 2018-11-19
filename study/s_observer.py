#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
观察者模式，为python事件的学习做准备

观察者模式（发布-订阅模式）
体现了一对多的依赖关系
多个观察者可以同时监听同一个主题，当主题有状态变更时，会通知所有的观察者进行更新
主题：
    包含观察者列表，
    添加和删除观察者方法，
    主题消息，
    通知方法
观察者：
    知道主题消息，
    根据主题消息变更的方法
应用：在一个对象变更的同时需要变更其他对象，且不知道有多少其他对象；
一个抽象模型有2个方面，其中一个方面依赖另一个方面，
    可以使用观察者模式将他们封装在独立的对象中使他们独立的变更和复用


"""
from threading import *
from queue import Queue, Empty
import sys
from datetime import datetime

class EventManager:
    def __init__(self):
        self.__eventQueue = Queue()
        self.__active = False
        self.__thread = Thread(target=self.__Run)
        # 这里的__handlers是一个字典，用来保存对应的事件的响应函数
        # 其中每个键对应的值是一个列表，列表中保存了对该事件监听的响应函数，一对多
        self.__handlers = {}

    def __Run(self):
        while self.__active == True:
            try:
                event = self.__eventQueue.get(block=True, timeout=1)
                self.__EventProcess(event)
            except Empty:
                pass
                #print('Queue Empty')

    def Start(self):
        self.__active = True
        self.__thread.start()

    def __EventProcess(self, event):
        if event.type_ in self.__handlers:
            for handler in self.__handlers[event.type_]:
                handler(event)

    def Stop(self):
        self.__active = False
        self.__thread.join()

    def AddEventLister(self, type_, handler):
        try:
            handlerList = self.__handlers[type_]
        except KeyError:
            handlerList = []

        self.__handlers[type_] = handlerList
        if handler not in handlerList:
            self.__handlers[type_].append(handler)
            print(str(handler) + '添加进dict' + str(type_))
            # handlerList.append(handler)

    def RemoveEventListerner(self, type_, handler):
        try:
            handlerList = self.__handlers[type_]
            if handler in handlerList:
                self.__handlers[type_].remove(handler)
            if not handlerList:
                del self.__handlers[type_]
        except KeyError:
            pass

    def SendEvent(self, event):
        self.__eventQueue.put(event)

class Event:
    def __init__(self, type_=None):
        self.type_ = type_
        self.dict = {}

event_1 = 'Event_1'
event_2 = 'Event_2'

#事件源 公众号
class PublicAccounts:
    def __init__(self):
        pass
    def add_eventmanger(self, eventmanager):
        self.eventManager = eventmanager

    def WriteNewArtical(self):
        #事件对象，写了新文章
        event = Event(type_=event_1)
        event.dict["artical"] = u'如何写出更优雅的代码\n'
        #发送事件
        self.eventManager.SendEvent(event)
        print (u'公众号发送新文章\n')

    def writeoldartical(self):
        event = Event(type_=event_2)
        event.dict['artical'] = 'my code'
        self.eventManager.SendEvent(event)

#监听器 订阅者
class Listener:
    def __init__(self,username):
        self.__username = username

    #监听器的处理函数 读文章
    def ReadArtical(self, event):
        print(u'%s 收到新文章' % self.__username)
        print(u'正在阅读新文章内容：%s'  % event.dict["artical"])

def test():
    listner1 = Listener("thinkroom") #订阅者1
    listner2 = Listener("steve")#订阅者2

    eventManager = EventManager()
    # event_1 = Event(type_='Event_1')

    #绑定事件和监听器响应函数(新文章)
    eventManager.AddEventLister(event_1, listner1.ReadArtical)
    eventManager.AddEventLister(event_1, listner2.ReadArtical)
    #eventManager.AddEventLister(event_2, listner1.ReadArtical)
    #eventManager.AddEventLister(event_2, listner2.ReadArtical)
    eventManager.Start()

    publicAcc = PublicAccounts()
    publicAcc.add_eventmanger(eventManager)
    publicAcc.WriteNewArtical()
    """
    timer = Timer(1, publicAcc.WriteNewArtical)
    timer.start()
    timer = Timer(1, publicAcc.writeoldartical)
    timer.start()
    """

if __name__ == '__main__':
    test()






