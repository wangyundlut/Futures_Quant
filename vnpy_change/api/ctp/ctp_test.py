#!/usr/bin/env python
# -*- coding: utf-8 -*-

from vnpy_change.api.ctp.vnctpmd import MdApi
import time
import os
import sys
import pandas as pd
import numpy as np


class zyc_time:
    def __init__(self):
        pass

    def zyc_timeNow(self):
        t = time.localtime(time.time())
        tS = time.strftime("%Y-%m-%d %H:%M:%S", t)
        return tS

    def zyc_print(self, strG):
        tS = self.zyc_timeNow()
        print(tS + ' -> '*3 + strG)


class zyc_ctpmd(MdApi, zyc_time):
    # 继承ctp的行情
    def __init__(self):
        MdApi.__init__(self)
        zyc_time.__init__(self)
        self.zyc_print('zyc_ctpmd 类')
        self.reqID = 0  # 操作请求编号
        self.tick = {}
        self.tick_his = {}
        self.bar = {}

    def onFrontConnected(self):
        self.zyc_print('行情服务器连接')
        self.login()  # 连接成功后登录账户

    def onFrontDisconnected(self):
        self.zyc_print('行情服务器断开连接')

    def login(self):
        req = {}
        req['UserID'] = self.userID
        req['Password'] = self.password
        req['BrokerID'] = self.brokerID
        self.reqID += 1
        self.reqUserLogin(req, self.reqID)

    def connect(self, userID, password, brokerID, address):
        """初始化连接"""
        self.userID = userID  # 账号
        self.password = password  # 密码
        self.brokerID = brokerID  # 经纪商代码
        self.address = address  # 服务器地址
        # path = os.getcwd() + '/md/con/'
        path = 'c:/ctp_con/md/'
        if not os.path.exists(path):
            os.makedirs(path)
        self.createFtdcMdApi(path)  # 创建C++环境中的API对象，这里传入的参数是需要用来保存.con文件的文件夹路径
        self.registerFront(self.address)
        # 注册服务器地址
        self.init()
        # 初始化连接，成功会调用onFrontConnected
        self.zyc_print('测试-connect')

    def onRtnDepthMarketData(self, data):
        """行情推送"""

        self.data = data
        try:
            self.zyc_print(
                '行情推送:' + data['UpdateTime'] + ',品种:' + data['InstrumentID'] + ',最新价格:' +
                str(data['LastPrice']) + ' TradingDay: ' + data['TradingDay'] + ' ActionDay: ' + data['ActionDay'])
            # print(data)
            # print(data)
            # data=self.data
            InstrumentID = data['InstrumentID']
            data['TradingDay'] = data['TradingDay'][:4] + '-' + data['TradingDay'][4:6] + '-' + data['TradingDay'][6:8]
            date = data['TradingDay'] + ' ' + data['UpdateTime']
            tick = [date, data['InstrumentID'], data['LastPrice'], data['Volume'], data['OpenInterest']]
            self.tick[InstrumentID] = data
            # 收集tick_his数据
            if InstrumentID not in self.tick_his:
                self.tick_his[InstrumentID] = [tick]
            else:
                self.tick_his[InstrumentID].append(tick)

            self.tick_his[InstrumentID + '_pd'] = pd.DataFrame(self.tick_his[InstrumentID],
                                                               columns=['时间', '品种', '最新价格', '数量', '持仓量'])
            '''
            tick=self.tick;tick_his=self.tick_his

            '''
        except:
            self.zyc_print('行情异常')

    def onRspUserLogout(self, data, error, n, last):
        self.zyc_print('行情登出回报')

    def onRspSubMarketData(self, data, error, n, last):
        self.zyc_print('订阅合约回报' + str(data))
        """
        try:
            self.zyc_print('订阅合约回报' + str(error))
        except Exception as e:
            print(e)
        """

    def onRspUnSubMarketData(self, data, error, n, last):
        self.zyc_print('退订合约回报' + str(data))

    def onRspError(self, error, n, last):
        self.zyc_print('错误回报' + str(error))

    def onRspUserLogin(self, data, error, n, last):
        self.zyc_print('行情登录回报')
        # self.subscribeMarketData('cu1810') # 登录成功了才能订阅行情
        # self.subscribeMarketData('rb1810') # 登录成功了才能订阅行情
        # 退订合约 self.unSubscribeMarketData(str(symbol))



    def onRspQryInstrument(self, data, error, n, last):
        self.zyc_print('合约查询回报')
        self.zyc_print(data)

    def qryInstrument(self):
        self.reqID += 1
        self.reqQryInstrument({}, self.reqID)


if __name__ == '__main__':
    # 测试
    self = zyc_ctpmd()
    self.connect('10201091', '5172187a', '8016', 'tcp://101.230.15.17:41213')
    #
    # self.qryInstrument()
    #self.reqQryInstrument({}, self.reqID)
    # self.connect('123609', 'wangyun199', '9999', 'tcp://180.168.146.187:10011')
    import threading
    # self.subscribeMarketData('au1906')
    # self.subscribeMarketData('j1905')
    # self.subscribeMarketData('TA905')
    # self.subscribeMarketData('CF905')
    self.subscribeMarketData('sc1903')
    time.sleep(1000)
    # 模拟
    # 这是实盘
    # self.connect('999839651', '5172187a', '9000', 'tcp://61.140.230.188:41205')
    """
    第一组：Trade：180.168.146.187:10000，Market：180.168.146.187:10010；【电信】
    第二组：Trade：180.168.146.187:10001，Market：180.168.146.187:10011；【电信】
    第三组：Trade：218.202.237.33 :10002，Market：218.202.237.33 :10012；【移动】
    交易前置：180.168.146.187:10030，行情前置：180.168.146.187:10031；【7x24】
    # 这是实盘
    # self.connect('10201091', '5172187a', '8016', 'tcp://101.230.15.17:41213')
    
    {
    'ActionDay': '20181221', 
    'TradingDay': '20181221', 
    'UpdateTime': '14:58:18',
    'UpdateMillisec': 0,  
    'InstrumentID': 'au1906', 
    
    'BidPrice1': 284.7, 
    'BidPrice2': 1.7976931348623157e+308, 
    'BidPrice3': 1.7976931348623157e+308,  
    'BidPrice4': 1.7976931348623157e+308,
    'BidPrice5': 1.7976931348623157e+308, 
    
    'BidVolume1': 233,
    'BidVolume2': 0, 
    'BidVolume3': 0, 
    'BidVolume4': 0, 
    'BidVolume5': 0,
    
    'AskPrice1': 284.75, 
    'AskPrice2': 1.7976931348623157e+308,
    'AskPrice3': 1.7976931348623157e+308, 
    'AskPrice4': 1.7976931348623157e+308,  
    'AskPrice5': 1.7976931348623157e+308,
    'AskVolume1': 9, 
    'AskVolume2': 0, 
    'AskVolume3': 0, 
    'AskVolume4': 0, 
    'AskVolume5': 0,
    
    'CurrDelta': 1.7976931348623157e+308, 
    'AveragePrice': 284419.34696700255, 
    
    'PreOpenInterest': 253774.0, 
    'LastPrice': 284.75, 
    'ExchangeInstID': '', 
    'HighestPrice': 285.75, 
    'PreSettlementPrice': 282.8, 
    
    'Volume': 202440, 
    'Turnover': 57577852600.0, 
    'OpenPrice': 283.4, 
    'PreClosePrice': 282.15, 
    'OpenInterest': 263606.0, 
    'ClosePrice': 1.7976931348623157e+308, 
    'LowerLimitPrice': 271.45, 
    'UpperLimitPrice': 294.1, 
    'SettlementPrice': 1.7976931348623157e+308, 
    'LowestPrice': 283.1, 

    'PreDelta': 0.0, 
    'ExchangeID': ''}
    
    """


