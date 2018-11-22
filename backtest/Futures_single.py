#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author     : Jack


"""
多策略单品种的CTA策略回测框架
Futures_single

订单驱动型回测系统
主要模仿交易所的逐日盯市 + 逐笔账单来制定回测系统
包括MarketData Order position Positions  Account_Summary Trade_Summary期货账单六部分
MarketData 模仿行情推送
Order Order定制
PositionDetail 逐日持仓详情
Positions 逐日持仓汇总
account 逐日账单汇总
Trade_Summary 逐笔订单
通过六部分的组合，构建所有策略的回测系统

使用方法：
初始化：
初始化市场行情等几部分，随后用于记录
每个推送给order_driven_backtest 一个市场数据，格式固定，一个order的组合（可为空），格式固定，由此，完成策略回测

1 将futures的info部分写入config
2 将strategy的info demo部分写入config
3 手续费不再考虑今仓和老仓，开发中低频交易策略为主，今仓和老仓可以通过持仓加大对冲来解决
4 手续费不再考虑单边双边，一律按平仓时收取手续费，交易所1.5倍标准（中低频策略，手续费影响不大）
"""

import configparser
import xlwt
import os
import pandas as pd
import copy

class Futures_single:
    def __init__(self, instrument):
        # 品种名称用来本地调用数据,例如 rb
        # 读取本地期货品种信息
        config_info = configparser.ConfigParser()
        file = os.getcwd()
        file = os.path.join(os.path.dirname(file), 'config', 'futures_info.ini')
        config_info.read(file)
        # 读取本地策略基本信息（初始资金）
        config_strategy = configparser.ConfigParser()
        file = os.getcwd()
        file = os.path.join(os.path.dirname(file), 'config', 'strategy.ini')
        config_strategy.read(file)

        self.config_info = config_info
        self.config_strategy = config_strategy

        self.marketdata_init()
        self.order_init()
        self.position_detail_init()
        initial_money = config_strategy.getint('common', 'initial_money')
        self.account_init(initial_money=initial_money)
        self.trade_init()

        self.instrument = instrument

    def marketdata_init(self):
        # 市场数据，此处品种如 j rb
        init = pd.DataFrame({'时间': [None],
                             '品种': [None],
                             '昨收': [None],
                             '开盘': [None],
                             '最高': [None],
                             '最低': [None],
                             '今收': [None],
                             '成交量': [None],
                             '持仓量': [None],
                             })
        self.marketdata = copy.deepcopy(init)
        self.marketdata_record = copy.deepcopy(init)

    def marketdata_new(self):
        init = pd.DataFrame({'时间': [None],
                             '品种': [None],
                             '昨收': [None],
                             '开盘': [None],
                             '最高': [None],
                             '最低': [None],
                             '今收': [None],
                             '成交量': [None],
                             '持仓量': [None],
                             })
        md = copy.deepcopy(init)
        return md

    def order_init(self):
        init = pd.DataFrame({'时间': [None], '品种': [None], '买卖': [None], '成交价': [None],
                             '数量': [None]})
        self.order = copy.deepcopy(init)
        self.order_record = copy.deepcopy(init)

    def order_new(self):
        init = pd.DataFrame(columns=['时间', '品种', '买卖', '成交价', '数量'])
        return init

    def position_detail_init(self):
        init = pd.DataFrame({'时间': [None],
                             '品种': [None],
                             '开仓时间': [None],
                             '盯开盘': [None],
                             '多空': [None],
                             '数量': [None],
                             '开仓价': [None],
                             '昨收': [None],
                             '今收': [None],
                             '逐笔盈亏': [None],
                             '盯市盈亏': [None],
                             '市值': [None],
                             '保证金': [None]})
        self.position = copy.deepcopy(init)
        self.position_record = copy.deepcopy(init)

    def position_detail_new(self):
        init = pd.DataFrame({'时间': [None],
                             '品种': [None],
                             '开仓时间': [None],
                             '盯开盘': [None],
                             '多空': [None],
                             '数量': [None],
                             '开仓价': [None],
                             '昨收': [None],
                             '今收': [None],
                             '逐笔盈亏': [None],
                             '盯市盈亏': [None],
                             '市值': [None],
                             '保证金': [None]})
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
                             '保证金': 0,
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
                             '盯开盘': [None],
                             '手续费': [None],
                             '平仓盈亏': [None],
                             '净盈亏': [None],
                             '逐笔累计盈利': 0})

        self.trade = copy.deepcopy(init)

    def backtest_loop(self, md, order):
        # 单策略，单品种的回测，支持加减仓，支持单根K线多次操作（例如反手）
        # 主循环部分，循环输入市场行情，以及建仓加仓操作等
        self.marketdata = copy.deepcopy(md)
        self.order = copy.deepcopy(order)
        # 首先将marketdata_record更新
        self.marketdata_record = self.marketdata_record.append(self.marketdata)
        # 根据order的情况，进行开平仓的操作
        # 注：order在这部分可能出现长度为0的情况，此时，不进行下面的循环
        for i in range(0, len(order)):
            order_min = order.loc[i,:]
            # 记录order_min
            self.order_record = self.order_record.append(order_min)
            if order_min['买卖'] == '买开' or order_min['买卖'] == '卖开':
                self.process_open(order_min)
            elif order_min['买卖'] == '卖平' or order_min['买卖'] == '买平':
                self.process_close(order_min)
            else:
                print('order 格式非标准，请重新输入order')

        # 更新仓位加减，多次操作之后，进行收盘价结算
        self.settle()
        # 修改新开仓位盯开盘的情况
        self.position['盯开盘'] = '否'

    # 处理开仓的情况
    def process_open(self, order):
        """
        开仓，改变self.position
        结算时，记录position到position_record
        :param order: 订单
        :return: 以self的形式return
        """
        slip = self.config_info.getfloat(self.instrument, 'slip') # 滑点，滑点和策略相关，也和品种相关
        last_p = self.marketdata['昨收'][0]
        toda_p = self.marketdata['今收'][0]

        position = copy.deepcopy(self.position)
        # 当前无持仓，则记录
        if position.loc[0, '品种'] == None:
            position.loc[0, '时间'] = order['时间']
            position.loc[0, '品种'] = order['品种']
            position.loc[0, '开仓时间'] = order['时间']
            position.loc[0, '盯开盘'] = '是'
            if order['买卖'] == '买开':
                position.loc[0, '多空'] = '多'
            elif order['买卖'] == '卖开':
                position.loc[0, '多空'] = '空'
            position.loc[0, '数量'] = order['数量']
            if position.loc[0, '多空'] == '多':
                position.loc[0, '开仓价'] = order['成交价'] + slip
            elif position.loc[0, '多空'] == '空':
                position.loc[0, '开仓价'] = order['成交价'] - slip
            position.loc[0, '昨收'] = last_p
            position.loc[0, '今收'] = toda_p
            # 先不结算
            position.loc[0, '逐笔盈亏'] = 0
            position.loc[0, '盯市盈亏'] = 0
            position.loc[0, '市值'] = 0
            position.loc[0, '保证金'] = 0
        # 当前已有仓位
        else:
            ind = len(position)
            position.loc[ind, '时间'] = order['时间']
            position.loc[ind, '品种'] = order['品种']
            position.loc[ind, '开仓时间'] = order['时间']
            position.loc[ind, '盯开盘'] = '是'
            if order['买卖'] == '买开':
                position.loc[ind, '多空'] = '多'
            elif order['买卖'] == '卖开':
                position.loc[ind, '多空'] = '空'
            position.loc[ind, '数量'] = order['数量']
            if position.loc[ind, '多空'] == '多':
                position.loc[ind, '开仓价'] = order['成交价'] + slip
            elif position.loc[ind, '多空'] == '空':
                position.loc[ind, '开仓价'] = order['成交价'] - slip
            position.loc[ind, '昨收'] = last_p
            position.loc[ind, '今收'] = toda_p
            # 先不结算
            position.loc[ind, '逐笔盈亏'] = 0
            position.loc[ind, '盯市盈亏'] = 0
            position.loc[ind, '市值'] = 0
            position.loc[ind, '保证金'] = 0
        # position_record记录
        self.position = copy.deepcopy(position)

    # 处理平仓的情况
    def process_close(self, order):
        """
        改变trade
        改变position
        改变account
        """
        # 先把持仓的该品种的仓位选出来
        if order['买卖'] == '卖平':
            posi = self.position.loc[(self.position['多空'] == '多')]
        elif order['买卖'] == '买平':
            posi = self.position.loc[(self.position['多空'] == '空')]

        # 计算所需要的平掉的哪些个仓位,此处平仓是按顺序来的，实际中，通过计算哪个平仓手续费便宜按哪个来,有时平今便宜，有时平昨便宜
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
        # 根据所需的平仓, 记录TradeSummary
        t_len = len(self.trade)
        order_num = order['数量']
        for i1 in range(0, ind):  # i1 + t_len 定位trade
            i = posi.index[i1]  # i 定位posi

            c_fx = self.config_info.getfloat(self.instrument, 'commission_fix')
            c_ft = self.config_info.getfloat(self.instrument, 'commission_float')
            trading_unit = self.config_info.getint(self.instrument, 'trading_unit')
            slip = self.config_info.getfloat(self.instrument, 'slip')
            num = posi.loc[i, '数量'] # 这个num是平掉的这个仓的数量

            self.trade.loc[t_len + i1, '品种'] = posi.loc[i, '品种']
            self.trade.loc[t_len + i1, '开仓时间'] = posi.loc[i, '开仓时间']
            if posi.loc[i, '多空'] == '多':
                self.trade.loc[t_len + i1, '开仓操作'] = '买开'
            elif posi.loc[i, '多空'] == '空':
                self.trade.loc[t_len + i1, '开仓操作'] = '卖开'
            self.trade.loc[t_len + i1, '开仓价'] = posi.loc[i, '开仓价']
            self.trade.loc[t_len + i1, '开仓数量'] = posi.loc[i, '数量']
            if i1 == ind - 1: # 如果是最后一个仓位，平掉的仓位就是剩下的仓位需要平掉的还没平掉的仓位
                self.trade.loc[t_len + i1, '开仓数量'] = order_num # order_num就是最后剩下的那些仓位
                num = order_num
            self.trade.loc[t_len + i1, '平仓时间'] = order['时间']
            self.trade.loc[t_len + i1, '平仓操作'] = order['买卖']
            if self.trade.loc[t_len + i1, '开仓操作'] == '买开':
                self.trade.loc[t_len + i1, '平仓价'] = order['成交价'] - slip
            elif self.trade.loc[t_len + i1, '开仓操作'] == '卖开':
                self.trade.loc[t_len + i1, '平仓价'] = order['成交价'] + slip
            closeprice = self.trade.loc[t_len + i1, '平仓价']
            self.trade.loc[t_len + i1, '平仓数量'] = self.trade.loc[t_len + i1, '开仓数量']
            self.trade.loc[t_len + i1, '盯开盘'] = posi.loc[i, '盯开盘']
            # 手续费
            self.trade.loc[t_len + i1, '手续费'] = num * c_fx + num * trading_unit * closeprice * c_ft
            commission = self.trade.loc[t_len + i1, '手续费'] # 手续费要计入到account
            # 平仓盈亏计算
            if posi.loc[i, '多空'] == '多':
                self.trade.loc[t_len + i1, '平仓盈亏'] = num * trading_unit * (closeprice - posi.loc[i, '开仓价'])
            elif posi.loc[i, '多空'] == '空':
                self.trade.loc[t_len + i1, '平仓盈亏'] = -num * trading_unit * (closeprice - posi.loc[i, '开仓价'])
            close_p_l = self.trade.loc[t_len + i1, '平仓盈亏'] # 平仓盈亏要记录要account
            # 净盈亏
            self.trade.loc[t_len + i1, '净盈亏'] = close_p_l - commission
            if t_len + i1 != 0:
                self.trade.loc[t_len + i1, '逐笔累计盈利'] = self.trade.loc[t_len + i1 - 1, '逐笔累计盈利'] + \
                                                            self.trade.loc[t_len + i1, '净盈亏']
            else:
                self.trade.loc[t_len + i1, '逐笔累计盈利'] = self.trade.loc[t_len + i1, '逐笔累计盈利'] + \
                                                            self.trade.loc[t_len + i1, '净盈亏']
            # ===========记录Account 平仓盈亏和手续费=============
            # 获得该品种昨日收盘价
            lastprice = self.marketdata['昨收'][0]
            # 盯盘盈亏，用于
            if order['买卖'] == '卖平':
                close_sting = num * trading_unit * (closeprice - lastprice)
            elif order['买卖'] == '买平':
                close_sting = num * trading_unit * (lastprice - closeprice)

            if posi.loc[i, '盯开盘'] == '是':
                self.account.loc[0, '平盯今盈亏'] += close_p_l
            elif posi.loc[i, '盯开盘'] == '否':
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

    # 仓位处理之后，进行结算
    def settle(self):
        """
        结算时：
        position所有新仓变成老仓,更新逐笔浮盈和盯市浮盈，
        其中盯市浮盈要记录到账户里去,计算持仓盈亏
        account进行更新

        """
        # 如果此时无仓位了
        time = self.marketdata['时间'][0]
        if self.position.loc[0, '品种'] == None:
            # 如果当前没有持仓了
            # 计算account
            self.account.loc[0, '时间'] = time
            self.account.loc[0, '平仓盈亏'] = self.account.loc[0, '平盯昨盈亏'] + \
                                             self.account.loc[0, '平盯今盈亏']
            self.account.loc[0, '盯市盈亏'] = self.account.loc[0, '盯昨盈亏'] + \
                                             self.account.loc[0, '盯今盈亏']
            self.account.loc[0, '期末'] = self.account.loc[0, '期初'] + \
                                          self.account.loc[0, '平仓盈亏'] + \
                                          self.account.loc[0, '盯市盈亏'] - \
                                          self.account.loc[0, '手续费']

            self.account.loc[0, '保证金'] = 0
            self.account.loc[0, '可用资金'] = self.account.loc[0, '期末']
            self.account.loc[0, '风险度'] = 0
            self.account.loc[0, '多头市值'] = 0
            self.account.loc[0, '空头市值'] = 0
            self.account.loc[0, '市值'] = 0

            # 记录account
            self.account_record = self.account_record.append(self.account)

            # 这里要把account为下一衡量日调整
            self.account.loc[0, '期初'] = self.account.loc[0, '期末']
            self.account.loc[0, '平盯今盈亏'] = 0
            self.account.loc[0, '平盯昨盈亏'] = 0
            self.account.loc[0, '平仓盈亏'] = 0
            self.account.loc[0, '盯昨盈亏'] = 0
            self.account.loc[0, '盯今盈亏'] = 0
            self.account.loc[0, '盯市盈亏'] = 0
            self.account.loc[0, '手续费'] = 0
            self.account.loc[0, '期末'] = 0
            self.account.loc[0, '保证金'] = 0
            self.account.loc[0, '可用资金'] = 0
            self.account.loc[0, '风险度'] = 0
            self.account.loc[0, '多头市值'] = 0
            self.account.loc[0, '空头市值'] = 0
            self.account.loc[0, '市值'] = 0

        elif self.position.loc[0, '品种'] != None:
            # ============================================position
            for i in range(0, len(self.position)):
                trading_unit = self.config_info.getint(self.instrument, 'trading_unit')
                margin = self.config_info.getfloat(self.instrument, 'margin')
                num = self.position.loc[i, '数量']
                last_p = self.marketdata['昨收'][0]
                toda_p = self.marketdata['今收'][0]
                open_p = self.position.loc[i, '开仓价']
                self.position.loc[i, '时间'] = time
                self.position.loc[i, '昨收'] = last_p
                self.position.loc[i, '今收'] = toda_p
                # 更新逐笔盈亏
                trade_by_trade = (toda_p - open_p) * trading_unit * num
                if self.position.loc[i, '多空'] == '多':
                    self.position.loc[i, '逐笔盈亏'] = trade_by_trade
                elif self.position.loc[i, '多空'] == '空':
                    self.position.loc[i, '逐笔盈亏'] = -trade_by_trade
                # 更新盯市盈亏
                if self.position.loc[i, '盯开盘'] == '是':
                    trade_by_trade = (toda_p - open_p) * trading_unit * num
                    if self.position.loc[i, '多空'] == '多':
                        self.position.loc[i, '盯市盈亏'] = trade_by_trade
                    elif self.position.loc[i, '多空'] == '空':
                        self.position.loc[i, '盯市盈亏'] = -trade_by_trade
                elif self.position.loc[i, '盯开盘'] == '否':
                    trade_by_day = (toda_p - last_p) * trading_unit * num
                    if self.position.loc[i, '多空'] == '多':
                        self.position.loc[i, '盯市盈亏'] = trade_by_day
                    elif self.position.loc[i, '多空'] == '空':
                        self.position.loc[i, '盯市盈亏'] = -trade_by_day

                self.position.loc[i, '市值'] = num * trading_unit * toda_p
                self.position.loc[i, '保证金'] = num * trading_unit * toda_p * margin

            # 记录positon_record
            self.position_record = self.position_record.append(self.position)

            # ============================================account
            self.account.loc[0, '时间'] = time
            self.account.loc[0, '平仓盈亏'] = self.account.loc[0, '平盯昨盈亏'] + \
                                             self.account.loc[0, '平盯今盈亏']
            position = copy.deepcopy(self.position)
            # 结算仓位盯昨盯今情况
            self.account.loc[0, '盯昨盈亏'] = position.loc[position['盯开盘'] == '否', '盯市盈亏'].sum()
            self.account.loc[0, '盯今盈亏'] = position.loc[position['盯开盘'] == '是', '盯市盈亏'].sum()

            self.account.loc[0, '盯市盈亏'] = self.account.loc[0, '盯昨盈亏'] + \
                                             self.account.loc[0, '盯今盈亏']
            self.account.loc[0, '期末'] = self.account.loc[0, '期初'] + \
                                          self.account.loc[0, '平仓盈亏'] + \
                                          self.account.loc[0, '盯市盈亏'] - \
                                          self.account.loc[0, '手续费']

            self.account.loc[0, '保证金'] = self.position['保证金'].sum()
            self.account.loc[0, '可用资金'] = self.account.loc[0, '期末'] - \
                                            self.account.loc[0, '保证金']
            if self.account.loc[0, '期末'] != 0: # 如果期末还有钱。。。。。
                self.account.loc[0, '风险度'] = self.account.loc[0, '保证金'] / \
                                               self.account.loc[0, '期末']
            else:
                self.account.loc[0, '风险度'] = 0 # 期末都没有钱了

            self.account.loc[0, '多头市值'] = self.position.loc[
                self.position['多空'] == '多', '市值'].sum()

            if self.account.loc[0, '多头市值'] == False:
                self.account.loc[0, '多头市值'] = 0

            self.account.loc[0, '空头市值'] = self.position.loc[
                self.position['多空'] == '空', '市值'].sum()

            if self.account.loc[0, '空头市值'] == False:
                self.account.loc[0, '空头市值'] = 0

            self.account.loc[0, '市值'] = self.account.loc[0, '多头市值'] + \
                                         self.account.loc[0, '空头市值']

            # 记录account
            self.account_record = self.account_record.append(self.account)

            # 这里要把account为下一衡量日调整
            self.account.loc[0, '期初'] = self.account.loc[0, '期末']
            self.account.loc[0, '平盯今盈亏'] = 0
            self.account.loc[0, '平盯昨盈亏'] = 0
            self.account.loc[0, '平仓盈亏'] = 0
            self.account.loc[0, '盯昨盈亏'] = 0
            self.account.loc[0, '盯今盈亏'] = 0
            self.account.loc[0, '盯市盈亏'] = 0
            self.account.loc[0, '手续费'] = 0
            self.account.loc[0, '期末'] = 0
            self.account.loc[0, '保证金'] = 0
            self.account.loc[0, '可用资金'] = 0
            self.account.loc[0, '风险度'] = 0
            self.account.loc[0, '多头市值'] = 0
            self.account.loc[0, '空头市值'] = 0
            self.account.loc[0, '市值'] = 0

    def record_process(self):
        # 输入本地存储的文件夹名称及文件名称，存储回测结果
        # =======================先reset_index
        self.marketdata_record = self.marketdata_record.reset_index(drop=True)
        self.order_record = self.order_record.reset_index(drop=True)
        self.position_record = self.position_record.reset_index(drop=True)
        self.trade = self.trade.reset_index(drop=True)
        self.account_record = self.account_record.reset_index(drop=True)
        # ========================这里修复了一个不明原因的bug
        marketcond1 = (self.marketdata_record.loc[0, '时间'] == None)
        marketcond2 = (self.marketdata_record.loc[0, '品种'] == None)
        if marketcond1 or marketcond2:
            self.marketdata_record.drop([0], inplace=True)

        ordercond1 = (self.order_record.loc[0, '时间'] == None)
        ordercond2 = (self.order_record.loc[0, '品种'] == None)
        if ordercond1 or ordercond2:
            self.order_record.drop([0], inplace=True)

        positioncond1 = (self.position_record.loc[0, '时间'] == None)
        positioncond2 = (self.position_record.loc[0, '品种'] == None)
        if positioncond1 or positioncond2:
            self.position_record.drop([0], inplace=True)

        if self.trade.loc[0, '品种'] == None:
            self.trade.drop([0], inplace=True)

        if self.account_record.loc[0, '时间'] == None:
            self.account_record.drop([0], inplace=True)
        # ==========================再次reset_index把index设置好
        self.marketdata_record = self.marketdata_record.reset_index(drop=True)
        self.order_record = self.order_record.reset_index(drop=True)
        self.position_record = self.position_record.reset_index(drop=True)
        self.trade = self.trade.reset_index(drop=True)
        self.account_record = self.account_record.reset_index(drop=True)

    def backtest_record_save(self, file_name, strategy_name):
        filename = os.getcwd()
        files = os.path.join(os.path.dirname(filename), 'backtest_result', file_name)
        if not os.path.exists(files):
            os.mkdir(files)
        filename = os.path.join(files, strategy_name + '.xlsx')
        if not os.path.exists(filename):
            wb = xlwt.Workbook()
            wb.add_sheet('marketdata')
            wb.add_sheet('order')
            wb.add_sheet('position')
            wb.add_sheet('trade')
            wb.add_sheet('account')
            wb.save(filename)
        else:
            print('策略名称已存在，请改变策略名称！！！')

        xlswriter = pd.ExcelWriter(filename)

        self.marketdata_record.to_excel(xlswriter, sheet_name='marketdata')
        self.order_record.to_excel(xlswriter, sheet_name='order')
        self.position_record.to_excel(xlswriter, sheet_name='position')
        self.trade.to_excel(xlswriter, sheet_name='trade')
        self.account_record.to_excel(xlswriter, sheet_name='account')

        xlswriter.save()


def main():
    self = Futures_single(instrument='j')
    md = self.marketdata_new()
    order = self.order_new()

    md.loc[0, '时间'] = '2018-02-01'
    md.loc[0, '品种'] = 'j'
    md.loc[0, '昨收'] = 4000
    md.loc[0, '开盘'] = 4000
    md.loc[0, '最高'] = 4170
    md.loc[0, '最低'] = 4130
    md.loc[0, '今收'] = 4150
    md.loc[0, '成交量'] = 10000
    md.loc[0, '持仓量'] = 20000
    self.backtest_loop(md, order)

    md.loc[0, '时间'] = '2018-02-02'
    md.loc[0, '品种'] = 'j'
    md.loc[0, '昨收'] = 4150
    md.loc[0, '开盘'] = 4150
    md.loc[0, '最高'] = 4170
    md.loc[0, '最低'] = 4130
    md.loc[0, '今收'] = 4140
    md.loc[0, '成交量'] = 10000
    md.loc[0, '持仓量'] = 20000

    order.loc[0, '时间'] = '2018-02-02'
    order.loc[0, '品种'] = 'j'
    order.loc[0, '买卖'] = '买开'
    order.loc[0, '成交价'] = 4020
    order.loc[0, '数量'] = 20

    order.loc[1, '时间'] = '2018-02-02'
    order.loc[1, '品种'] = 'j'
    order.loc[1, '买卖'] = '买开'
    order.loc[1, '成交价'] = 4030
    order.loc[1, '数量'] = 20

    order.loc[2, '时间'] = '2018-02-02'
    order.loc[2, '品种'] = 'j'
    order.loc[2, '买卖'] = '卖平'
    order.loc[2, '成交价'] = 4060
    order.loc[2, '数量'] = 24

    self.backtest_loop(md, order)
    md = self.marketdata_new()
    order = self.order_new()

    md.loc[0, '时间'] = '2018-02-03'
    md.loc[0, '品种'] = 'j'
    md.loc[0, '昨收'] = 4140
    md.loc[0, '开盘'] = 4140
    md.loc[0, '最高'] = 4150
    md.loc[0, '最低'] = 4130
    md.loc[0, '今收'] = 4150
    md.loc[0, '成交量'] = 10000
    md.loc[0, '持仓量'] = 20000

    self.backtest_loop(md, order)

    md = self.marketdata_new()
    order = self.order_new()

    md.loc[0, '时间'] = '2018-02-04'
    md.loc[0, '品种'] = 'j'
    md.loc[0, '昨收'] = 4150
    md.loc[0, '开盘'] = 4150
    md.loc[0, '最高'] = 4170
    md.loc[0, '最低'] = 4130
    md.loc[0, '今收'] = 4160
    md.loc[0, '成交量'] = 10000
    md.loc[0, '持仓量'] = 20000

    order.loc[0, '时间'] = '2018-02-04'
    order.loc[0, '品种'] = 'j'
    order.loc[0, '买卖'] = '卖平'
    order.loc[0, '成交价'] = 4130
    order.loc[0, '数量'] = 16

    self.backtest_loop(md, order)
    self.record_process()
    self.backtest_record_save('test', 'test')
    print("Done")


if __name__ == '__main__':
    main()
