#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pymongo
from collections import OrderedDict
import datetime

from vnpy_backtest_imitation.vnrpc import RpcServer,RpcClient,RemoteException
from vnpy_backtest_imitation.vtFunction import globalSetting
from vnpy_backtest_imitation.vtObject import *
from vnpy_backtest_imitation.constant import *
from vnpy_backtest_imitation.ctaBase import *


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
        """Constructor"""
        # 本地停止单
        self.stopOrderCount = 0  # 编号计数：stopOrderID = STOPORDERPREFIX + str(stopOrderCount)

        # 本地停止单字典, key为stopOrderID，value为stopOrder对象
        self.stopOrderDict = {}  # 停止单撤销后不会从本字典中删除
        self.workingStopOrderDict = {}  # 停止单撤销后会从本字典中删除

        #self.engineType = ENGINETYPE_BACKTESTING  # 引擎类型为回测

        self.strategy = None  # 回测策略
        self.mode = self.BAR_MODE  # 回测模式，默认为K线

        #self.startDate = ''
        #self.initDays = 0
        #self.endDate = ''

        #self.capital = 1000000  # 回测时的起始本金（默认100万）
        #self.slippage = 0  # 回测时假设的滑点
        #self.rate = 0  # 回测时假设的佣金比例（适用于百分比佣金）
        #self.size = 1  # 合约大小，默认为1
        self.priceTick = 0  # 价格最小变动

        self.dbClient = None  # 数据库客户端
        self.dbCursor = None  # 数据库指针
        self.hdsClient = None  # 历史数据服务器客户端

        #self.initData = []  # 初始化用的数据
        self.dbName = ''  # 回测数据库名
        self.symbol = ''  # 回测集合名

        self.dataStartDate = None  # 回测数据开始日期，datetime对象
        self.dataEndDate = None  # 回测数据结束日期，datetime对象
        self.strategyStartDate = None  # 策略启动日期（即前面的数据用于初始化），datetime对象

        self.limitOrderCount = 0  # 限价单编号
        self.limitOrderDict = OrderedDict()  # 限价单字典
        self.workingLimitOrderDict = OrderedDict()  # 活动限价单字典，用于进行撮合用

        self.tradeCount = 0  # 成交编号
        self.tradeDict = OrderedDict()  # 成交字典

        #self.logList = []  # 日志记录

        # 当前最新数据，用于模拟成交用
        #self.tick = None
        #self.bar = None
        #self.dt = None  # 最新的时间

        # 日线回测结果计算用
        self.dailyResultDict = OrderedDict()


        # ===================================================
        self.dataStartDate = datetime.strptime("2014-07-04 21:30:00", "%Y-%m-%d %H:%M:%S")
        self.dataEndDate = datetime.strptime("2014-07-08 14:30:00", "%Y-%m-%d %H:%M:%S")
        self.strategyStartDate = datetime.strptime("2014-07-04 21:35:00", "%Y-%m-%d %H:%M:%S")

        self.dbName = "VnTrader_1Min_Db"
        self.symbol = "j"

    # ------------------------------------------------
    # 通用功能
    # ------------------------------------------------

    # ----------------------------------------------------------------------
    def roundToPriceTick(self, price):
        """取整价格到合约最小价格变动"""
        if not self.priceTick:
            return price

        newPrice = round(price / self.priceTick, 0) * self.priceTick
        return newPrice



    # ------------------------------------------------
    # 数据回放相关
    # ------------------------------------------------


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

    # ----------------------------------------------------------------------
    def runBacktesting(self):
        """运行回测"""
        # 载入历史数据
        self.loadHistoryData()

        # 首先根据回测模式，确认要使用的数据类
        if self.mode == self.BAR_MODE:
            dataClass = VtBarData
            func = self.newBar
        else:
            dataClass = VtTickData
            func = self.newTick

        self.output(u'开始回测')

        self.strategy.onInit()
        self.strategy.inited = True
        self.output(u'策略初始化完成')

        self.strategy.trading = True
        self.strategy.onStart()
        self.output(u'策略启动完成')

        self.output(u'开始回放数据')

        for d in self.dbCursor:
            data = dataClass()
            data.__dict__ = d
            func(data)

        self.output(u'数据回放结束')

    # ----------------------------------------------------------------------
    def newBar(self, bar):
        """新的K线"""
        self.bar = bar
        self.dt = bar.datetime

        self.crossLimitOrder()  # 先撮合限价单
        self.crossStopOrder()  # 再撮合停止单
        self.strategy.onBar(bar)  # 推送K线到策略中

        self.updateDailyClose(bar.datetime, bar.close)

    # ----------------------------------------------------------------------
    def newTick(self, tick):
        """新的Tick"""
        self.tick = tick
        self.dt = tick.datetime

        self.crossLimitOrder()
        self.crossStopOrder()
        self.strategy.onTick(tick)

        self.updateDailyClose(tick.datetime, tick.lastPrice)

    # ----------------------------------------------------------------------
    def updateDailyClose(self, dt, price):
        """更新每日收盘价"""
        date = dt.date()

        if date not in self.dailyResultDict:
            self.dailyResultDict[date] = DailyResult(date, price)
        else:
            self.dailyResultDict[date].closePrice = price

    def output(self, content):
        """输出内容"""
        print(str(datetime.now()) + "\t" + content)

    def crossLimitOrder(self):
        """基于最新数据撮合限价单"""
        # 先确定会撮合成交的价格
        if self.mode == self.BAR_MODE:
            buyCrossPrice = self.bar.low  # 若买入方向限价单价格高于该价格，则会成交
            sellCrossPrice = self.bar.high  # 若卖出方向限价单价格低于该价格，则会成交
            buyBestCrossPrice = self.bar.open  # 在当前时间点前发出的买入委托可能的最优成交价
            sellBestCrossPrice = self.bar.open  # 在当前时间点前发出的卖出委托可能的最优成交价
        else:
            buyCrossPrice = self.tick.askPrice1
            sellCrossPrice = self.tick.bidPrice1
            buyBestCrossPrice = self.tick.askPrice1
            sellBestCrossPrice = self.tick.bidPrice1

        # 遍历限价单字典中的所有限价单
        for orderID, order in list(self.workingLimitOrderDict.items()):
            # 推送委托进入队列（未成交）的状态更新
            if not order.status:
                order.status = STATUS_NOTTRADED
                self.strategy.onOrder(order)

            # 判断是否会成交
            buyCross = (order.direction == DIRECTION_LONG and
                        order.price >= buyCrossPrice and
                        buyCrossPrice > 0)  # 国内的tick行情在涨停时askPrice1为0，此时买无法成交

            sellCross = (order.direction == DIRECTION_SHORT and
                         order.price <= sellCrossPrice and
                         sellCrossPrice > 0)  # 国内的tick行情在跌停时bidPrice1为0，此时卖无法成交

            # 如果发生了成交
            if buyCross or sellCross:
                # 推送成交数据
                self.tradeCount += 1  # 成交编号自增1
                tradeID = str(self.tradeCount)
                trade = VtTradeData()
                trade.vtSymbol = order.vtSymbol
                trade.tradeID = tradeID
                trade.vtTradeID = tradeID
                trade.orderID = order.orderID
                trade.vtOrderID = order.orderID
                trade.direction = order.direction
                trade.offset = order.offset

                # 以买入为例：
                # 1. 假设当根K线的OHLC分别为：100, 125, 90, 110
                # 2. 假设在上一根K线结束(也是当前K线开始)的时刻，策略发出的委托为限价105
                # 3. 则在实际中的成交价会是100而不是105，因为委托发出时市场的最优价格是100
                if buyCross:
                    trade.price = min(order.price, buyBestCrossPrice)
                    self.strategy.pos += order.totalVolume
                else:
                    trade.price = max(order.price, sellBestCrossPrice)
                    self.strategy.pos -= order.totalVolume

                trade.volume = order.totalVolume
                trade.tradeTime = self.dt.strftime('%H:%M:%S')
                trade.dt = self.dt
                self.strategy.onTrade(trade)

                self.tradeDict[tradeID] = trade

                # 推送委托数据
                order.tradedVolume = order.totalVolume
                order.status = STATUS_ALLTRADED
                self.strategy.onOrder(order)

                # 从字典中删除该限价单
                if orderID in self.workingLimitOrderDict:
                    del self.workingLimitOrderDict[orderID]

    # ----------------------------------------------------------------------
    def crossStopOrder(self):
        """基于最新数据撮合停止单"""
        # 先确定会撮合成交的价格，这里和限价单规则相反
        if self.mode == self.BAR_MODE:
            buyCrossPrice = self.bar.high  # 若买入方向停止单价格低于该价格，则会成交
            sellCrossPrice = self.bar.low  # 若卖出方向限价单价格高于该价格，则会成交
            bestCrossPrice = self.bar.open  # 最优成交价，买入停止单不能低于，卖出停止单不能高于
        else:
            buyCrossPrice = self.tick.lastPrice
            sellCrossPrice = self.tick.lastPrice
            bestCrossPrice = self.tick.lastPrice

        # 遍历停止单字典中的所有停止单
        for stopOrderID, so in list(self.workingStopOrderDict.items()):
            # 判断是否会成交
            buyCross = so.direction == DIRECTION_LONG and so.price <= buyCrossPrice
            sellCross = so.direction == DIRECTION_SHORT and so.price >= sellCrossPrice

            # 如果发生了成交
            if buyCross or sellCross:
                # 更新停止单状态，并从字典中删除该停止单
                so.status = STOPORDER_TRIGGERED
                if stopOrderID in self.workingStopOrderDict:
                    del self.workingStopOrderDict[stopOrderID]

                    # 推送成交数据
                self.tradeCount += 1  # 成交编号自增1
                tradeID = str(self.tradeCount)
                trade = VtTradeData()
                trade.vtSymbol = so.vtSymbol
                trade.tradeID = tradeID
                trade.vtTradeID = tradeID

                if buyCross:
                    self.strategy.pos += so.volume
                    trade.price = max(bestCrossPrice, so.price)
                else:
                    self.strategy.pos -= so.volume
                    trade.price = min(bestCrossPrice, so.price)

                self.limitOrderCount += 1
                orderID = str(self.limitOrderCount)
                trade.orderID = orderID
                trade.vtOrderID = orderID
                trade.direction = so.direction
                trade.offset = so.offset
                trade.volume = so.volume
                trade.tradeTime = self.dt.strftime('%H:%M:%S')
                trade.dt = self.dt

                self.tradeDict[tradeID] = trade

                # 推送委托数据
                order = VtOrderData()
                order.vtSymbol = so.vtSymbol
                order.symbol = so.vtSymbol
                order.orderID = orderID
                order.vtOrderID = orderID
                order.direction = so.direction
                order.offset = so.offset
                order.price = so.price
                order.totalVolume = so.volume
                order.tradedVolume = so.volume
                order.status = STATUS_ALLTRADED
                order.orderTime = trade.tradeTime

                self.limitOrderDict[orderID] = order

                # 按照顺序推送数据
                self.strategy.onStopOrder(so)
                self.strategy.onOrder(order)
                self.strategy.onTrade(trade)

    # ------------------------------------------------
    def sendOrder(self, vtSymbol, orderType, price, volume, strategy):
        """发单"""
        self.limitOrderCount += 1
        orderID = str(self.limitOrderCount)

        order = VtOrderData()
        order.vtSymbol = vtSymbol
        order.price = self.roundToPriceTick(price)
        order.totalVolume = volume
        order.orderID = orderID
        order.vtOrderID = orderID
        order.orderTime = self.dt.strftime('%H:%M:%S')

        # CTA委托类型映射
        if orderType == CTAORDER_BUY:
            order.direction = DIRECTION_LONG
            order.offset = OFFSET_OPEN
        elif orderType == CTAORDER_SELL:
            order.direction = DIRECTION_SHORT
            order.offset = OFFSET_CLOSE
        elif orderType == CTAORDER_SHORT:
            order.direction = DIRECTION_SHORT
            order.offset = OFFSET_OPEN
        elif orderType == CTAORDER_COVER:
            order.direction = DIRECTION_LONG
            order.offset = OFFSET_CLOSE

            # 保存到限价单字典中
        self.workingLimitOrderDict[orderID] = order
        self.limitOrderDict[orderID] = order

        return [orderID]

    # ----------------------------------------------------------------------
    def cancelOrder(self, vtOrderID):
        """撤单"""
        if vtOrderID in self.workingLimitOrderDict:
            order = self.workingLimitOrderDict[vtOrderID]

            order.status = STATUS_CANCELLED
            order.cancelTime = self.dt.strftime('%H:%M:%S')

            self.strategy.onOrder(order)

            del self.workingLimitOrderDict[vtOrderID]

    # ----------------------------------------------------------------------
    def sendStopOrder(self, vtSymbol, orderType, price, volume, strategy):
        """发停止单（本地实现）"""
        self.stopOrderCount += 1
        stopOrderID = STOPORDERPREFIX + str(self.stopOrderCount)

        so = StopOrder()
        so.vtSymbol = vtSymbol
        so.price = self.roundToPriceTick(price)
        so.volume = volume
        so.strategy = strategy
        so.status = STOPORDER_WAITING
        so.stopOrderID = stopOrderID

        if orderType == CTAORDER_BUY:
            so.direction = DIRECTION_LONG
            so.offset = OFFSET_OPEN
        elif orderType == CTAORDER_SELL:
            so.direction = DIRECTION_SHORT
            so.offset = OFFSET_CLOSE
        elif orderType == CTAORDER_SHORT:
            so.direction = DIRECTION_SHORT
            so.offset = OFFSET_OPEN
        elif orderType == CTAORDER_COVER:
            so.direction = DIRECTION_LONG
            so.offset = OFFSET_CLOSE

            # 保存stopOrder对象到字典中
        self.stopOrderDict[stopOrderID] = so
        self.workingStopOrderDict[stopOrderID] = so

        # 推送停止单初始更新
        self.strategy.onStopOrder(so)

        return [stopOrderID]


########################################################################
class DailyResult(object):
    """每日交易的结果"""

    # ----------------------------------------------------------------------
    def __init__(self, date, closePrice):
        """Constructor"""
        self.date = date  # 日期
        self.closePrice = closePrice  # 当日收盘价
        self.previousClose = 0  # 昨日收盘价

        self.tradeList = []  # 成交列表
        self.tradeCount = 0  # 成交数量

        self.openPosition = 0  # 开盘时的持仓
        self.closePosition = 0  # 收盘时的持仓

        self.tradingPnl = 0  # 交易盈亏
        self.positionPnl = 0  # 持仓盈亏
        self.totalPnl = 0  # 总盈亏

        self.turnover = 0  # 成交量
        self.commission = 0  # 手续费
        self.slippage = 0  # 滑点
        self.netPnl = 0  # 净盈亏

    # ----------------------------------------------------------------------
    def addTrade(self, trade):
        """添加交易"""
        self.tradeList.append(trade)

    # ----------------------------------------------------------------------
    def calculatePnl(self, openPosition=0, size=1, rate=0, slippage=0):
        """
        计算盈亏
        size: 合约乘数
        rate：手续费率
        slippage：滑点点数
        """
        # 持仓部分
        self.openPosition = openPosition
        self.positionPnl = self.openPosition * (self.closePrice - self.previousClose) * size
        self.closePosition = self.openPosition

        # 交易部分
        self.tradeCount = len(self.tradeList)

        for trade in self.tradeList:
            if trade.direction == DIRECTION_LONG:
                posChange = trade.volume
            else:
                posChange = -trade.volume

            self.tradingPnl += posChange * (self.closePrice - trade.price) * size
            self.closePosition += posChange
            self.turnover += trade.price * trade.volume * size
            self.commission += trade.price * trade.volume * size * rate
            self.slippage += trade.volume * size * slippage

        # 汇总
        self.totalPnl = self.tradingPnl + self.positionPnl
        self.netPnl = self.totalPnl - self.commission - self.slippage

def main():
    from vnpy_backtest_imitation.strategyDoubleMa import DoubleMaStrategy
    self = BacktestingEngine()
    self.loadHistoryData()
    # self.initHdsClient()
    print('Hello world!!!')


if __name__ == '__main__':
    main()