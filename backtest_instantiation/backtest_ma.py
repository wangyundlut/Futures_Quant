# -*- coding: UTF-8 -*-
# author:@Jack.Wang
# time :2018/8/30 23:56

from backtest.Backtest_EventDriven import event_data, event_strategy, event_backtest
from strategy.ma_event import strategy_ma
from EventEngine.EventEngine import EventManager
import pandas as pd
from data_get_save.futures_info import futures_info
import math
import time


class backtest_ma(event_strategy, strategy_ma):
    def __init__(self, dic):
        event_strategy.__init__(self)
        self.info = dic['info'] # 传入品种信息
        self.mavalue = strategy_ma(dic['fast_index'], dic['slow_index'])

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
        self.mavalue.ma_calculate(data)


        # order计算
        # 过滤掉前slow_index根K线，由于算法，导致前面的数据可信度不高
        datalen = len(self.mavalue.data)
        if datalen >= self.mavalue.slow_index:
            # 计算仓位：以固定2倍杠杆交易
            open_num = math.floor(account['期初'][0]*2/data/self.info['trading_unit'])
            # 首次处理
            if datalen == self.mavalue.slow_index:
                if self.mavalue.slow_ma[-1] >= self.mavalue.fast_ma[-1]:
                    order.loc[0, '时间'] = marketdata.loc[0, '时间']
                    order.loc[0, '品种'] = marketdata.loc[0, '品种']
                    order.loc[0, '买卖'] = '卖开'
                    order.loc[0, '成交价'] = marketdata.loc[0, '今收']
                    order.loc[0, '数量'] = open_num
                if self.mavalue.slow_ma[-1] < self.mavalue.fast_ma[-1]:
                    order.loc[0, '时间'] = marketdata.loc[0, '时间']
                    order.loc[0, '品种'] = marketdata.loc[0, '品种']
                    order.loc[0, '买卖'] = '买开'
                    order.loc[0, '成交价'] = marketdata.loc[0, '今收']
                    order.loc[0, '数量'] = open_num

            if position.loc[0, '多空'] == '多':
                now_num = position['数量'][0]
                if self.mavalue.slow_ma[-1] >= self.mavalue.fast_ma[-1]:
                    order.loc[0, '时间'] = marketdata.loc[0, '时间']
                    order.loc[0, '品种'] = marketdata.loc[0, '品种']
                    order.loc[0, '买卖'] = '卖平'
                    order.loc[0, '成交价'] = marketdata.loc[0, '今收']
                    order.loc[0, '数量'] = now_num
                    order.loc[1, '时间'] = marketdata.loc[0, '时间']
                    order.loc[1, '品种'] = marketdata.loc[0, '品种']
                    order.loc[1, '买卖'] = '卖开'
                    order.loc[1, '成交价'] = marketdata.loc[0, '今收']
                    order.loc[1, '数量'] = open_num
            if position.loc[0, '多空'] == '空':
                now_num = position['数量'][0]
                if self.mavalue.slow_ma[-1] < self.mavalue.fast_ma[-1]:
                    order.loc[0, '时间'] = marketdata.loc[0, '时间']
                    order.loc[0, '品种'] = marketdata.loc[0, '品种']
                    order.loc[0, '买卖'] = '买平'
                    order.loc[0, '成交价'] = marketdata.loc[0, '今收']
                    order.loc[0, '数量'] = now_num
                    order.loc[1, '时间'] = marketdata.loc[0, '时间']
                    order.loc[1, '品种'] = marketdata.loc[0, '品种']
                    order.loc[1, '买卖'] = '买开'
                    order.loc[1, '成交价'] = marketdata.loc[0, '今收']
                    order.loc[1, '数量'] = open_num
            # 最后一根处理
            if self.event['num'] == self.event['sum']:
                now_num = position['数量'][0]
                if position.loc[0, '多空'] == '多':
                    order.loc[0, '时间'] = marketdata.loc[0, '时间']
                    order.loc[0, '品种'] = marketdata.loc[0, '品种']
                    order.loc[0, '买卖'] = '卖平'
                    order.loc[0, '成交价'] = marketdata.loc[0, '今收']
                    order.loc[0, '数量'] = now_num
                if position.loc[0, '多空'] == '空':
                    order.loc[0, '时间'] = marketdata.loc[0, '时间']
                    order.loc[0, '品种'] = marketdata.loc[0, '品种']
                    order.loc[0, '买卖'] = '买平'
                    order.loc[0, '成交价'] = marketdata.loc[0, '今收']
                    order.loc[0, '数量'] = now_num
        #############################################################

        self.event['order'] = pd.DataFrame(order)


def mytest():
    # 数据参数
    spe_list = ['ta','m','rb','v','ru','cu','j']
    # spe_list = ['m', 'rb', 'v', 'ru', 'cu', 'j']
    time_list = [['2014-12-12 21:00:00','2018-08-21 15:30:00'],
                 ['2014-12-26 21:00:00','2018-08-21 15:30:00'],
                 ['2014-12-26 21:00:00','2018-08-21 15:30:00'],
                 ['2009-05-25 09:00:00','2018-08-21 15:30:00'],
                 ['2014-12-26 09:00:00','2018-08-21 15:30:00'],
                 ['2013-12-20 21:00:00','2018-08-21 15:30:00'],
                 ['2014-07-04 21:00:00','2018-08-21 15:30:00'],
                 ]
    strategy_list = [[3,5,7,9,11,13],[20,25,30,40,60,80,100]]
    for spe in spe_list:
        for begintime, endtime in time_list:
            for fast in strategy_list[0]:
                for slow in strategy_list[1]:
                    strategy = 'ma_' + spe + '_' + str(fast) + '-' + str(slow)
                    f_info = futures_info()
                    commodity_info, finance_info, info = f_info.futures_info()
                    info = info[spe]

                    stradict = {}
                    stradict['info'] = info
                    stradict['fast_index'] = fast
                    stradict['slow_index'] = slow

                    initialmoney = 1000000

                    # 获取数据
                    da = event_data(spe, begintime, endtime, 'D')
                    # 获取回测框架
                    bt = event_backtest(strategy, info['min_change']*2, initialmoney)
                    # 获取策略
                    jm = backtest_ma(stradict)

                    eventmanger = EventManager()
                    eventmanger.AddEventLister('begin', da.data_begin)
                    eventmanger.AddEventLister('data_public', jm.strategy_receive)
                    eventmanger.AddEventLister('data_receive', da.data_public)
                    eventmanger.AddEventLister('strategy_public', bt.backtest_receive)
                    eventmanger.AddEventLister('strategy_receive', jm.strategy_public)
                    eventmanger.AddEventLister('backtest_public', da.data_receive)
                    eventmanger.AddEventLister('backtest_receive', bt.backtest_public)
                    eventmanger.AddEventLister('end', bt.backtest_end)
                    # 绑定好之后，运行事件管理器
                    eventmanger.Start()

                    da.data_add_eventmanager(eventmanger)
                    bt.backtest_add_eventmanager(eventmanger)
                    jm.strategy_add_eventmanager(eventmanger)

                    da.init()

                    time.sleep(300)



if __name__ == '__main__':
    mytest()
    print('Done')