#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author:@Jack.Wang
# time :2018/8/15 10:35

from vnctptd import TdApi
import time
import os

import random


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


class ly_ctptd(TdApi, ly_time):
    # 继承ctp的行情
    def __init__(self, address, userID, password, brokerID):
        TdApi.__init__(self)
        ly_time.__init__(self)
        self.ly_print('ly_ctpmd 类')
        self.reqID = 0  # 操作请求编号
        self.data = []
        #self.orderRef = 1000 # 订单编号
        self.orderRef = random.randrange(start=1000, stop=9000, step=random.randint(10, 100))  # 订单编号

        """初始化连接"""
        self.address = address  # 服务器地址
        self.userID = userID  # 账号
        self.password = password  # 密码
        self.brokerID = brokerID  # 经纪商代码
        self.合约查询 = {}
        self.账户信息 = {} # 账户信息
        self.持仓信息 = {} # 账户持仓
        self.报单 = [] # 报单数据
        self.成交数据 = []
        self.程序启动时间 = self.ly_timeNow()

        # path = os.getcwd() + '/ctp_con/'
        path = 'c:/ctp_con/md/'
        if not os.path.exists(path):
            os.makedirs(path)
        self.createFtdcTraderApi(path)  # 创建C++环境中的API对象，这里传入的参数是需要用来保存.con文件的文件夹路径
        self.registerFront(self.address)  # 注册服务器地址
        self.init()  # 初始化连接，成功会调用onFrontConnected
        self.ly_print("初始化连接成功，调用onFrontConnected")

    def onFrontConnected(self):
        self.ly_print('交易服务器连接')
        self.login() # 连接成功后登录账户
    def onFrontDisconnected(self):
        self.ly_print('交易服务器断开连接')
    def login(self):
        req = {}
        req['UserID'] = self.userID
        req['Password'] = self.password
        req['BrokerID'] = self.brokerID
        self.reqID += 1
        self.reqUserLogin(req, self.reqID)

    def onRspUserLogin(self, data, error, n, last):
        self.ly_print('交易登录回报')
        # self.ly_print(str(data))

        s = 'TradingDay:' + data['TradingDay'] + \
            ' ,LoginTime:' + data['LoginTime'] +\
            ' ,BrokerID:' + data['BrokerID'] +\
            ' ,UserID:' + data['UserID'] +\
            ' ,MaxOrderRef:' + data['MaxOrderRef'] +\
            ' ,FrontID:' + str(data['FrontID']) +\
            ' ,SessionID:' + str(data['SessionID']) +\
            ' ,reqId:' + str(n)
        self.FrontID = data['FrontID']
        self.SessionID = data['SessionID']
        self.ly_print(s)
        ########################################
        # self.ly_print(str(data))
    def logout(self):
        req = {}
        req['UserID'] = self.userID
        req['BrokerID'] = self.brokerID
        self.reqID += 1
        self.reqUserLogout(req, self.reqID)

    def onRspUserLogout(self, data, error, n, last):
        self.ly_print('交易登出回报')
        self.ly_print(str(data))
    # 查询账户回报

    def qryAccount(self):
        self.ly_print('查询账户')
        self.reqID += 1
        """
        req = {}
        req['BrokerID'] = self.brokerID
        req['InvestorID'] = self.userID
        self.reqQryTradingAccount(req, self.reqID)
        """
        self.reqQryTradingAccount({}, self.reqID)

    def onRspQryTradingAccount(self, data, error, n, last):
        self.ly_print('查询账户回报')
        try:
            tmp = {}
            tmp["投资者帐号"] = data["AccountID"]
            tmp["静态权益"] = data["PreBalance"]
            tmp["上次存款额"] = data["PreDeposit"]
            tmp["入金金额"] = data["Deposit"]
            tmp["出金金额"] = data["Withdraw"]
            tmp["冻结保证金"] = data["FrozenMargin"]
            tmp["总保证金"] = data["CurrMargin"]
            tmp["手续费"] = data["Commission"]
            tmp["平仓盈亏"] = data["CloseProfit"]
            tmp["持仓盈亏"] = data["PositionProfit"]
            tmp["动态权益"] = data["Balance"]
            tmp["可用资金"] = data["Available"]
            tmp["可取资金"] = data["WithdrawQuota"]
            tmp["交易日"] = data["TradingDay"]

            self.account = tmp
            # 账户资金=self.账户资金
        except:
            print('查询账户回报出错')

    # N/A
    def reqOrder_Limit(self, symbol, price, volume, direction, offset):

        self.reqID += 1 # 操作请求编号
        self.orderRef += 1 # 订单编号
        req = {}

        req['BrokerID'] = self.brokerID
        req['InvestorID'] = self.userID
        req['InstrumentID'] = symbol  # 品种
        req['OrderRef'] = str(self.orderRef)
        req['UserID'] = self.userID
        req['OrderPriceType'] = '2'  # 价格类型 限价
        req['Direction'] = direction
        req['CombOffsetFlag'] = offset
        req['CombHedgeFlag'] = '1'  # 1=投机单 2=套利 3=套保 4=备兑
        req['LimitPrice'] = price  # 价格
        req['VolumeTotalOriginal'] = volume  # 数量
        req['TimeCondition'] = '3'  # 今日有效
        req['GTDDate'] = ''
        req['VolumeCondition'] = '1'  # 任意成交量
        req['MinVolume'] = 1  # 最小成交量为1
        req['ContingentCondition'] = '1'  # 1=立即发单 2=止损  3=止赢  4=预埋单
        req['IsAutoSuspend'] = 0  # 非自动挂起
        req['ForceCloseReason'] = '0'  # 非强平

        self.reqOrderInsert(req, self.reqID)
        # 返回订单号（字符串），便于某些算法进行动态管理
        return str(self.orderRef)
    def onRtnOrder(self, data):
        #self.ly_print('响应：报单回报')

        s = 'InsertDate:' + data['InsertDate'] + \
            ' ,StatusMsg:' + data['StatusMsg'] + \
            ' ,InsertTime:' + data['InsertTime'] + \
            ' ,OrderRef:' + data['OrderRef'] + \
            ' ,RequestID:' + str(data['RequestID']) + \
            ' ,ExchangeID:' + str(data['ExchangeID']) + \
            ' ,OrderSysID:' + str(data['OrderSysID']) + \
            ' ,InstrumentID:' + data['InstrumentID'] + \
            ' ,OrderPriceType:' + data['OrderPriceType'] + \
            ' ,Direction:' + data['Direction'] + \
            ' ,LimitPrice:' + str(data['LimitPrice']) + \
            ' ,VolumeTotalOriginal:' + str(data['VolumeTotalOriginal']) + \
            ' ,ContingentCondition:' + data['ContingentCondition'] + \
            ' ,OrderSubmitStatus:' + data['OrderSubmitStatus'] + \
            ' ,VolumeTraded:' + str(data['VolumeTraded']) + \
            ' ,VolumeTotal:' + str(data['VolumeTotal']) + \
            ' ,StatusMsg:' + data['StatusMsg']
        #self.ly_print(s)
        # self.ly_print(str(data))

    def order_cancel(self, exchangeid, ordersysid):
        """撤单"""
        # self.撤单('SHFE','      610656')
        # self.撤单('SHFE','      609484')
        print('撤单')
        self.reqID += 1

        req = {}

        req['ExchangeID'] = exchangeid
        req['OrderSysID'] = ordersysid

        req['ActionFlag'] = '0'
        req['BrokerID'] = self.brokerID
        req['InvestorID'] = self.userID

        self.reqOrderAction(req, self.reqID)

    # N/A
    def onRtnTrade(self, data):
        # self.zyc_print('成交回报')
        # print(data)
        self.成交data = data
        try:

            成交 = {}
            成交['投资者代码'] = data['InvestorID']
            成交['合约代码'] = data['InstrumentID']
            成交['报单引用'] = data['OrderRef']  # orderRef 比较重要。下单返回的本地编号。一一对应

            成交['买卖方向'] = data['Direction']

            成交['开平标志'] = data['OffsetFlag']
            if 成交['买卖方向'] == '0':
                成交['方向'] = '买入'
            else:
                成交['方向'] = '卖出'

            # 开平类型
            if 成交['开平标志'] == '0':
                成交['开平类型'] = '开仓'
            elif 成交['开平标志'] == '1':
                成交['开平类型'] = '平仓'
            elif 成交['开平标志'] == '3':
                成交['开平类型'] = '平今'
            elif 成交['开平标志'] == '4':
                成交['开平类型'] = '平昨'
            else:
                pass

            if 成交['买卖方向'] == '0' and 成交['开平标志'] == '0':
                成交['信号'] = '开多'
            elif 成交['买卖方向'] == '1' and 成交['开平标志'] == '1':
                成交['信号'] = '平多(平仓)'
            elif 成交['买卖方向'] == '1' and 成交['开平标志'] == '3':
                成交['信号'] = '平多(平今)'
            elif 成交['买卖方向'] == '1' and 成交['开平标志'] == '4':
                成交['信号'] = '平多(平昨)'

            elif 成交['买卖方向'] == '1' and 成交['开平标志'] == '0':
                成交['信号'] = '开空'
            elif 成交['买卖方向'] == '0' and 成交['开平标志'] == '1':
                成交['信号'] = '平空(平仓)'
            elif 成交['买卖方向'] == '0' and 成交['开平标志'] == '3':
                成交['信号'] = '平空(平今)'
            elif 成交['买卖方向'] == '0' and 成交['开平标志'] == '4':
                成交['信号'] = '平空(平昨)'

            else:
                print('出错了')

            成交['价格'] = data['Price']
            成交['数量'] = data['Volume']
            成交['交易所代码'] = data['ExchangeID']

            成交['报单编号'] = data['OrderSysID']

            成交['成交日期'] = data['TradeDate']
            成交['成交时间'] = data['TradeTime']

            成交['成交日期时间'] = 成交['成交日期'][:4] + '-' + 成交['成交日期'][4:6] + '-' + 成交['成交日期'][6:8] + ' ' + 成交['成交时间']

            if 成交['成交日期时间'] > self.程序启动时间:
                print('成交回报：' + 成交['信号'] + ',价格:' + str(成交['价格']) + ',数量:' + str(成交['数量']) + ',成交时间:' + 成交['成交时间'])
                self.成交 = 成交
                self.成交data = data
            # 成交= self.成交
            # data=self.成交data
            if len(self.成交数据) == 0:
                self.成交数据 = [成交]
            else:
                self.成交数据.append(成交)
            # 成交数据=self.成交数据
            # 成交['报单引用']=data['OrderRef'] 利用这个字段来配对
        except:
            print('成交回报出错了')
    # ReqOderInsert
    def onRspOrderInsert(self, data, error, n, last):
        self.ly_print('响应：报单录入')
        # self.ly_print(str(data))
        self.ly_print(data['ordersysID'])
    # 报单查询
    def qryOrder(self):
        # self.ly_print('报单查询')
        self.reqID += 1
        req = {}
        self.reqQryOrder(req, self.reqID)
        print('查询保单之后的orderref：  ' + str(self.orderRef))
    def onRspQryOrder(self, data, error, n, last):
        # self.ly_print('响应：报单查询')
        try:

            报单 = {}
            报单['投资者代码'] = data['InvestorID']
            报单['合约代码'] = data['InstrumentID']
            报单['报单引用'] = data['OrderRef']  # orderRef 比较重要。下单返回的本地编号。一一对应

            报单['买卖方向'] = data['Direction']
            报单['组合开平标志'] = data['CombOffsetFlag']

            报单['价格'] = data['LimitPrice']
            报单['数量'] = data['VolumeTotalOriginal']
            报单['交易所代码'] = data['ExchangeID']
            报单['交易日'] = data['TradingDay']
            报单['报单编号'] = data['OrderSysID']

            报单['报单状态'] = data['OrderStatus']

            报单['报单日期'] = data['InsertDate']
            报单['委托时间'] = data['InsertTime']
            报单['状态信息'] = data['StatusMsg']

            # 报单['报单操作状态']=data['OrderActionStatus'] # TThostFtdcOrderActionStatusType
            # self.zyc_print('报单操作状态: '+str(报单['报单操作状态']))
            # 全部成交=0 部分成交还在队列中=1 部分成交不在队列中=2  未成交还在队列中=3 未成交不在队列中=4
            # 撤单=5 未知='a' 尚未触发 =b 已触发 =c
            if 报单['状态信息'] == '全部成交报单已提交':
                报单['订单状态'] = 0
            elif 报单['状态信息'] == '报单已提交':
                报单['订单状态'] = 1
            elif 报单['状态信息'] == '未成交':
                报单['订单状态'] = 2
            elif 报单['状态信息'] == '已撤单':
                报单['订单状态'] = 3
            else:
                报单['订单状态'] = 4
                # print('订单状态错误：' + 报单['合约代码'] + ',' + 报单['状态信息'])

            # print(报单['报单日期']+' '+报单['委托时间']+'  合约代码:'+报单['合约代码']+',买卖方向:'+报单['买卖方向']+',状态信息:'+报单['状态信息'])
            if len(self.报单) == 0:
                if 报单['订单状态'] < 3:
                    self.报单 = [报单]
            else:
                if 报单['订单状态'] < 3:
                    self.报单.append(报单)
            # 报单数据=self.报单数据
            # 报单['报单引用']=data['OrderRef'] 利用这个字段来配对

        except:
            print('报单回报出错了')
    # 成交查询
    def qryTrade(self):
        self.ly_print('成交查询')
        self.reqID += 1
        req = {}
        self.reqQryTrade(req, self.reqID)
        #############################


        #############################
    def onRspQryTrade(self, data, error, n, last):
        self.ly_print('响应：成交查询')
        self.ly_print(str(data))

    def selttle_info_confirm(self):
        self.ly_print('确认账单')
        self.reqID += 1
        req = {}
        req['BrokerID'] = self.brokerID
        req['InvestorID'] = self.userID
        req['ConfirmDate'] = '20180904'
        req['ConfirmTime'] = '22:10:50'
        self.reqSettlementInfoConfirm(req, self.reqID)
        # self.reqQryInvestorPosition(req, self.reqID)

    # 查询持仓
    def qryInvestorPosition(self):
        self.ly_print('查询持仓')
        self.reqID += 1
        req = {}
        req['BrokerID'] = self.brokerID
        req['InvestorID'] = self.userID
        self.reqQryInvestorPosition(req, self.reqID)


    # reqQryInvestorPosition
    def onRspQryInvestorPosition(self, data, error, n, last):
        self.ly_print('查询持仓回报')
        tmp = {}
        ## 持仓要以本地为准，本地持仓
        tmp["合约代码"] = data["InstrumentID"]
        tmp["持仓多空方向"] = data["PosiDirection"]
        tmp["投资者代码"] = data["InvestorID"]
        tmp["投机套保标志"] = data["HedgeFlag"]
        tmp["持仓日期"] = data["PositionDate"]
        tmp["上日持仓"] = data["YdPosition"]
        tmp["今日持仓"] = data["TodayPosition"]
        tmp["多头冻结"] = data["LongFrozen"]
        tmp["空头冻结"] = data["ShortFrozen"]
        tmp["开仓量"] = data["OpenVolume"]
        tmp["平仓量"] = data["CloseVolume"]
        tmp["持仓成本"] = data["PositionCost"]
        tmp["开仓成本"] = data["OpenCost"]
        tmp["交易所代码"] = data["ExchangeID"]
        tmp["交易日"] = data["TradingDay"]
        tmp["平仓盈亏"] = data["CloseProfit"]
        tmp["持仓盈亏"] = data["PositionProfit"]
        # tmp['策略名称'] = 'jma'
        self.position = tmp


    # 查询合约
    def qryInstrument(self):
        self.ly_print('合约查询')
        self.reqID += 1
        req = {}
        self.reqQryInstrument(req, self.reqID)

    # reqQryInstrument
    def onRspQryInstrument(self, data, error, n, last):
        self.ly_print('响应：合约查询')
        self.ly_print(str(data))

    # ----------------------------------------------------------------------
    def 下单_五秒撤单(self, symbol, price, volume, direction, offset, min_change):
        # 实际下单用这个方法，五秒不成即撤单
        结束信息 = 1
        while True:
            if 结束信息 == 0:
                break
            self.buy(symbol, price, volume, direction, offset)
            orderref = self.orderRef
            time.sleep(5)
            self.qryOrder()
            time.sleep(2)
            for 报单 in self.报单:
                # 定位到刚才的报单
                if 报单['报单引用'] == str(orderref):
                    if 报单['订单状态'] != 0: # 未成交
                        交易所代码 = 报单['交易所代码']
                        报单编号 = 报单['报单编号']
                        # 撤单
                        self.撤单(交易所代码, 报单编号)
                        print('已撤单')

                        if direction == '买入':
                            price = price + min_change
                            self.ly_print(str(price))
                            break
                        if direction == '卖出':
                            price = price - min_change
                            self.ly_print(str(price))
                            break
                    elif 报单['订单状态'] == 0:
                        结束信息 = 0
                        break

        self.ly_print('下单成功')

    def buy(self, symbol, price, volume, direction, offset):  # 多开
        # self.buy('ag1812',3780,1,'买入','开仓')
        # self.buy('ag1812',3600,1,'卖出','平今')

        # self.buy('ag1812',3700,1,'卖出','开仓')
        # self.buy('ag1812',3780,1,'买入','平今')

        # symbol=''
        # price=3850
        # vol=1
        # direction='买入';offset='开仓';
        self.reqID += 1
        self.orderRef += 1
        req = {}

        req['InstrumentID'] = symbol  # 品种
        req['LimitPrice'] = price  # 价格
        req['VolumeTotalOriginal'] = volume  # 数量

        # 价格类型
        # 1-任意价 2-限价 3=最优价 4=最新价
        # 5=最新价浮动上浮1个ticks 6=
        #
        req['OrderPriceType'] = '2'  # 价格类型

        # 买卖方向 0=买  1=卖
        if direction == '买入':
            req['Direction'] = '0'
        elif direction == '卖出':
            req['Direction'] = '1'
        else:
            pass

        # 开平类型映射
        # 0='开仓' 1=平仓 2=强平  3=平今  4= 平昨 5=强减  6=本地强平
        if offset == '开仓':
            req['CombOffsetFlag'] = '0'
        elif offset == '平仓':
            req['CombOffsetFlag'] = '1'
        elif offset == '强平':
            req['CombOffsetFlag'] = '2'
        elif offset == '平今':
            req['CombOffsetFlag'] = '3'
        elif offset == '平昨':
            req['CombOffsetFlag'] = '4'
        elif offset == '强减':
            req['CombOffsetFlag'] = '5'
        elif offset == '本地强平':
            req['CombOffsetFlag'] = '6'
        else:
            pass
        req['OrderRef'] = str(self.orderRef)
        req['InvestorID'] = self.userID
        req['UserID'] = self.userID
        req['BrokerID'] = self.brokerID

        req['CombHedgeFlag'] = '1'  # 1=投机单 2=套利 3=套保 4=备兑
        req['ContingentCondition'] = '1'  # 1=立即发单 2=止损  3=止赢  4=预埋单
        req['ForceCloseReason'] = '0'  # 非强平
        req['IsAutoSuspend'] = 0  # 非自动挂起
        req['TimeCondition'] = '3'  # 今日有效
        req['VolumeCondition'] = '1'  # 任意成交量
        req['MinVolume'] = 1  # 最小成交量为1
        self.reqOrderInsert(req, self.reqID)
        # 返回订单号（字符串），便于某些算法进行动态管理
        return str(self.orderRef)

    def 撤单(self, 交易所, 报单编号):
        """撤单"""
        # self.撤单('SHFE','      610656')
        # self.撤单('SHFE','      609484')
        print('撤单')
        self.reqID += 1

        req = {}

        req['ExchangeID'] = 交易所
        req['OrderSysID'] = 报单编号

        req['ActionFlag'] = '0'
        req['BrokerID'] = self.brokerID
        req['InvestorID'] = self.userID

        self.reqOrderAction(req, self.reqID)

if __name__=='__main__':
    # 测试
    self=ly_ctptd('tcp://180.168.146.187:10000', '123609', 'wangyun199', '9999')
    time.sleep(3)
    self.下单_五秒撤单('cu1810', 47900, 1, '买入', '开仓', 10)
    #time.sleep(5)
    #self.qryAccount()
    # self.reqOrder_Cancel(orderRef='1001', exchangeID='SHFE', ordersysID='113925')
    # self.reqOrder_Limit('rb1810', 4300, 1, '0', '0')
    # self.buy('rb1810', 4300, 1, '买入', '开仓')
    """
    第一组：Trade：180.168.146.187:10000，Market：180.168.146.187:10010；【电信】
    第二组：Trade：180.168.146.187:10001，Market：180.168.146.187:10011；【电信】
    第三组：Trade：218.202.237.33 :10002，Market：218.202.237.33 :10012；【移动】
    交易前置：180.168.146.187:10030，行情前置：180.168.146.187:10031；【7x24】
    # 这是实盘
    # self.connect('999819992', '5172187a', '9000', 'tcp://61.140.230.188:41205')
    """