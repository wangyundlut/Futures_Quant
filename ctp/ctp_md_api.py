# -*- coding: utf-8 -*-


#模拟账户注册和下载软件
#http://www.simnow.com.cn/static/softwareOthersDownload.action


from vnctpmd import MdApi
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
        print(tS + '  ' + strG)

class zyc_ctpmd(MdApi,zyc_time):
    # 继承ctp的行情
    def __init__(self):
        MdApi.__init__(self)
        zyc_time.__init__(self)
        self.zyc_print('zyc_ctpmd 类')
        self.reqID=0 # 操作请求编号
        self.tick={}
        self.tick_his={}
        self.bar={}
    def onFrontConnected(self):
        self.zyc_print('行情服务器连接')
        self.login() # 连接成功后登录账户
    def onFrontDisconnected(self):
        self.zyc_print('行情服务器断开连接')
    def login(self):
        req = {}
        req['UserID'] = self.userID
        req['Password'] = self.password
        req['BrokerID'] = self.brokerID
        self.reqID += 1
        self.reqUserLogin(req, self.reqID)
    def connect(self,userID, password, brokerID, address):
        """初始化连接"""
        self.userID = userID  # 账号
        self.password = password  # 密码
        self.brokerID = brokerID  # 经纪商代码
        self.address = address  # 服务器地址
        # path = os.getcwd() + '/md/con/'
        path ='c:/ctp_con/md/'
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
        
        self.data=data
        try:
            self.zyc_print('行情推送:'+data['UpdateTime']+',品种:'+data['InstrumentID']+',最新价格:'+str(data['LastPrice']) )
            #print(data)
            #data=self.data
            InstrumentID=data['InstrumentID']
            data['TradingDay']=data['TradingDay'][:4]+'-'+data['TradingDay'][4:6]+'-'+data['TradingDay'][6:8]
            date=data['TradingDay']+' '+data['UpdateTime']
            tick=[date,data['InstrumentID'],data['LastPrice'],data['Volume'],data['OpenInterest']]
            self.tick[InstrumentID]=data
            # 收集tick_his数据
            if InstrumentID not in self.tick_his:
                self.tick_his[InstrumentID]=[tick]
            else:
                self.tick_his[InstrumentID].append(tick)
                
            self.tick_his[InstrumentID+'_pd']=pd.DataFrame(self.tick_his[InstrumentID],columns=['时间','品种','最新价格','数量','持仓量'])
            '''
            tick=self.tick;tick_his=self.tick_his
            
            '''
        except:
            pass
            self.zyc_print('行情异常')
        
    def onRspUserLogout(self, data, error, n, last):
        self.zyc_print('行情登出回报')
        
    def onRspSubMarketData(self, data, error, n, last):
        self.zyc_print('订阅合约回报'+str(data))
        
    def onRspUnSubMarketData(self, data, error, n, last):
        self.zyc_print('退订合约回报'+str(data))
    def onRspError(self, error, n, last):
        self.zyc_print('错误回报'+str(error))

    def onRspUserLogin(self, data, error, n, last):
        self.zyc_print('行情登录回报')
        # self.subscribeMarketData('cu1810') # 登录成功了才能订阅行情
        # self.subscribeMarketData('rb1810') # 登录成功了才能订阅行情
        # 退订合约 self.unSubscribeMarketData(str(symbol))

        
if __name__=='__main__':
    # 测试
    import time
    self=zyc_ctpmd()
    self.connect('123609', 'wangyun199', '9999', 'tcp://180.168.146.187:10011')
    time.sleep(2)
    self.subscribeMarketData('cu1902')
    self.subscribeMarketData('rb1910')
    time.sleep(100)
    # 模拟
    # 这是实盘
    # self.connect('999819992', '5172187a', '9000', 'tcp://61.140.230.188:41205')
    """
    第一组：Trade：180.168.146.187:10000，Market：180.168.146.187:10010；【电信】
    第二组：Trade：180.168.146.187:10001，Market：180.168.146.187:10011；【电信】
    第三组：Trade：218.202.237.33 :10002，Market：218.202.237.33 :10012；【移动】
    交易前置：180.168.146.187:10030，行情前置：180.168.146.187:10031；【7x24】
    # 这是实盘
    # self.connect('999819992', '5172187a', '9000', 'tcp://61.140.230.188:41205')
    """



    





        