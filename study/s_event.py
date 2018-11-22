#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author:@Jack.Wang



"""
    事件驱动引擎
    事件驱动引擎中所有的变量都设置为私有变量，为了不小心从外部修改这些变量的值
    或状态，导致bug
    变量说明：
    __queue:事件队列
    __active:事件引擎开关
    __thread:事件处理线程
    __timer:私有变量，计时器
    __handlers:私有变量，事件处理函数字典

    方法说明：
    __run:私有方法，事件处理线程连续运行用
    __process:私有方法，处理事件，调用注册在引擎中的监听函数
    __onTimer:私有方法，及时器固定事件间隔触发后，向事件队列中存入计时器事件
    start:公共方法，启动引擎
    stop:公共方法，停止引擎
    register:公共方法，向引擎中注册监听事件

    事件监听函数必须定义为输入参数仅为一个event对象，即：

    函数
    def func(event)
    ...
    对象方法
    def method(self, event)
"""

from threading import *
from queue import Queue, Empty
import time

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
                # print('Queue Empty')

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
            # print(str(handler) + '添加进dict' + str(type_))
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



class kline:
    def __init__(self):
        data = [i for i in range(10)]
        self.data = data
        self.kline = {}
        self.kline['num']=0
        self.kline['sum']=10

    def add_eventmanger(self, eventmanger):
        self.eventmanager = eventmanger

    def kline_pub(self):
        event = Event('kline')
        event.dict['num'] = self.kline['num']
        event.dict['sum'] = self.kline['sum']
        self.eventmanager.SendEvent(event)
        print('kline pub ' + str(event.dict['num']))

    def kline_receive(self, event):
        self.kline['num'] = event.dict['num'] + 1
        print('kline_receive ' + str(event.dict['num']))
        if self.kline['num'] <= self.kline['sum']:
            self.kline_pub()
        else:
            print('end')

class strategy:
    def __init__(self):
        self.strategy = {}

    def add_eventmanger(self, eventmanger):
        self.eventmanager = eventmanger

    def strategy_receive(self, event):
        print('strategy receive ' + str(event.dict['num']))
        self.strategy['num'] = event.dict['num']
        self.strategy['sum'] = event.dict['sum']
        self.strategy_public()

    def strategy_public(self):
        event = Event('strategy')
        event.dict['num'] = self.strategy['num']
        event.dict['sum'] = self.strategy['sum']
        self.eventmanager.SendEvent(event)
        print('strategy publib ' + str(event.dict['num']))

class bt:
    def __init__(self):
        self.bt = {}

    def add_eventmanger(self, eventmanger):
        self.eventmanager = eventmanger

    def bt_receive(self, event):
        print('bt_receive ' + str(event.dict['num']))
        self.bt['num'] = event.dict['num']
        self.bt['sum'] = event.dict['sum']
        self.bt_public()


    def bt_public(self):
        event = Event('bt')
        event.dict['num'] = self.bt['num']
        event.dict['sum'] = self.bt['sum']
        self.eventmanager.SendEvent(event)
        print('bt_public ' + str(event.dict['num']))


def mytest():

    stra = strategy()
    back = bt()
    kl = kline()
    event_kl = Event('kline')
    event_st = Event('strategy')
    event_bt = Event('bt')
    eventmanager = EventManager()

    eventmanager.AddEventLister('kline', stra.strategy_receive)
    eventmanager.AddEventLister('strategy', back.bt_receive)
    eventmanager.AddEventLister('bt', kl.kline_receive)
    eventmanager.Start()

    stra.add_eventmanger(eventmanager)
    back.add_eventmanger(eventmanager)
    kl.add_eventmanger(eventmanager)
    # 启动函数
    kl.kline_pub()


if __name__=='__main__':
    mytest()
