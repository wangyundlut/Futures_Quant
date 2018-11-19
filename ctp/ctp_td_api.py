# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 16:37:06 2018

模拟账户注册和下载软件
http://www.simnow.com.cn/static/softwareOthersDownload.action


@author: Administrator
"""

from vnctptd import TdApi
import time
import os

import random

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
        
class zyc_ctptd(TdApi,zyc_time):
    # 继承ctp的行情
    def __init__(self):
        TdApi.__init__(self)
        zyc_time.__init__(self)
        self.zyc_print('zyc_ctpmd 类')
        self.reqID=0 # 操作请求编号
        self.data=[]
        self.orderRef = random.randrange(start=1000,stop=9000,step=random.randint(10,100)  )           # 订单编号
    def onFrontConnected(self):
        self.zyc_print('交易服务器连接')
        self.login() # 连接成功后登录账户
    def onFrontDisconnected(self):
        self.zyc_print('交易服务器断开连接')

    def login(self):
        req = {}
        req['UserID'] = self.userID
        req['Password'] = self.password
        req['BrokerID'] = self.brokerID
        self.reqID += 1
        self.reqUserLogin(req, self.reqID)

    def onRspUserLogin(self, data, error, n, last):
        self.zyc_print('交易登录回报')
        self.qryAccount()
        # self.buy('ag1812',3740,1,'买入','开仓')
        
    def onRspUserLogout(self, data, error, n, last):
        self.zyc_print('交易登出回报')

    def connect(self,userID, password, brokerID, address):
        """初始化连接"""
        self.userID = userID  # 账号
        self.password = password  # 密码
        self.brokerID = brokerID  # 经纪商代码
        self.address = address  # 服务器地址
        #path = os.getcwd() + '/ctp_con/'
        path ='c:/ctp_con/md/'
        if not os.path.exists(path):
            os.makedirs(path)
        self.createFtdcTraderApi(path)  # 创建C++环境中的API对象，这里传入的参数是需要用来保存.con文件的文件夹路径
        self.registerFront(self.address) # 注册服务器地址
        self.init()# 初始化连接，成功会调用onFrontConnected
        #self.zyc_print('测试-connect')
    # 
    def qryAccount(self):
        self.zyc_print('查询账户')
        self.reqID += 1
        self.reqQryTradingAccount({}, self.reqID)
    def onRspQryTradingAccount(self, data, error, n, last):
        self.zyc_print('查询账户回报')
        self.zyc_print(str(data))

    def qryPosition(self):
        self.zyc_print('查询持仓')
        self.reqID += 1
        req = {}
        req['BrokerID'] = self.brokerID
        req['InvestorID'] = self.userID
        self.reqQryInvestorPosition(req, self.reqID)
    def onRspQryInvestorPosition(self, data, error, n, last):
        self.zyc_print('查询持仓回报')
        self.zyc_print(str(data))
        
    def qryInstrument(self):
        self.zyc_print('查询合约')
        self.reqID += 1
        req = {}
        self.reqQryInstrument(req, self.reqID)
    def onRspQryInstrument(self, data, error, n, last):
        self.zyc_print('合约查询回报')
        self.zyc_print(str(data))

    def onRtnOrder(self, data):
        self.zyc_print('报单回报')
        self.zyc_print(str(data))
    def onRtnTrade(self, data):
        self.zyc_print('成交回报')
        self.zyc_print(str(data))
    def reqOrderAction(self, data, error, n, last):
        self.zyc_print('撤单')
    def onRspOrderAction(self, data, error, n, last):
        self.zyc_print('撤单响应')
        self.onRtnTrade(self, data)
        
        
    #----------------------------------------------------------------------
    def buy(self, symbol, price, volume,direction,offset):  # 多开
        # self.buy('ag1812',3780,1,'买入','开仓')
        # self.buy('ag1812',3600,1,'卖出','平今')
        
        # self.buy('ag1812',3700,1,'卖出','开仓')
        # self.buy('ag1812',3780,1,'买入','平今')
        
        #symbol=''
        #price=3850
        #vol=1
        # direction='买入';offset='开仓';
        self.reqID += 1
        self.orderRef += 1
        req = {}
        
        req['InstrumentID'] = symbol # 品种
        req['LimitPrice'] = price # 价格
        req['VolumeTotalOriginal'] =volume # 数量
        
        # 价格类型 
        # 1-任意价 2-限价 3=最优价 4=最新价 
        # 5=最新价浮动上浮1个ticks 6=
        # 
        req['OrderPriceType'] ='2' # 价格类型 
        
        # 买卖方向 0=买  1=卖
        if direction=='买入':
            req['Direction'] = '0'
        elif direction=='卖出':
            req['Direction'] = '1'
        else:
            pass
        
        # 开平类型映射
        # 0='开仓' 1=平仓 2=强平  3=平今  4= 平昨 5=强减  6=本地强平
        if offset=='开仓':
            req['CombOffsetFlag'] ='0'
        elif offset=='平仓':
            req['CombOffsetFlag'] ='1'
        elif offset=='强平':
            req['CombOffsetFlag'] ='2'
        elif offset=='平今':
            req['CombOffsetFlag'] ='3'
        elif offset=='平昨':
            req['CombOffsetFlag'] ='4'
        elif offset=='强减':
            req['CombOffsetFlag'] ='5'
        elif offset=='本地强平':
            req['CombOffsetFlag'] ='6'
        else:
            pass
        req['OrderRef'] = str(self.orderRef)
        req['InvestorID'] = self.userID
        req['UserID'] = self.userID
        req['BrokerID'] = self.brokerID
        
        req['CombHedgeFlag'] = '1'      # 1=投机单 2=套利 3=套保 4=备兑
        req['ContingentCondition'] = '1' # 1=立即发单 2=止损  3=止赢  4=预埋单
        req['ForceCloseReason'] = '0' # 非强平
        req['IsAutoSuspend'] = 0                                             # 非自动挂起
        req['TimeCondition'] = '3'               # 今日有效
        req['VolumeCondition'] = '1'             # 任意成交量
        req['MinVolume'] = 1                                                 # 最小成交量为1
        self.reqOrderInsert(req, self.reqID)
        # 返回订单号（字符串），便于某些算法进行动态管理
        return str(self.orderRef)
    
    def onRspQryInstrument(self, data, error, n, last):
        pass
        self.zyc_print(str(data))
        self.Instrument=data
        self.data.append(data)
        '''
        self.reqID += 1
        self.reqQryInstrument({}, self.reqID)
        Instrument=self.Instrument
        '''
        
        
if __name__=='__main__':
    # 测试
    self=zyc_ctptd()
    self.connect('123609', 'wangyun199', '9999', 'tcp://180.168.146.187:10001')
    # self.buy('j1901', 2495, 1, '买入', '开仓')
    """
    第一组：Trade：180.168.146.187:10000，Market：180.168.146.187:10010；【电信】
    第二组：Trade：180.168.146.187:10001，Market：180.168.146.187:10011；【电信】
    第三组：Trade：218.202.237.33 :10002，Market：218.202.237.33 :10012；【移动】
    交易前置：180.168.146.187:10030，行情前置：180.168.146.187:10031；【7x24】
    # 这是实盘
    # self.connect('999819992', '5172187a', '9000', 'tcp://61.140.230.188:41205')
    """