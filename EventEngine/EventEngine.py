# -*- coding: UTF-8 -*-
# author:@Jack.Wang


from threading import *
from queue import Queue, Empty

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