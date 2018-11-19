# -*- coding: UTF-8 -*-
# author:@Jack.Wang
# time :2018/8/30 23:56

from backtest.Backtest_EventDriven import event_data, event_strategy, event_backtest
from strategy.jma_event import jmavalue
from EventEngine.EventEngine import EventManager
import pandas as pd



class jma_strategy(event_strategy, jmavalue):
    def __init__(self, dic):
        event_strategy.__init__(self)
        self.jmafast = jmavalue(dic['fastLength'], dic['fastphase'])
        self.jmaslow = jmavalue(dic['slowLength'], dic['slowphase'])

    def strategy_to_order(self):
        # 提取数据
        marketdata = pd.DataFrame(self.event['marketdata'])
        data = marketdata['今收'][0]
        position = pd.DataFrame(self.event['position'])
        account = pd.DataFrame(self.event['account'])
        # 初始化order
        order = self.strategy_order_new()
        ###########################################################
        # 快慢线计算
        self.jmafast.jma_calculate(data)
        self.jmaslow.jma_calculate(data)
        # 以固定2倍杠杆交易
        if len(account) != 0:
            money = account['期初'][0]

        # order计算
        # 过滤掉前199根K线，由于算法，导致前面的数据可信度不高
        len(self.jmafast.jma['data'])
        if len(self.jmafast.jma['data']) >= 100:
            # 首次处理
            if len(self.jmafast.jma['data']) == 100:
                if self.jmaslow.jma['JMAValueBuffer'][-1] > self.jmafast.jma['JMAValueBuffer'][-1]:
                    order.loc[0, '时间'] = marketdata.loc[0, '时间']
                    order.loc[0, '品种'] = marketdata.loc[0, '品种']
                    order.loc[0, '买卖'] = '卖开'
                    order.loc[0, '成交价'] = marketdata.loc[0, '今收']
                    order.loc[0, '数量'] = 100
                if self.jmafast.jma['JMAValueBuffer'][-1] > self.jmaslow.jma['JMAValueBuffer'][-1]:
                    order.loc[0, '时间'] = marketdata.loc[0, '时间']
                    order.loc[0, '品种'] = marketdata.loc[0, '品种']
                    order.loc[0, '买卖'] = '买开'
                    order.loc[0, '成交价'] = marketdata.loc[0, '今收']
                    order.loc[0, '数量'] = 100

            if position.loc[0, '多空'] == '多':
                if self.jmaslow.jma['JMAValueBuffer'][-1] > self.jmafast.jma['JMAValueBuffer'][-1]:
                    order.loc[0, '时间'] = marketdata.loc[0, '时间']
                    order.loc[0, '品种'] = marketdata.loc[0, '品种']
                    order.loc[0, '买卖'] = '卖平'
                    order.loc[0, '成交价'] = marketdata.loc[0, '今收']
                    order.loc[0, '数量'] = 100
                    order.loc[1, '时间'] = marketdata.loc[0, '时间']
                    order.loc[1, '品种'] = marketdata.loc[0, '品种']
                    order.loc[1, '买卖'] = '卖开'
                    order.loc[1, '成交价'] = marketdata.loc[0, '今收']
                    order.loc[1, '数量'] = 100
            if position.loc[0, '多空'] == '空':
                if self.jmafast.jma['JMAValueBuffer'][-1] > self.jmaslow.jma['JMAValueBuffer'][-1]:
                    order.loc[0, '时间'] = marketdata.loc[0, '时间']
                    order.loc[0, '品种'] = marketdata.loc[0, '品种']
                    order.loc[0, '买卖'] = '买平'
                    order.loc[0, '成交价'] = marketdata.loc[0, '今收']
                    order.loc[0, '数量'] = 100
                    order.loc[1, '时间'] = marketdata.loc[0, '时间']
                    order.loc[1, '品种'] = marketdata.loc[0, '品种']
                    order.loc[1, '买卖'] = '买开'
                    order.loc[1, '成交价'] = marketdata.loc[0, '今收']
                    order.loc[1, '数量'] = 100
            # 最后一根处理
            if self.event['num'] == self.event['sum']:
                if position.loc[0, '多空'] == '多':
                    order.loc[0, '时间'] = marketdata.loc[0, '时间']
                    order.loc[0, '品种'] = marketdata.loc[0, '品种']
                    order.loc[0, '买卖'] = '卖平'
                    order.loc[0, '成交价'] = marketdata.loc[0, '今收']
                    order.loc[0, '数量'] = 100
                if position.loc[0, '多空'] == '空':
                    order.loc[0, '时间'] = marketdata.loc[0, '时间']
                    order.loc[0, '品种'] = marketdata.loc[0, '品种']
                    order.loc[0, '买卖'] = '买平'
                    order.loc[0, '成交价'] = marketdata.loc[0, '今收']
                    order.loc[0, '数量'] = 100
        #############################################################

        self.event['order'] = pd.DataFrame(order)


def mytest():
    # 数据参数
    spe = 'ta'
    begintime = '2014-12-12 21:00:00'
    endtime = '2018-08-21 15:30:00'
    periods = 'D'
    # 策略参数
    strategy = 'jma_ta'
    slip = 1
    initialmoney = 1000000
    # 策略参数
    stradict = {}
    stradict['slowLength'] = 21
    stradict['slowphase'] = 101
    stradict['fastLength'] = 10
    stradict['fastphase'] = 101

    da = event_data(spe, begintime, endtime, periods)
    bt = event_backtest(strategy, slip, initialmoney)
    jm = jma_strategy(stradict)

    eventmanger = EventManager()
    eventmanger.AddEventLister('begin', da.data_begin)
    eventmanger.AddEventLister('data_public', jm.strategy_receive)
    eventmanger.AddEventLister('data_receive', da.data_public)
    eventmanger.AddEventLister('strategy_public', bt.backtest_receive)
    eventmanger.AddEventLister('strategy_receive', jm.strategy_public)
    eventmanger.AddEventLister('backtest_public', da.data_receive)
    eventmanger.AddEventLister('backtest_receive', bt.backtest_public)
    eventmanger.AddEventLister('end', bt.backtest_end)
    eventmanger.Start()

    da.data_add_eventmanager(eventmanger)
    bt.backtest_add_eventmanager(eventmanger)
    jm.strategy_add_eventmanager(eventmanger)

    da.init()



if __name__ == '__main__':
    mytest()