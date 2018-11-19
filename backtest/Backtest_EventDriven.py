# -*- coding: UTF-8 -*-
# author:@Jack.Wang
# time :2018/8/29 19:13

"""
事件驱动型的回测
三部分
一：event_data 负责数据的推送
二：event_strategy 负责收取数据，并推送行情数据和order
三：event_backtest 负责回测数据收集，收集之后，别忘分析



"""
from backtest.Backtest_Data import dataload
from backtest.Backtest_Order_Drive import order_driven_backtest
from EventEngine.EventEngine import Event
import pandas as pd
from backtest.BackTest_Analysis import BackTestAnalysis


class event_data:
    def __init__(self, spe, begintime, endtime, periods):
        self.data_source = {}
        self.data_source['id'] = spe
        self.data_source['begintime'] = begintime
        self.data_source['endtime'] = endtime
        self.data_source['periods'] = periods
        self.event = {}

        dl = dataload(spe, begintime, endtime, periods)
        data = dl.backtest_data()
        self.data_source['data'] = data
        self.event['num'] = 0
        self.event['sum'] = len(data)

    def data_add_eventmanager(self, eventmanger):
        self.eventmanager = eventmanger

    def init(self):
        event = Event('begin')
        print('EventDriven_Backtest开始！！！！！')
        # begin  Addlistener data_begin
        self.eventmanager.SendEvent(event)



    def data_begin(self, event):
        event = Event('data_public')
        event.dict['num'] = self.event['num']
        event.dict['sum'] = self.event['sum']
        event.dict['position'] = None
        event.dict['account'] = None
        md = pd.DataFrame(self.data_source['data'].iloc[[0], :])
        md.index = [0]
        event.dict['marketdata'] = md
        print('%s of %s data 发送........' % (str(self.event['num']), str(self.event['sum'])))
        # data_public 输送至strategy_receive
        self.eventmanager.SendEvent(event)


    def data_public(self, event):
        event = Event('data_public')
        event.dict['num'] = self.event['num']
        event.dict['sum'] = self.event['sum']
        #####################################
        md = pd.DataFrame(self.data_source['data'].iloc[[self.event['num']], :])
        md.index = [0]
        #####多个品种同时推送，market就应该改为dict
        event.dict['marketdata'] = md
        event.dict['position'] = self.event['position']
        event.dict['account'] = self.event['account']
        print('%s of %s data 发送........' % (str(self.event['num']), str(self.event['sum'])))
        # data_public 输送至strategy_receive
        self.eventmanager.SendEvent(event)


    def data_receive(self, event):
        ## 收到backtest事件之后，要继续加第几根K线
        self.event['num'] = event.dict['num'] + 1
        self.event['sum'] = event.dict['sum']
        self.event['position'] = event.dict['position']
        self.event['account'] = event.dict['account']
        print('%s of %s data 收到........' % (str(self.event['num']), str(self.event['sum'])))
        event = Event('data_receive')
        # data_receive 发送至 datapublic
        self.eventmanager.SendEvent(event)


class event_strategy:
    def __init__(self):
        self.event = {}

    def strategy_add_eventmanager(self, eventmanger):
        self.eventmanager = eventmanger

    def strategy_order_new(self):
        init = pd.DataFrame(columns=['时间', '品种', '买卖', '成交价', '数量'])
        return init

    def strategy_public(self, event):
        event = Event('strategy_public')
        event.dict['num'] = self.event['num']
        event.dict['sum'] = self.event['sum']
        event.dict['marketdata'] = self.event['marketdata']
        event.dict['order'] = self.event['order']
        event.dict['position'] = self.event['position']
        event.dict['account'] = self.event['account']
        print('%s of %s strategy 发送........' % (str(self.event['num']), str(self.event['sum'])))
        self.eventmanager.SendEvent(event)


    def strategy_receive(self, event):
        self.event['num'] = event.dict['num']
        self.event['sum'] = event.dict['sum']
        self.event['marketdata'] = event.dict['marketdata']
        self.event['position'] = event.dict['position']
        self.event['account'] = event.dict['account']
        print('%s of %s strategy 收到........' % (str(self.event['num']), str(self.event['sum'])))
        self.strategy_to_order()
        event = Event('strategy_receive')
        # strategy_receive event绑定 strategy_public
        self.eventmanager.SendEvent(event)


    def strategy_to_order(self):
        # 具体策略实现
        pass

class event_backtest(order_driven_backtest):
    def __init__(self, strategy, slip, initialmoney):
        order_driven_backtest.__init__(self, strategyname=strategy, slip=slip, initial_money=initialmoney)
        self.event = {}
        self.strategyname = strategy

    def backtest_add_eventmanager(self, eventmanger):
        self.eventmanager = eventmanger

    def backtest_public(self, event):
        event = Event('backtest_public')
        event.dict['num'] = self.event['num']
        event.dict['sum'] = self.event['sum']
        event.dict['position'] = self.event['position']
        event.dict['account'] = self.event['account']
        if self.event['num'] != self.event['sum'] - 1:
            print('%s of %s backtest 发送........' % (str(self.event['num']), str(self.event['sum'])))
            self.eventmanager.SendEvent(event)
        else:
            event = Event('end')
            print('This is end. Hold your breathe and count to ten.')
            self.eventmanager.SendEvent(event)


    def backtest_receive(self, event):
        self.event['num'] = event.dict['num']
        self.event['sum'] = event.dict['sum']
        self.event['marketdata'] = event.dict['marketdata']
        self.event['order'] = event.dict['order']

        self.process_control(event.dict['marketdata'], event.dict['order'])
        self.event['position'] = self.backtest['position']
        self.event['account'] = self.backtest['account']
        print('%s of %s backtest 收到........' % (str(self.event['num']), str(self.event['sum'])))
        event = Event('backtest_receive')
        self.eventmanager.SendEvent(event)

    def backtest_end(self, event):
        print('正在分析策略回测........')
        self.backtest_record_save()
        analysis = BackTestAnalysis(self.strategyname)
        analysis.backtest_main()



if __name__ == '__main__':
    print('Done!!!')



