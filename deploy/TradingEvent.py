# -*- coding: UTF-8 -*-
# author:@Jack.Wang
# time :2018/8/31 21:26

from EventEngine.EventEngine import EventManager, Event
from data_get_save.PostgreSQL import PostgreSQL
from data_get_save.kline_process import kline_process
from strategy.jma_event import jmavalue
import pandas as pd
from ctp.md_api_mine import ly_ctpmd





class trading_order:
    def __init__(self, posi_dict):
        self.event = {}
        self.event['position'] = posi_dict

    def order_add_eventmanager(self, eventmanger):
        self.eventmanager = eventmanger

    def order_begin(self, event):
        pass # 策略需要给初始的order情况，交易所的order并没有记录实际的order状况


    def order_public(self):
        event = Event('strategy_public')
        self.eventmanager.SendEvent(event)

    def order_receive(self, event):
        event = Event('strategy_receive')
        self.eventmanager.SendEvent(event)

    def order_end(self):
        # 具体策略实现
        pass

class trading_data(PostgreSQL, kline_process):
    def __init__(self, data_dict):
        PostgreSQL.__init__(self, 'futures_min')
        kline_process.__init__(self)
        self.data = data_dict

    def data_add_eventmanager(self, eventmanger):
        self.eventmanager = eventmanger

    # 交易总接口
    def data_init(self, event):
        event = Event('start')
        self.eventmanager.SendEvent(event)

    def data_begin(self, event):
        # 读取本地数据
        data = self.minute_select(self.data['instrument'])
        data = pd.DataFrame(data, columns=['时间', '开盘价', '最高价', '最低价', '收盘价', '成交量', '持仓量'])
        data.set_index(data['时间'], inplace=True)
        # 时间筛选
        data = data[(data.index >= self.data['time_begin'])]
        data = data[(data.index <= self.data['time_end'])]
        # k线合成
        data = self.minute_combine(data, self.data['periods'])
        # 本地数据准备
        self.data['data'] = data
        print('===================Trading_Event_Driven: data begin===================')
        # 本地数据准备好了之后，就开始进行实盘事件驱动
        event = Event('data_begin')
        ly_ctpmd(contract=event.dict['instrument'])
        event.dict['data'] = data
        self.eventmanager.SendEvent(event)




    def data_public(self, event):
        # 数据循环发布
        event = Event('data_public')
        self.eventmanager.SendEvent(event)


    def data_receive(self, event):
        # order处理之后，数据可以进一步
        print('初始化全部完成，数据循环播报')
        event = Event('data_receive')
        self.eventmanager.SendEvent(event)

class trading_strategy:
    def __init__(self, stra_dict):
        self.event = stra_dict

    def strategy_add_eventmanager(self, eventmanger):
        self.eventmanager = eventmanger

    def strategy_begin(self, event):
        pass # 策略具体实现

    def strategy_public(self):
        event = Event('strategy_public')
        self.eventmanager.SendEvent(event)

    def strategy_receive(self, event):

        # 收到数据后，先进行策略_to_order的处理
        self.strategy_to_order()
        event = Event('strategy_receive')
        self.eventmanager.SendEvent(event)

    def strategy_to_order(self):
        pass # 具体策略实现

class strategy_jma(trading_strategy):
    def __init__(self, stra_dict):
        trading_strategy.__init__(self, stra_dict)

    def strategy_begin(self, event):
        data = event.dict['data']
        # 将数据转成所需要的类型
        data = data['收盘价'].tolist()
        # 将数据转换成策略所需要的类型
        jmafast = jmavalue(self.event['slowLength'], self.event['slowphase'])
        jmaslow = jmavalue(self.event['fastLength'], self.event['fastphase'])
        for i in range(len(data)):
            d = data[i]
            jmafast.jma_calculate(d)
            jmaslow.jma_calculate(d)
        print('===================Trading_Event_Driven: strategy begin===============')
        event = Event('strategy_begin')
        self.eventmanager.SendEvent(event)

class order_jma(trading_order):
    def __init__(self, posi_dict):
        trading_order.__init__(self, posi_dict)

    def order_begin(self, event):

        print('===================Trading_Event_Driven: order begin==================')
        event = Event('order_begin')
        self.eventmanager.SendEvent(event)

def mytest():
    data_dict = {'contract_list': ['j1901', 'j1905']}
    data_dict = {'id': 'j', 'instrument': 'j1901', 'periods': '30min',
                 'time_begin': '2018-03-01 21:00:00', 'time_end': '2018-08-31 23:29:00'}
    stra_dict = {'name': 'jma', 'slowLength': 21, 'slowphase': 101, 'fastLength': 10, 'fastphase': 101}
    orde_dict = {}
    trad_dict = {}
    posi_dict = {}

    data = trading_data(data_dict)
    jma=strategy_jma(stra_dict)
    order = order_jma(posi_dict)


    eventmanger = EventManager()
    eventmanger.AddEventLister('start', data.data_begin)
    eventmanger.AddEventLister('data_begin', jma.strategy_begin)
    eventmanger.AddEventLister('strategy_begin', order.order_begin)
    eventmanger.AddEventLister('order_begin', data.data_receive)
    """
    eventmanger.AddEventLister('td_data_public', jma.strategy_receive)
    eventmanger.AddEventLister('td_data_receive', data.data_public)
    eventmanger.AddEventLister('td_strategy_public', order.trading_order_receive)
    eventmanger.AddEventLister('td_strategy_receive', jma.trading_strategy_public)
    eventmanger.AddEventLister('td_order_public', data.trading_data_receive)
    eventmanger.AddEventLister('td_order_receive', order.trading_order_public)
    eventmanger.AddEventLister('td_end', order.trading_order_end)
    """
    eventmanger.Start()

    data.data_add_eventmanager(eventmanger)
    jma.strategy_add_eventmanager(eventmanger)
    order.order_add_eventmanager(eventmanger)

    event = Event('start')
    event.dict['instrument'] = ['j1901']
    data.data_init(event)

if __name__ == '__main__':
    mytest()
