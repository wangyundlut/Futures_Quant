#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author:@Jack.Wang
# time :2018/8/14 17:57

from vnctpmd import MdApi
import time
import os
import pandas as pd
from data_get_save.PostgreSQL import PostgreSQL
import datetime
from data_get_save.futures_time import futures_time



class ly_time:
    def __init__(self):
        pass

    def ly_timeNow(self):
        t = time.localtime(time.time())
        tS = time.strftime("%Y-%m-%d %H:%M:%S", t)
        return tS

    def ly_print(self, strG):
        tS = self.ly_timeNow()
        print(tS + '  ' + strG)


class ly_ctpmd(MdApi, ly_time):
    # 继承ctp的行情

    def __init__(self, contract, address='tcp://180.168.146.187:10010', userID='123609', password='wangyun199', brokerID='9999'):
        MdApi.__init__(self)
        ly_time.__init__(self)
        tick_sql = PostgreSQL('futures_tick')
        minu_sql = PostgreSQL('futures_min')
        self.tick_sql = tick_sql
        self.minu_sql = minu_sql
        self.contract = contract
        self.ly_print('ly_ctpmd 类')
        self.reqID = 0  # 操作请求编号
        self.tick = {}
        self.tick_his = {}
        self.bar = {}
        self.address = address  # 服务器地址
        self.time_point = {} # 用来记录'rb1901'合成一分钟所需要的时点

        # path = os.getcwd() + '/md/con/'
        path = 'c:/ctp_con/md/'
        if not os.path.exists(path):
            os.makedirs(path)
        self.createFtdcMdApi(path)  # 创建C++环境中的API对象，这里传入的参数是需要用来保存.con文件的文件夹路径
        self.registerFront(self.address)
        # 注册服务器地址
        self.init()
        # 初始化连接，成功会调用onFrontConnected

        self.userID = userID  # 账号
        self.password = password  # 密码
        self.brokerID = brokerID  # 经纪商代码

    def onFrontConnected(self):
        self.ly_print('初始化连接成功，前置无身份服务器已连接！！！可以使用账号密码登陆')
        self.login()

    def onFrontDisconnected(self):
        self.ly_print('前置无身份服务器断开连接！！！')

    def login(self):
        req = {}
        req['UserID'] = self.userID
        req['Password'] = self.password
        req['BrokerID'] = self.brokerID
        self.reqID += 1
        self.reqUserLogin(req, self.reqID)
        self.ly_print('账号密码登陆已连接！！！')

    def onRspUserLogout(self, data, error, n, last):
        self.ly_print('行情登出回报')

    def onRspUserLogin(self, data, error, n, last):
        self.ly_print('行情已登录，可以订阅深度行情')
        self.subscribe_contract()
        # self.subscribeMarketData('cu1810') # 登录成功了才能订阅行情
        # 退订合约 self.unSubscribeMarketData(str(symbol))
    def subscribe_contract(self):
        contract = self.contract
        futures_t = futures_time()
        trade_day = futures_t.trade_day_now_cal()
        for con in contract:
            self.tick_sql.tick_create_table(con)
            min_list = futures_t.trade_time_min(con[0:-4], trade_day)
            self.time_point[con] = min_list
            self.subscribeMarketData(con)


    def onRspSubMarketData(self, data, error, n, last):
        self.ly_print('订阅合约回报' + str(data))

    def onRtnDepthMarketData(self, data):
        """行情推送"""

        self.data = data
        self.ly_print(str(data))
        """
        try:

            tick = {}
            tick['业务日期'] = data['ActionDay']
            tick['最后修改时间'] = data['UpdateTime']
            tick['时间'] = tick['业务日期'][:4] + '-' + tick['业务日期'][4:6] + '-' + tick['业务日期'][6:8]
            tick['时间'] = tick['时间'] + ' ' + tick['最后修改时间']
            tick['最新价'] = data['LastPrice']
            tick['数量'] = data['Volume']
            tick['持仓量'] = data['OpenInterest']
            tick['涨停板价'] = data['UpperLimitPrice']
            tick['跌停板价'] = data['LowerLimitPrice']
            tick['申买一价'] = data['BidPrice1']
            tick['申买一量'] = data['BidVolume1']
            tick['申卖一价'] = data['AskPrice1']
            tick['申卖一量'] = data['AskVolume1']



            # 输入到本地数据库

            tablename = data['InstrumentID']
            self.tick_sql.tick_insert(tablename, tick['时间'], float(tick['最新价']),
                             int(tick['数量']), int(tick['持仓量']),float(tick['涨停板价']),
                             float(tick['跌停板价']), float(tick['申买一价']),
                             int(tick['申买一量']),float(tick['申卖一价']), int(tick['申卖一量']))
            # 根据传入时间点，处理
            if tick['时间'] > self.time_point[tablename][0][1]:
                timestart = self.time_point[tablename][0][0]
                timeend = self.time_point[tablename][0][1]
                self.tick_to_minute(tablename, timestart, timeend)
                self.time_point[tablename].remove(self.time_point[tablename][0])
        except:
            # self.ly_print('行情异常')
            pass
        """

    def tick_to_minute(self, tablename, timestart, timeend):  # tick数据转min数据
        # 根据输入，选取本地tick数据
        try:
            data = self.tick_sql.tick_select_time(tablename, timestart, timeend)
            # 将本地数据合成minute数据
            data = pd.DataFrame(data, columns=['时间', '最新价', '数量', '持仓量'])
            if len(data) != 0:  # 有些没有数据的情况
                t = str(data['时间'][0])[0:19]
                o = data['最新价'][0]
                h = data['最新价'].max()
                l = data['最新价'].min()
                c = data['最新价'][len(data) - 1]
                vo = data['数量'][len(data) - 1] - data['数量'][0]
                op = data['持仓量'][len(data) - 1]
                self.minu_sql.minute_insert(tablenmae,t,o,h,l,c,vo,op)
            print('分钟数据合成完毕')
        except:
            print('合成数据出现问题，请检查')


    def onRspUnSubMarketData(self, data, error, n, last):
        self.ly_print('退订合约回报' + str(data))

    def onRspError(self, error, n, last):
        self.ly_print('错误回报' + str(error))

    def onHeartBeatWarning(self):
        self.ly_print("连接仍继续")

if __name__ == '__main__':
    # 测试
    self = ly_ctpmd(contract=['cu1810','cu1811'], address='tcp://180.168.146.187:10010', userID='123609', password='wangyun199', brokerID='9999')
    #由于是分线程的程序，所以，此时主线程必须等待分线程进行到了之后，才能加入
    # self.subscribeMarketData('cu1810')  # 登录成功了才能订阅行情
    """
    第一组：Trade：180.168.146.187:10000，Market：180.168.146.187:10010；【电信】
    第二组：Trade：180.168.146.187:10001，Market：180.168.146.187:10011；【电信】
    第三组：Trade：218.202.237.33 :10002，Market：218.202.237.33 :10012；【移动】
    交易前置：180.168.146.187:10030，行情前置：180.168.146.187:10031；【7x24】
    # 这是实盘
    # self.connect('999819992', '5172187a', '9000', 'tcp://61.140.230.188:41205')
    """






