# -*- coding: utf-8 -*-
# author: Jack Wang

"""
数字货币的单品种 单策略回测框架
框架可容纳:
1 加减仓策略
2 单根K线多次买卖
3 中低频，不同周期K线策略
4 高频策略数据输入端需要重新整理



模仿交易所实时行情数据进行框架搭建
包括 
MarketData 市场K线数据
Order 交易订单数据
Position 持仓数据
Account 账户数据
Trade 逐笔交易汇总数据

每次推送MarketData 和 Order数据
推送过来之后
1 进行Order数据的处理
分为开仓处理和平仓处理
2 进行结算，盯市账单进行结算
"""


import configparser
import xlwt
import os
import pandas as pd
import copy

class frame_single:

    # 输入策略名称，输入合约名称，进行回测
    def __init__(self, strategy_name, instrument_name):
        config_info = configparser.ConfigParser()
        file = os.getcwd()
        file = os.path.join(file, 'config', 'info.ini')
        config_info.read(file)
        # 读取本地策略基本信息（初始资金）
        config_strategy = configparser.ConfigParser()
        file = os.getcwd()
        file = os.path.join(file, 'config', 'strategy.ini')
        config_strategy.read(file)

        self.config_info = config_info
        self.config_strategy = config_strategy

        self.marketdata_init()
        self.order_init()
        self.position_detail_init()
        initial_money = config_strategy.getint(strategy_name, 'initial_money')
        self.account_init(initial_money=initial_money)
        self.trade_init()

        self.strategy_name = strategy_name
        self.instrument_name = instrument_name

    def marketdata_init(self):
        # 市场数据，此处品种如 btc
        init = pd.DataFrame({'时间': [None],
                             '品种': [None],
                             '昨收': [None],
                             '开盘': [None],
                             '最高': [None],
                             '最低': [None],
                             '今收': [None],
                             '成交': [None],
                             '持仓': [None],
                             })
        self.marketdata = copy.deepcopy(init)
        self.marketdata_record = copy.deepcopy(init)

    def marketdata_new(self):
        # 市场数据，此处品种如 btc
        init = pd.DataFrame({'时间': [None],
                             '品种': [None],
                             '昨收': [None],
                             '开盘': [None],
                             '最高': [None],
                             '最低': [None],
                             '今收': [None],
                             '成交': [None],
                             '持仓': [None],
                             })
        md = copy.deepcopy(init)
        return md

    def order_init(self):
        init = pd.DataFrame({'时间': [None], '品种': [None], '买卖': [None],
                             '成交价': [None], '数量': [None]})
        self.order = copy.deepcopy(init)
        self.order_record = copy.deepcopy(init)

    def order_new(self):
        init = pd.DataFrame(columns=['时间', '品种', '买卖', '成交价', '数量'])
        return init

    def position_detail_init(self):
        init = pd.DataFrame({'时间': [None],
                             '品种': [None],
                             '开仓时间': [None],
                             '是否今仓': [None],
                             '盯开盘': [None],
                             '多空': [None],
                             '数量': [None],
                             '开仓价': [None],
                             '昨收': [None],
                             '今收': [None],
                             '逐笔盈亏': [None],
                             '盯市盈亏': [None],
                             '市值': [None],
                             })
        self.position = copy.deepcopy(init)
        self.position_record = copy.deepcopy(init)

    def position_detail_new(self):
        init = pd.DataFrame({'时间': [None],
                             '品种': [None],
                             '开仓时间': [None],
                             '是否今仓': [None],
                             '盯开盘': [None],
                             '多空': [None],
                             '数量': [None],
                             '开仓价': [None],
                             '昨收': [None],
                             '今收': [None],
                             '逐笔盈亏': [None],
                             '盯市盈亏': [None],
                             '市值': [None],
                             })
        return init

    def account_init(self, initial_money):  # 初始化一个account
        init = pd.DataFrame({'时间': [None],
                             '期初': initial_money,
                             '平盯昨盈亏': 0,
                             '平盯今盈亏': 0,
                             '平仓盈亏': 0,
                             '盯昨盈亏': 0,
                             '盯今盈亏': 0,
                             '盯市盈亏': 0,
                             '手续费': 0,
                             '期末': 0,
                             '可用资金': 0,
                             '风险度': 0,
                             '多头市值': 0,
                             '空头市值': 0,
                             '市值': 0,
                             })
        self.account = copy.deepcopy(init)
        self.account_record = copy.deepcopy(init)

    def trade_init(self):
        init = pd.DataFrame({'品种': [None],
                             '开仓时间': [None],
                             '开仓操作': [None],
                             '开仓价': [None],
                             '开仓数量': [None],
                             '平仓时间': [None],
                             '平仓操作': [None],
                             '平仓价': [None],
                             '平仓数量': [None],
                             '手续费': [None],
                             '是否平今': [None],
                             '平仓盈亏': [None],
                             '净盈亏': [None],
                             '逐笔累计盈利': 0})

        self.trade = copy.deepcopy(init)

    # 策略主循环，外部接口
    def main_loop(self, md, order):
        self.marketdata = copy.deepcopy(md)
        self.order = copy.deepcopy(order)
        # 1 记录marketdata到marketdata_record
        self.marketdata_record = self.marketdata_record.append(self.marketdata)

        # 注：order在这部分可能出现长度为0的情况，此时，不进行下面的循环
        for i in range(0, len(order)):
            order_min = order.loc[i, :]
            # 2 根据order情况，进行order_record更新
            self.order_record = self.order_record.append(order_min)
            if order_min['买卖'] == '买开' or order_min['买卖'] == '卖开':
                # 处理开仓情况  position变动
                self.process_open(order_min)
            elif order_min['买卖'] == '卖平' or order_min['买卖'] == '买平':
                # 处理平仓情况 trade变动 account变动 position变动
                self.process_closeposition(order_min)
            else:
                print('order 格式非标准，请重新输入order')

        # 更新仓位加减，多次操作之后，进行收盘价结算，position盯市 account盯市、期末计算
        self.close_settle()
        # 修改新开仓位盯开盘的情况
        self.position['盯开盘'] = '否'
        # 修改是否今仓
        self.position['是否今仓'] = '否'

    # 处理开仓的情况
    def process_open(self, order):
        # 开仓，分两种，一种是此时无持仓，记录相关信息，一种是此时有信息，需要加入信息

        slip = self.config_info.getfloat(self.instrument_name, 'slip')
        commission = self.config_info.getfloat(self.instrument_name, 'commission_open')
        last_p = self.marketdata['昨收'][0]
        toda_p = self.marketdata['今收'][0]
        time = order['时间']
        instrument = order['品种']
        num = order['数量']
        price = order['成交价']

        position = copy.deepcopy(self.position)
        # 当前无持仓，则记录
        if position.loc[0, '品种'] == None:
            position.loc[0, '时间'] = time
            position.loc[0, '品种'] = instrument
            position.loc[0, '开仓时间'] = time
            position.loc[0, '是否今仓'] = '是'
            position.loc[0, '盯开盘'] = '是'
            if order['买卖'] == '买开':
                position.loc[0, '多空'] = '多'
            elif order['买卖'] == '卖开':
                position.loc[0, '多空'] = '空'
            position.loc[0, '数量'] = num
            if position.loc[0, '多空'] == '多':
                position.loc[0, '开仓价'] = price + slip
            elif position.loc[0, '多空'] == '空':
                position.loc[0, '开仓价'] = price - slip
            position.loc[0, '昨收'] = last_p
            position.loc[0, '今收'] = toda_p
            position.loc[0, '手续费'] = num * position.loc[0, '开仓价'] * commission
            # 先不结算
            position.loc[0, '逐笔盈亏'] = 0
            position.loc[0, '盯市盈亏'] = 0
            position.loc[0, '市值'] = 0
        # 当前已有仓位
        else:
            ind = len(position)
            position.loc[ind, '时间'] = time
            position.loc[ind, '品种'] = instrument
            position.loc[ind, '开仓时间'] = time
            position.loc[ind, '是否今仓'] = '是'
            position.loc[ind, '盯开盘'] = '是'
            if order['买卖'] == '买开':
                position.loc[ind, '多空'] = '多'
            elif order['买卖'] == '卖开':
                position.loc[ind, '多空'] = '空'
            position.loc[ind, '数量'] = num
            if position.loc[ind, '多空'] == '多':
                position.loc[ind, '开仓价'] = price + slip
            elif position.loc[ind, '多空'] == '空':
                position.loc[ind, '开仓价'] = price - slip
            position.loc[ind, '昨收'] = last_p
            position.loc[ind, '今收'] = toda_p
            position.loc[0, '手续费'] = num * position.loc[ind, '开仓价'] * commission
            # 先不结算
            position.loc[ind, '逐笔盈亏'] = 0
            position.loc[ind, '盯市盈亏'] = 0
            position.loc[ind, '市值'] = 0

        # position_record记录
        self.position = copy.deepcopy(position)

    # 处理平仓的情况
    def process_closeposition(self, order):
        """
        order + position
        改变position
        改变account
        """

        instrument = order['品种']
        if order['买卖'] == '卖平':
            posi = self.position.loc[(self.position['多空'] == '多')]

        elif order['买卖'] == '买平':
            posi = self.position.loc[(self.position['多空'] == '空')]

        # 计算所需要的平掉的哪些个仓位,平仓是按建仓时间顺序来的
        ind = len(posi.index)
        order_num = order['数量']
        i = 0
        while i < ind:
            order_num = order_num - posi.loc[posi.index[i], '数量']
            if order_num <= 0:
                ind = i + 1
                break
            else:
                i = i + 1
                if i == ind:
                    print('平掉太多仓了，错误！！！')
        # 根据所需的平仓, 记录trade
        t_len = len(self.trade)
        order_num = order['数量']
        for i1 in range(0, ind):  # i1 + t_len 定位trade
            i = posi.index[i1]  # i 定位posi
            c_fx_t = self.config_info.getfloat(self.instrument_name, 'commission_close')
            slip = self.config_strategy.getfloat(self.instrument_name, 'slip')
            num = posi.loc[i, '数量'] # 这个数量是持仓详细中这个仓位的数量

            self.trade.loc[t_len + i1, '品种'] = instrument
            self.trade.loc[t_len + i1, '开仓时间'] = posi.loc[i, '开仓时间']
            if posi.loc[i, '多空'] == '多':
                self.trade.loc[t_len + i1, '开仓操作'] = '买开'
            elif posi.loc[i, '多空'] == '空':
                self.trade.loc[t_len + i1, '开仓操作'] = '卖开'
            self.trade.loc[t_len + i1, '开仓价'] = posi.loc[i, '开仓价']
            self.trade.loc[t_len + i1, '开仓数量'] = posi.loc[i, '数量']
            if i1 == ind - 1:
                self.trade.loc[t_len + i1, '开仓数量'] = order_num
                num = order_num
            self.trade.loc[t_len + i1, '平仓时间'] = order['时间']
            self.trade.loc[t_len + i1, '平仓操作'] = order['买卖']
            if self.trade.loc[t_len + i1, '开仓操作'] == '买开':
                self.trade.loc[t_len + i1, '平仓价'] = order['成交价'] - slip
            elif self.trade.loc[t_len + i1, '开仓操作'] == '卖开':
                self.trade.loc[t_len + i1, '平仓价'] = order['成交价'] + slip
            closeprice = self.trade.loc[t_len + i1, '平仓价']
            self.trade.loc[t_len + i1, '平仓数量'] = self.trade.loc[t_len + i1, '开仓数量']
            self.trade.loc[t_len + i1, '是否平今'] = posi.loc[i, '是否今仓']
            self.trade.loc[t_len + i1, '盯开盘'] = posi.loc[i, '盯开盘']
            # 手续费
            if posi.loc[i, '是否今仓'] == '是':
                self.trade.loc[t_len + i1, '手续费'] = num * c_fx_t + \
                                                    num * trading_unit * closeprice * c_ft_t
            else:
                self.trade.loc[t_len + i1, '手续费'] = num * c_fx + \
                                                    num * trading_unit * closeprice * c_ft
            commission = self.trade.loc[t_len + i1, '手续费']
            # 平仓盈亏计算
            self.trade.loc[t_len + i1, '平仓盈亏'] = num * trading_unit * (closeprice - posi.loc[i, '开仓价'])
            if posi.loc[i, '多空'] == '空':
                self.trade.loc[t_len + i1, '平仓盈亏'] = -self.trade.loc[t_len + i1, '平仓盈亏']
            close_p_l = self.trade.loc[t_len + i1, '平仓盈亏']
            # 净盈亏
            self.trade.loc[t_len + i1, '净盈亏'] = close_p_l - commission
            if t_len + i1 != 0:
                self.trade.loc[t_len + i1, '逐笔累计盈利'] = self.trade.loc[
                                                           t_len + i1 - 1, '逐笔累计盈利'] + \
                                                       self.trade.loc[t_len + i1, '净盈亏']
            else:
                self.trade.loc[t_len + i1, '逐笔累计盈利'] = self.trade.loc[t_len + i1, '逐笔累计盈利'] + \
                                                       self.trade.loc[t_len + i1, '净盈亏']
            # ===========记录Account 平仓盈亏和手续费=============
            # 获得该品种昨日收盘价
            marketdata = self.marketdata
            lastprice = marketdata[marketdata['品种'] == order['品种']]['昨收'][0]
            # 盯盘盈亏，用于
            if order['买卖'] == '卖平':
                close_sting = num * trading_unit * (closeprice - lastprice)
            elif order['买卖'] == '买平':
                close_sting = num * trading_unit * (lastprice - closeprice)

            if posi.loc[i, '盯开盘'] == '是':
                self.account.loc[0, '平盯今盈亏'] += close_sting
            else:
                self.account.loc[0, '平盯昨盈亏'] += close_sting

            self.account.loc[0, '手续费'] += commission
            # 记录完一次操作，要把trade里面的order的数量更新下
            order_num = order_num - posi.loc[i, '数量']
            self.position.loc[i, '数量'] = self.position.loc[i, '数量'] - \
                                         self.trade.loc[t_len + i1, '平仓数量']

        # 删除品种是None的逐笔交易记录,只有第一次删除，需要reset_index
        if self.trade.loc[0, '品种'] == None:
            self.trade = self.trade.drop([0])
            self.trade = self.trade.reset_index(drop=True)

        # 删除持仓详细数量为0的持仓
        self.position = self.position.loc[self.position['数量'] != 0]
        self.position = self.position.reset_index(drop=True)

        # 如果把所有持仓全部删除了，那么就再给持仓一个初值
        if len(self.position) == 0:
            self.position = self.position_detail_new()



def main():
    print('Hello world')


if __name__ == '__main__':
    main()


