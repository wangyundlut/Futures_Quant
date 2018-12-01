#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pymongo
import collections
import datetime

from vnpy_backtest_imitation.vnrpc import RpcServer,RpcClient,RemoteException
from vnpy_backtest_imitation.vtFunction import globalSetting
from vnpy_backtest_imitation.vtObject import *

class BacktestingEngine:
    """
    CTA回测引擎
    函数接口和策略引擎保持一样，
    从而实现同一套代码从回测到实盘
    """
    TICK_MODE = 'tick'
    BAR_MODE = 'bar'

    def __init__(self):
        """构造函数"""


        self.dbClient = None   # 数据库客户端
        self.dbCursor = None   # 数据库指针
        self.hdsClient = None  # 历史数据服务器客户端

        self.dbName = None     # 数据库客户端
        self.symbol = None     # 数据库合约
        self.mode = self.BAR_MODE # 回测模式，默认为K线

        self.dataStartDate = None
        self.dataStartDate = None

        self.dataStartDate = datetime.strptime("2014-07-04 21:30:00", "%Y-%m-%d %H:%M:%S")
        self.dataEndDate = datetime.strptime("2014-07-08 14:30:00", "%Y-%m-%d %H:%M:%S")
        self.strategyStartDate = datetime.strptime("2014-07-04 21:35:00", "%Y-%m-%d %H:%M:%S")





        self.dbName = "VnTrader_1Min_Db"
        self.symbol = "j"


        # ------------------------------------------------
    # 数据回放相关
    # ------------------------------------------------

    # ----------------------------------------------------------------------
    def initHdsClient(self):
        """初始化历史数据服务器客户端，注意，这里不是服务端，服务端在下面的函数中"""
        reqAddress = 'tcp://localhost:5555'
        subAddress = 'tcp://localhost:7777'

        self.hdsClient = RpcClient(reqAddress, subAddress)
        self.hdsClient.start()
        print('初始化历史数据服务器客户端成功！！！！')

    def loadHistoryData(self):
        """载入历史数据"""
        self.dbClient = pymongo.MongoClient(globalSetting['mongoHost'], globalSetting['mongoPort'])
        dbClient = self.dbClient
        print(dbClient)
        collection = self.dbClient[self.dbName][self.symbol]

        self.output(u'开始载入数据')

        # 首先根据回测模式，确认要使用的数据类
        if self.mode == self.BAR_MODE:
            dataClass = VtBarData
            func = self.newBar
        else:
            dataClass = VtTickData
            func = self.newTick

        # 载入初始化需要用的数据
        if self.hdsClient:
            initCursor = self.hdsClient.loadHistoryData(self.dbName,
                                                        self.symbol,
                                                        self.dataStartDate,
                                                        self.strategyStartDate)
        else:
            flt = {'datetime':{'$gte':self.dataStartDate,
                               '$lte':self.strategyStartDate}}
            initCursor = collection.find(flt).sort('datetime')

        # 将数据从查询指针中读取出，并生成列表
        self.initData = []              # 清空initData列表
        for d in initCursor:
            data = dataClass()
            data.__dict__ = d
            self.initData.append(data)

        # 载入回测数据
        if self.hdsClient:
            self.dbCursor = self.hdsClient.loadHistoryData(self.dbName,
                                                           self.symbol,
                                                           self.strategyStartDate,
                                                           self.dataEndDate)
        else:
            if not self.dataEndDate:
                flt = {'datetime':{'$gte':self.strategyStartDate}}   # 数据过滤条件
            else:
                flt = {'datetime':{'$gte':self.strategyStartDate,
                                   '$lte':self.dataEndDate}}
            self.dbCursor = collection.find(flt).sort('datetime')

        if isinstance(self.dbCursor, list):
            count = len(initCursor) + len(self.dbCursor)
        else:
            count = initCursor.count() + self.dbCursor.count()
        self.output(u'载入完成，数据量：%s' %count)

    def newBar(self):
        """收到新的bardata之后做什么"""
        pass

    def newTick(self):
        """收到新的tick数据之后做什么"""
        pass

    def output(self, content):
        """输出内容"""
        print(str(datetime.now()) + "\t" + content)


def main():
    self = BacktestingEngine()
    self.loadHistoryData()
    # self.initHdsClient()
    print('Hello world!!!')


if __name__ == '__main__':
    main()