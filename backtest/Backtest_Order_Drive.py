# -*- coding: UTF-8 -*-
# author:@Jack.Wang
# time :2018/8/24 22:23
"""
订单驱动型回测系统
主要模仿交易所的逐日盯市 + 逐笔 账单来制定回测系统
包括MarketData Order position Positions  Account_Summary Trade_Summary期货账单六部分
MarketData 模仿行情推送
Order Order定制
PositionDetail 逐日持仓详情
Positions 逐日持仓汇总
account 逐日账单汇总
Trade_Summary 逐笔订单
通过六部分的组合，构建所有策略的回测系统
使用方法：
初始化：策略名称（用于之后记录回测结果的唯一参数，策略滑点，每个策略有不同的滑点，初始资金设置
每个推送给order_driven_backtest 一个市场数据，格式固定，一个order，格式固定，由此，完成策略回测

"""

from data_get_save.futures_info_process import futures_cal
import xlwt
import os
import pandas as pd


class order_driven_backtest:

    def __init__(self, strategyname, slip=2, initial_money=1000000):
        self.backtest = {}
        self.marketdata_init()
        self.order_init()
        self.position_detail_init()
        self.positions_init()
        self.account_init(initial_money=initial_money)
        self.trade_init()
        futures = futures_cal()
        futu_list = futures.futu_list
        futu_info = futures.futu_info
        futu_info['commission_mul'] = 1.5
        futu_info['margin_add'] = 0.02
        self.backtest['slip'] = slip
        self.backtest['strategyname'] = strategyname
        self.backtest['futures_list'] = futu_list
        self.backtest['futures_info'] = futu_info

    def marketdata_init(self):
        # 市场数据，此处品种如 j rb，而非j1801
        init = pd.DataFrame(columns=['时间', '品种', '昨收', '开盘', '最高', '最低', '今收', '是否结算'])
        init = init.append(pd.DataFrame({'时间': [None],
                                         '品种': [None],
                                         '昨收': [None],
                                         '开盘': [None],
                                         '最高': [None],
                                         '最低': [None],
                                         '今收': [None],
                                         '是否结算': [None]}), ignore_index=True)
        self.backtest['marketdata']=init
        record = pd.DataFrame(columns=['时间', '品种', '昨收', '开盘', '最高', '最低', '今收', '是否结算'])
        record = record.append(pd.DataFrame({'时间': [None],
                                             '品种': [None],
                                             '昨收': [None],
                                             '开盘': [None],
                                             '最高': [None],
                                             '最低': [None],
                                             '今收': [None],
                                             '是否结算': [None]}), ignore_index=True)
        self.backtest['marketdata_record'] = record

    def marketdata_new(self):
        init = pd.DataFrame(columns=['时间', '品种', '昨收', '开盘', '最高', '最低', '今收', '是否结算'])
        init = init.append(pd.DataFrame({'时间': [None],
                                         '品种': [None],
                                         '昨收': [None],
                                         '开盘': [None],
                                         '最高': [None],
                                         '最低': [None],
                                         '今收': [None],
                                         '是否结算': [None]}), ignore_index=True)
        return init

    def order_init(self):
        init = pd.DataFrame(columns=['时间', '品种', '买卖', '成交价', '数量'])
        self.backtest['order'] = init
        record = init.append(pd.DataFrame({'时间': [None], '品种': [None], '买卖': [None], '成交价': [None],
                                           '数量': [None]}), ignore_index=True)
        self.backtest['order_record'] = record

    def order_new(self):
        init = pd.DataFrame(columns=['时间', '品种', '买卖', '成交价', '数量'])
        return init

    def position_detail_init(self):
        init = pd.DataFrame(columns=['时间', '品种', '开仓时间', '是否今仓', '盯开盘',
                                     '多空', '数量', '开仓价', '昨收', '今收',
                                     '逐笔盈亏', '盯市盈亏', '市值', '保证金'])
        init = init.append(pd.DataFrame({'时间': [None],
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
                                         '保证金': [None]}), ignore_index=True)
        self.backtest['position'] = init
        record = pd.DataFrame(columns=['时间', '品种', '开仓时间', '是否今仓', '盯开盘',
                                       '多空', '数量', '开仓价', '昨收', '今收',
                                       '逐笔盈亏', '盯市盈亏', '市值', '保证金'])
        record = record.append(pd.DataFrame({'时间': [None],
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
                                             '保证金': [None]}), ignore_index=True)
        self.backtest['position_record'] = record

    def position_detail_new(self):
        init = pd.DataFrame(columns=['时间', '品种', '开仓时间', '是否今仓', '盯开盘',
                                     '多空', '数量', '开仓价', '昨收', '今收',
                                     '逐笔盈亏', '盯市盈亏', '市值', '保证金'])
        init = init.append(pd.DataFrame({'时间': [None],
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
                                         '保证金': [None]}), ignore_index=True)
        return init

    def positions_init(self): # 初始化一个positions
        init = pd.DataFrame(columns=['时间', '品种',
                                     '买持量', '买均价', '多头盯市', '多头逐笔', '多头保证金',
                                     '卖持量', '卖均价', '空头盯市', '空头逐笔', '空头保证金',
                                     '昨收', '今收'])
        init = init.append(pd.DataFrame({'时间': [None],
                                         '品种': [None],
                                         '买持量': 0,
                                         '买均价': 0,
                                         '多头盯市': 0,
                                         '多头逐笔': 0,
                                         '多头保证金': 0,
                                         '卖持量': 0,
                                         '卖均价': 0,
                                         '空头盯市': 0,
                                         '空头逐笔': 0,
                                         '空头保证金': 0,
                                         '昨收': 0,
                                         '今收': 0}), ignore_index=True)
        self.backtest['positions'] = init
        record = pd.DataFrame(columns=['时间', '品种',
                                       '买持量', '买均价', '多头盯市', '多头逐笔', '多头保证金',
                                       '卖持量', '卖均价', '空头盯市', '空头逐笔', '空头保证金',
                                       '昨收', '今收'])
        record = record.append(pd.DataFrame({'时间': [None],
                                             '品种': [None],
                                             '买持量': [None],
                                             '买均价': [None],
                                             '多头盯市': [None],
                                             '多头逐笔': [None],
                                             '多头保证金': [None],
                                             '卖持量': [None],
                                             '卖均价': [None],
                                             '空头盯市': [None],
                                             '空头逐笔': [None],
                                             '空头保证金': [None],
                                             '昨收': [None],
                                             '今收': [None]}), ignore_index=True)
        self.backtest['positions_record'] = record

    def positions_new(self): # 初始化一个positions
        init = pd.DataFrame(columns=['时间', '品种',
                                     '买持量', '买均价', '多头盯市', '多头逐笔', '多头保证金',
                                     '卖持量', '卖均价', '空头盯市', '空头逐笔', '空头保证金',
                                     '昨收', '今收'])
        init = init.append(pd.DataFrame({'时间': [None],
                                         '品种': [None],
                                         '买持量': 0,
                                         '买均价': 0,
                                         '多头盯市': 0,
                                         '多头逐笔': 0,
                                         '多头保证金': 0,
                                         '卖持量': 0,
                                         '卖均价': 0,
                                         '空头盯市': 0,
                                         '空头逐笔': 0,
                                         '空头保证金': 0,
                                         '昨收': 0,
                                         '今收': 0}), ignore_index=True)
        return init

    def account_init(self, initial_money): # 初始化一个account
        init = pd.DataFrame(columns=['时间', '出入金', '期初',
                                     '平盯昨盈亏', '平盯今盈亏', '平仓盈亏',
                                     '盯昨盈亏', '盯今盈亏', '盯市盈亏',
                                     '手续费', '期末', '保证金', '可用资金',
                                     '风险度', '多头市值', '空头市值', '市值'])
        init = init.append(pd.DataFrame({'时间': [None],
                                         '出入金': 0,
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
                                         '市值': 0}), ignore_index=True)
        self.backtest['account'] = init
        record = pd.DataFrame(columns=['时间', '出入金', '期初',
                                       '平盯昨盈亏', '平盯今盈亏', '平仓盈亏',
                                       '盯昨盈亏', '盯今盈亏', '盯市盈亏',
                                       '手续费', '期末', '保证金', '可用资金',
                                       '风险度', '多头市值', '空头市值', '市值'])
        record = record.append(pd.DataFrame({'时间': [None],
                                             '出入金': [None],
                                             '期初': [None],
                                             '平盯昨盈亏': [None],
                                             '平盯今盈亏': [None],
                                             '平仓盈亏': [None],
                                             '盯昨盈亏': [None],
                                             '盯今盈亏': [None],
                                             '盯市盈亏': [None],
                                             '手续费': [None],
                                             '期末': [None],
                                             '保证金': [None],
                                             '可用资金': [None],
                                             '风险度': [None],
                                             '多头市值': [None],
                                             '空头市值': [None],
                                             '市值': [None]}), ignore_index=True)
        self.backtest['account_record'] = record

    def trade_init(self):
        init = pd.DataFrame(columns=['品种', '开仓时间', '开仓操作', '开仓价', '开仓数量',
                                     '平仓时间', '平仓操作', '平仓价', '平仓数量', '手续费',
                                     '是否平今', '平仓盈亏', '净盈亏', '逐笔累计盈利'])
        init = init.append(pd.DataFrame({'品种': [None],
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
                                         '逐笔累计盈利': 0}), ignore_index=True)

        self.backtest['trade'] = init

    def process_control(self, md, order):
        self.backtest['marketdata'] = md
        self.backtest['order'] = order
        # marketdata_record记录
        self.backtest['marketdata_record'] = self.backtest['marketdata_record'].append(self.backtest['marketdata'])
        # 根据md和order
        # 进行position的更新
        # 进行Positions的更新
        # 进行account的更新
        # 进行Trade_Summary的更新
        for i in range(0, len(order)):
            order_ = order.loc[i, :]
            # 记录order_record
            self.backtest['order_record'] = self.backtest['order_record'].append(order_)
            # 先进行order的处理
            if order_['买卖'] == '买开' or order_['买卖'] == '卖开':
                self.process_open(order_)
            elif order_['买卖'] == '卖平' or order_['买卖'] == '买平':
                self.process_closeposition(order_)
            else:
                print('order 格式非标准，请重新输入order')

        # 根据持仓详细，md计算逐笔盈亏，盯市盈亏，保证金
        # 根据持仓详细，计算持仓合并，计算合并后的逐笔盈亏，盯市盈亏，保证金等
        # 计算account的平仓盈亏，盯市盈亏，手续费，期末，保证金，可用资金，风险度等

        self.minutes_settle()
        # 修改盯开盘
        self.backtest['position']['盯开盘'] = '否'

        if self.backtest['marketdata'].loc[0, '是否结算'] == '是':
            # 修改是否今仓，
            self.backtest['position']['是否今仓'] = '否'

    def position_detail_open(self, md, order_, position, info, slip):
        trading_unit = info[order_['品种']]['trading_unit']
        margin = info[order_['品种']]['margin'] + info['margin_add']
        last_p = md.loc[md['品种'] == order_['品种'], '昨收'][0]
        toda_p = md.loc[md['品种'] == order_['品种'], '今收'][0]

        if position.loc[0, '品种'] == None:
            position.loc[0, '时间'] = order_['时间']
            position.loc[0, '品种'] = order_['品种']
            position.loc[0, '开仓时间'] = order_['时间']
            position.loc[0, '是否今仓'] = '是'
            position.loc[0, '盯开盘'] = '是'
            if order_['买卖'] == '买开':
                position.loc[0, '多空'] = '多'
            elif order_['买卖'] == '卖开':
                position.loc[0, '多空'] = '空'
            position.loc[0, '数量'] = order_['数量']
            if position.loc[0, '多空'] == '多':
                position.loc[0, '开仓价'] = order_['成交价'] + slip
            elif position.loc[0, '多空'] == '空':
                position.loc[0, '开仓价'] = order_['成交价'] - slip
            position.loc[0, '昨收'] = last_p
            position.loc[0, '今收'] = toda_p
            position.loc[0, '逐笔盈亏'] = order_['数量'] * (toda_p - position.loc[0, '开仓价']) * trading_unit
            if order_['买卖'] == '卖开':
                position.loc[0, '逐笔盈亏'] = -position.loc[0, '逐笔盈亏']
            position.loc[0, '盯市盈亏'] = position.loc[0, '逐笔盈亏']
            position.loc[0, '市值'] = order_['数量'] * toda_p * trading_unit
            position.loc[0, '保证金'] = order_['数量'] * toda_p * trading_unit * margin
        else:
            ind = len(position)
            position.loc[ind, '时间'] = order_['时间']
            position.loc[ind, '品种'] = order_['品种']
            position.loc[ind, '开仓时间'] = order_['时间']
            position.loc[ind, '是否今仓'] = '是'
            position.loc[ind, '盯开盘'] = '是'
            if order_['买卖'] == '买开':
                position.loc[ind, '多空'] = '多'
            elif order_['买卖'] == '卖开':
                position.loc[ind, '多空'] = '空'
            position.loc[ind, '数量'] = order_['数量']
            if position.loc[ind, '多空'] == '多':
                position.loc[ind, '开仓价'] = order_['成交价'] + slip
            elif position.loc[ind, '多空'] == '空':
                position.loc[ind, '开仓价'] = order_['成交价'] - slip
            position.loc[ind, '昨收'] = last_p
            position.loc[ind, '今收'] = toda_p
            position.loc[ind, '逐笔盈亏'] = order_['数量'] * (toda_p - position.loc[ind, '开仓价']) * trading_unit
            position.loc[ind, '市值'] = order_['数量'] * toda_p * trading_unit
            if order_['买卖'] == '卖开':
                position.loc[ind, '逐笔盈亏'] = -position.loc[ind, '逐笔盈亏']
            position.loc[ind, '盯市盈亏'] = position.loc[ind, '逐笔盈亏']
            position.loc[ind, '保证金'] = order_['数量'] * toda_p * trading_unit * margin
        # position_record记录
        return position

    def process_open(self, order_):
        self.backtest['position'] = \
            self.position_detail_open(self.backtest['marketdata'],
                                      order_,
                                      self.backtest['position'],
                                      self.backtest['futures_info'],
                                      self.backtest['slip'])

    # 处理平仓操作
    def process_closeposition(self, order_):
        """
        order + position
        改变position
        改变account
        """
        # 先把持仓的该品种的仓位选出来
        instrument = order_['品种']
        if order_['买卖'] == '卖平':
            posi = self.backtest['position'].loc[(self.backtest['position']['品种'] == instrument) &
                                                 (self.backtest['position']['多空'] == '多')]
        elif order_['买卖'] == '买平':
            posi = self.backtest['position'].loc[(self.backtest['position']['品种'] == instrument) &
                                                 (self.backtest['position']['多空'] == '空')]
        # 计算所需要的平掉的哪些个仓位,此处平仓是按顺序来的，实际中，通过计算哪个平仓手续费便宜按哪个来,有时平今便宜，有时平昨便宜
        ind = len(posi.index)
        order_num = order_['数量']
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
        t_len = len(self.backtest['trade'])
        order_num = order_['数量']
        for i1 in range(0, ind): # i1 + t_len 定位trade
            i = posi.index[i1] # i 定位posi
            c_fx_t = self.backtest['futures_info'][order_['品种']]['commission_fix_today']
            c_ft_t = self.backtest['futures_info'][order_['品种']]['commission_float_today']
            c_fx = self.backtest['futures_info'][order_['品种']]['commission_fix']
            c_ft = self.backtest['futures_info'][order_['品种']]['commission_float']
            trading_unit = self.backtest['futures_info'][order_['品种']]['trading_unit']
            num = posi.loc[i, '数量']
            self.backtest['trade'].loc[t_len + i1, '品种'] = posi.loc[i, '品种']
            self.backtest['trade'].loc[t_len + i1, '开仓时间'] = posi.loc[i, '开仓时间']
            if posi.loc[i, '多空'] == '多':
                self.backtest['trade'].loc[t_len + i1, '开仓操作'] = '买开'
            elif posi.loc[i, '多空'] == '空':
                self.backtest['trade'].loc[t_len + i1, '开仓操作'] = '卖开'
            self.backtest['trade'].loc[t_len + i1, '开仓价'] = posi.loc[i, '开仓价']
            self.backtest['trade'].loc[t_len + i1, '开仓数量'] = posi.loc[i, '数量']
            if i1 == ind - 1:
                self.backtest['trade'].loc[t_len + i1, '开仓数量'] = order_num
                num = order_num
            self.backtest['trade'].loc[t_len + i1, '平仓时间'] = order_['时间']
            self.backtest['trade'].loc[t_len + i1, '平仓操作'] = order_['买卖']
            if self.backtest['trade'].loc[t_len + i1, '开仓操作'] == '买开':
                self.backtest['trade'].loc[t_len + i1, '平仓价'] = order_['成交价'] - self.backtest['slip']
            elif self.backtest['trade'].loc[t_len + i1, '开仓操作'] == '卖开':
                self.backtest['trade'].loc[t_len + i1, '平仓价'] = order_['成交价'] + self.backtest['slip']
            closeprice = self.backtest['trade'].loc[t_len + i1, '平仓价']
            self.backtest['trade'].loc[t_len + i1, '平仓数量'] = self.backtest['trade'].loc[t_len + i1, '开仓数量']
            self.backtest['trade'].loc[t_len + i1, '是否平今'] = posi.loc[i, '是否今仓']
            self.backtest['trade'].loc[t_len + i1, '盯开盘'] = posi.loc[i, '盯开盘']

            if posi.loc[i, '是否今仓'] == '是':
                self.backtest['trade'].loc[t_len + i1, '手续费'] = num * c_fx_t + \
                                                                num * trading_unit * closeprice * c_ft_t
            else:
                self.backtest['trade'].loc[t_len + i1, '手续费'] = num * c_fx + \
                                                                num * trading_unit * closeprice * c_ft
            commission = self.backtest['trade'].loc[t_len + i1, '手续费']

            self.backtest['trade'].loc[t_len + i1, '平仓盈亏'] = num * trading_unit * (closeprice - posi.loc[i, '开仓价'])
            if posi.loc[i, '多空'] == '空':
                self.backtest['trade'].loc[t_len + i1, '平仓盈亏'] = -self.backtest['trade'].loc[t_len + i1, '平仓盈亏']
            close_p_l = self.backtest['trade'].loc[t_len + i1, '平仓盈亏']
            self.backtest['trade'].loc[t_len + i1, '净盈亏'] = close_p_l - commission
            if t_len + i1 != 0:
                self.backtest['trade'].loc[t_len + i1, '逐笔累计盈利'] = self.backtest['trade'].loc[t_len + i1 - 1, '逐笔累计盈利'] + \
                                                            self.backtest['trade'].loc[t_len + i1, '净盈亏']
            else:
                self.backtest['trade'].loc[t_len + i1, '逐笔累计盈利'] = self.backtest['trade'].loc[t_len + i1, '逐笔累计盈利'] + \
                                                            self.backtest['trade'].loc[t_len + i1, '净盈亏']
            # 记录AccountSummary 平仓盈亏和手续费
            # 获得该品种昨日收盘价
            marketdata = self.backtest['marketdata']
            lastprice = marketdata[marketdata['品种']==order_['品种']]['昨收'][0]

            if order_['买卖'] == '卖平':
                close_sting = num * trading_unit * (closeprice - lastprice)
            elif order_['买卖'] == '买平':
                close_sting = num * trading_unit * (lastprice - closeprice)

            if posi.loc[i, '盯开盘'] == '是':
                self.backtest['account'].loc[0, '平盯今盈亏'] += close_sting
            else:
                self.backtest['account'].loc[0, '平盯昨盈亏'] += close_sting

            self.backtest['account'].loc[0, '手续费'] += commission
            # 记录完一次操作，要把trade里面的order的数量更新下
            order_num = order_num - posi.loc[i, '数量']
            self.backtest['position'].loc[i, '数量'] = self.backtest['position'].loc[i, '数量'] - \
                                                     self.backtest['trade'].loc[t_len + i1, '平仓数量']


        # 删除品种是None的逐笔交易记录,只有第一次删除，需要reset_index
        if self.backtest['trade'].loc[0, '品种'] == None:
            self.backtest['trade'] = self.backtest['trade'].drop([0])
            self.backtest['trade'] = self.backtest['trade'].reset_index(drop=True)

        # 删除持仓详细数量为0的持仓
        self.backtest['position'] = self.backtest['position'].loc[self.backtest['position']['数量'] != 0]
        self.backtest['position'] = self.backtest['position'].reset_index(drop=True)

        # 如果把所有持仓全部删除了，那么就再给持仓一个初值
        if len(self.backtest['position']) == 0:
            self.backtest['position'] = self.position_detail_new()

    # 每根K线之后，都要结算
    def minutes_settle(self):
        """
        结算时：
        position所有新仓变成老仓,更新逐笔浮盈和盯市浮盈，
        其中盯市浮盈要记录到账户里去
        并更新昨结算和今结算
        positions合并
        计算持仓盈亏
        account进行更新

        """

        if self.backtest['position'].loc[0, '品种'] == None:
            time = self.backtest['marketdata']['时间'][0]
            # 如果当前没有持仓了
            # 计算account
            self.backtest['account'].loc[0, '时间'] = time
            self.backtest['account'].loc[0, '平仓盈亏'] = self.backtest['account'].loc[0, '平盯昨盈亏'] + \
                                                      self.backtest['account'].loc[0, '平盯今盈亏']
            self.backtest['account'].loc[0, '盯市盈亏'] = self.backtest['account'].loc[0, '盯昨盈亏'] + \
                                                      self.backtest['account'].loc[0, '盯今盈亏']
            self.backtest['account'].loc[0, '期末'] = self.backtest['account'].loc[0, '期初'] + \
                                                    self.backtest['account'].loc[0, '平仓盈亏'] + \
                                                    self.backtest['account'].loc[0, '盯市盈亏'] - \
                                                    self.backtest['account'].loc[0, '手续费']

            self.backtest['account'].loc[0, '保证金'] = 0
            self.backtest['account'].loc[0, '可用资金'] = self.backtest['account'].loc[0, '期末']
            self.backtest['account'].loc[0, '风险度'] = 0
            self.backtest['account'].loc[0, '多头市值'] = 0
            self.backtest['account'].loc[0, '空头市值'] = 0
            self.backtest['account'].loc[0, '市值'] = 0

            # 记录account
            self.backtest['account_record'] = self.backtest['account_record'].append(self.backtest['account'])

            # 这里要把account为下一衡量日调整
            self.backtest['account'].loc[0, '期初'] = self.backtest['account'].loc[0, '期末']
            self.backtest['account'].loc[0, '平盯今盈亏'] = 0
            self.backtest['account'].loc[0, '平盯昨盈亏'] = 0
            self.backtest['account'].loc[0, '平仓盈亏'] = 0
            self.backtest['account'].loc[0, '盯昨盈亏'] = 0
            self.backtest['account'].loc[0, '盯今盈亏'] = 0
            self.backtest['account'].loc[0, '盯市盈亏'] = 0
            self.backtest['account'].loc[0, '手续费'] = 0
            self.backtest['account'].loc[0, '期末'] = 0



        # 首先更新position
        elif self.backtest['position'].loc[0, '品种'] != None:
            for i in range(0, len(self.backtest['position'])):
                trading_unit = self.backtest['futures_info'][self.backtest['position'].loc[i, '品种']]['trading_unit']
                margin = self.backtest['futures_info'][self.backtest['position'].loc[i, '品种']]['margin'] + \
                         self.backtest['futures_info']['margin_add']
                num = self.backtest['position'].loc[i, '数量']
                time = self.backtest['marketdata'].loc[self.backtest['marketdata']['品种'] == self.backtest['position'].loc[i, '品种'], '时间'][0]
                last_p = self.backtest['marketdata'].loc[self.backtest['marketdata']['品种'] == self.backtest['position'].loc[i, '品种'], '昨收'][0]
                toda_p = self.backtest['marketdata'].loc[self.backtest['marketdata']['品种'] == self.backtest['position'].loc[i, '品种'], '今收'][0]
                open_p = self.backtest['position'].loc[i, '开仓价']
                self.backtest['position'].loc[i, '时间'] = time
                self.backtest['position'].loc[i, '昨收'] = last_p
                self.backtest['position'].loc[i, '今收'] = toda_p
                self.backtest['position'].loc[i, '逐笔盈亏'] = (toda_p - open_p) * trading_unit * num
                # 盯市盈亏计算后，直接修改account的情况
                if self.backtest['position'].loc[i, '盯开盘'] == '是':
                    self.backtest['position'].loc[i, '盯市盈亏'] = (toda_p - open_p) * trading_unit * num
                    if self.backtest['position'].loc[i, '多空'] == '多':
                        self.backtest['account'].loc[0, '盯今盈亏'] += self.backtest['position'].loc[i, '盯市盈亏']
                    elif self.backtest['position'].loc[i, '多空'] == '空':
                        self.backtest['account'].loc[0, '盯今盈亏'] -= self.backtest['position'].loc[i, '盯市盈亏']
                elif self.backtest['position'].loc[i, '盯开盘'] == '否':
                    self.backtest['position'].loc[i, '盯市盈亏'] = (toda_p - last_p) * trading_unit * num
                    if self.backtest['position'].loc[i, '多空'] == '多':
                        self.backtest['account'].loc[0, '盯昨盈亏'] += self.backtest['position'].loc[i, '盯市盈亏']
                    elif self.backtest['position'].loc[i, '多空'] == '空':
                        self.backtest['account'].loc[0, '盯昨盈亏'] -= self.backtest['position'].loc[i, '盯市盈亏']
                if self.backtest['position'].loc[i, '多空'] == '空':
                    self.backtest['position'].loc[i, '逐笔盈亏'] = -self.backtest['position'].loc[i, '逐笔盈亏']
                    self.backtest['position'].loc[i, '盯市盈亏'] = -self.backtest['position'].loc[i, '盯市盈亏']
                self.backtest['position'].loc[i, '市值'] = num * trading_unit * toda_p
                self.backtest['position'].loc[i, '保证金'] = num * trading_unit * toda_p * margin

            # 记录positon_record
            self.backtest['position_record'] = self.backtest['position_record'].append(self.backtest['position'])

            # 计算account
            self.backtest['account'].loc[0, '时间'] = time
            self.backtest['account'].loc[0, '平仓盈亏'] = self.backtest['account'].loc[0, '平盯昨盈亏'] + \
                                                      self.backtest['account'].loc[0, '平盯今盈亏']
            self.backtest['account'].loc[0, '盯市盈亏'] = self.backtest['account'].loc[0, '盯昨盈亏'] + \
                                                      self.backtest['account'].loc[0, '盯今盈亏']
            self.backtest['account'].loc[0, '期末'] = self.backtest['account'].loc[0, '期初'] + \
                                                      self.backtest['account'].loc[0, '平仓盈亏'] + \
                                                      self.backtest['account'].loc[0, '盯市盈亏'] - \
                                                      self.backtest['account'].loc[0, '手续费']

            self.backtest['account'].loc[0, '保证金'] = self.backtest['position']['保证金'].sum()
            self.backtest['account'].loc[0, '可用资金'] = self.backtest['account'].loc[0, '期末'] - self.backtest['account'].loc[0, '保证金']
            if self.backtest['account'].loc[0, '期末'] != 0:
                self.backtest['account'].loc[0, '风险度'] = self.backtest['account'].loc[0, '保证金']/self.backtest['account'].loc[0, '期末']
            else:
                self.backtest['account'].loc[0, '风险度'] = 0
            self.backtest['account'].loc[0, '多头市值'] = self.backtest['position'].loc[self.backtest['position']['多空'] == '多', '市值'].sum()
            if self.backtest['account'].loc[0, '多头市值'] == False:
                self.backtest['account'].loc[0, '多头市值'] = 0
            self.backtest['account'].loc[0, '空头市值'] = self.backtest['position'].loc[self.backtest['position']['多空'] == '空', '市值'].sum()
            if self.backtest['account'].loc[0, '空头市值'] == False:
                self.backtest['account'].loc[0, '空头市值'] = 0
            self.backtest['account'].loc[0, '市值'] = self.backtest['account'].loc[0, '多头市值'] + self.backtest['account'].loc[0, '空头市值']

            # 记录account
            self.backtest['account_record'] = self.backtest['account_record'].append(self.backtest['account'])

            # 这里要把account为下一衡量日调整
            self.backtest['account'].loc[0, '期初'] = self.backtest['account'].loc[0, '期末']
            self.backtest['account'].loc[0, '平盯今盈亏'] = 0
            self.backtest['account'].loc[0, '平盯昨盈亏'] = 0
            self.backtest['account'].loc[0, '平仓盈亏'] = 0
            self.backtest['account'].loc[0, '盯昨盈亏'] = 0
            self.backtest['account'].loc[0, '盯今盈亏'] = 0
            self.backtest['account'].loc[0, '盯市盈亏'] = 0
            self.backtest['account'].loc[0, '手续费'] = 0
            self.backtest['account'].loc[0, '期末'] = 0
            # positions
            if self.backtest['position'].loc[0, '品种'] == None:
                self.backtest['positions'] = self.positions_new()
            else:
                self.backtest['positions'] = self.positions_settle(self.backtest['marketdata'], self.backtest['position'])
            self.backtest['positions_record'] = self.backtest['positions_record'].append(self.backtest['positions'])

    def positions_settle(self, marketdata, position):
        positions = self.positions_new()
        for i in range(0, len(marketdata)):
            time = marketdata.loc[i, '时间']
            species = marketdata.loc[i, '品种']
            last_p = marketdata.loc[i, '昨收']
            toda_p = marketdata.loc[i, '今收']
            positions.loc[i, '时间'] = time
            positions.loc[i, '品种'] = species
            positions.loc[i, '昨收'] = last_p
            positions.loc[i, '今收'] = toda_p
            # 找到所有这个品种的持仓
            l_group = position.loc[(position['品种'] == species) & (position['多空'] == '多')]
            if l_group['数量'].sum() == False:
                positions.loc[i, '买持量'] = 0
                positions.loc[i, '买均价'] = 0
                positions.loc[i, '多头盯市'] = 0
                positions.loc[i, '多头逐笔'] = 0
                positions.loc[i, '多头保证金'] = 0
            else:
                positions.loc[i, '买持量'] = l_group['数量'].sum()
                price = 0
                for j in range(0, len(l_group)):
                    price += l_group.loc[l_group.index[j], '数量'] * l_group.loc[l_group.index[j], '开仓价']
                positions.loc[i, '买均价'] = price / positions.loc[i, '买持量']
                positions.loc[i, '多头盯市'] = l_group['盯市盈亏'].sum()
                positions.loc[i, '多头逐笔'] = l_group['逐笔盈亏'].sum()
                positions.loc[i, '多头保证金'] = l_group['保证金'].sum()


            s_group = position.loc[(position['品种'] == species) & (position['多空'] == '空')]
            if s_group['数量'].sum() == False:
                positions.loc[i, '卖持量'] = 0
                positions.loc[i, '卖均价'] = 0
                positions.loc[i, '空头盯市'] = 0
                positions.loc[i, '空头逐笔'] = 0
                positions.loc[i, '空头保证金'] = 0
            else:
                positions.loc[i, '卖持量'] = s_group['数量'].sum()
                price = 0
                for j in range(0, len(s_group)):
                    price += s_group.loc[s_group.index[j], '数量'] * s_group.loc[s_group.index[j], '开仓价']
                positions.loc[i, '卖均价'] = price / positions.loc[i, '卖持量']
                positions.loc[i, '空头盯市'] = s_group['盯市盈亏'].sum()
                positions.loc[i, '空头逐笔'] = s_group['逐笔盈亏'].sum()
                positions.loc[i, '空头保证金'] = s_group['保证金'].sum()
        # positions_record记录
        self.backtest['positions_record'].append(positions)
        return positions

    def backtest_record_save(self):
        self.backtest['marketdata_record'] = self.backtest['marketdata_record'].reset_index(drop=True)
        self.backtest['order_record'] = self.backtest['order_record'].reset_index(drop=True)
        self.backtest['position_record'] = self.backtest['position_record'].reset_index(drop=True)
        self.backtest['positions_record'] = self.backtest['positions_record'].reset_index(drop=True)
        self.backtest['trade'] = self.backtest['trade'].reset_index(drop=True)
        self.backtest['account_record'] = self.backtest['account_record'].reset_index(drop=True)

        marketcond1 = (self.backtest['marketdata_record'].iloc[0, 0] == None)
        marketcond2 = (self.backtest['marketdata_record'].iloc[0, 1] == None)
        if marketcond1 or marketcond2:
            self.backtest['marketdata_record'].drop([0], inplace=True)

        ordercond1 = (self.backtest['order_record'].iloc[0, 0] == None)
        ordercond2 = (self.backtest['order_record'].iloc[0, 1] == None)
        if ordercond1 or ordercond2:
            self.backtest['order_record'].drop([0], inplace=True)

        positioncond1 = (self.backtest['position_record'].iloc[0, 0] == None)
        positioncond2 = (self.backtest['position_record'].iloc[0, 1] == None)
        if positioncond1 or positioncond2:
            self.backtest['position_record'].drop([0], inplace=True)

        if self.backtest['positions_record'].iloc[0, 0] == None:
            self.backtest['positions_record'].drop([0], inplace=True)

        if self.backtest['trade'].iloc[0, 0] == None:
            self.backtest['trade'].drop([0], inplace=True)

        if self.backtest['account_record'].iloc[0, 0] == None:
            self.backtest['account_record'].drop([0], inplace=True)

        self.backtest['marketdata_record'] = self.backtest['marketdata_record'].reset_index(drop=True)
        self.backtest['order_record'] = self.backtest['order_record'].reset_index(drop=True)
        self.backtest['position_record'] = self.backtest['position_record'].reset_index(drop=True)
        self.backtest['positions_record'] = self.backtest['positions_record'].reset_index(drop=True)
        self.backtest['trade'] = self.backtest['trade'].reset_index(drop=True)
        self.backtest['account_record'] = self.backtest['account_record'].reset_index(drop=True)
        """
        self.backtest['marketdata'] = marketdata
        self.backtest['order'] = order
        self.backtest['position'] = position
        self.backtest['positions'] = positions
        self.backtest['account'] = account
        self.backtest['trade'] = trade
        self.backtest['strategyname'] = strategyname
        """

        filename = 'F:\BackTest\BackTest_Excel\\'
        filename = filename + self.backtest['strategyname'] + '.xlsx'
        if not os.path.exists(filename):
            wb = xlwt.Workbook()
            wb.add_sheet('marketdata')
            wb.add_sheet('order')
            wb.add_sheet('position')
            wb.add_sheet('positions')
            wb.add_sheet('trade')
            wb.add_sheet('account')
            # wb.add_sheet('summary')
            wb.save(filename)

        xlswriter = pd.ExcelWriter(filename)

        self.backtest['marketdata_record'].to_excel(xlswriter, sheet_name='marketdata')
        self.backtest['order_record'].to_excel(xlswriter, sheet_name='order')
        self.backtest['position_record'].to_excel(xlswriter, sheet_name='position')
        self.backtest['positions_record'].to_excel(xlswriter, sheet_name='positions')
        self.backtest['trade'].to_excel(xlswriter, sheet_name='trade')
        self.backtest['account_record'].to_excel(xlswriter, sheet_name='account')
        # marketdata.DataFrame.to_excel(filename, sheet_name='summary')
        xlswriter.save()
        # print(self.backtest['strategyname'], '   Save Done!!!')


if __name__ == '__main__':
    # 测试模仿
    self = order_driven_backtest('x')
    md = self.marketdata_new()
    order = self.order_new()

    md.loc[0, '时间'] = '2018-02-02 09:00:00'
    md.loc[0, '品种'] = 'rb'
    md.loc[0, '昨收'] = 4000
    md.loc[0, '今收'] = 4150
    md.loc[0, '是否结算'] = '否'


    order.loc[0, '时间'] = '2018-02-02 09:00:00'
    order.loc[0, '品种'] = 'rb'
    order.loc[0, '买卖'] = '买开'
    order.loc[0, '成交价'] = 4020
    order.loc[0, '数量'] = 20

    order.loc[1, '时间'] = '2018-02-02 09:05:00'
    order.loc[1, '品种'] = 'rb'
    order.loc[1, '买卖'] = '卖开'
    order.loc[1, '成交价'] = 4030
    order.loc[1, '数量'] = 20
    order.loc[2, '时间'] = '2018-02-02 09:10:00'
    order.loc[2, '品种'] = 'rb'
    order.loc[2, '买卖'] = '卖开'
    order.loc[2, '成交价'] = 4040
    order.loc[2, '数量'] = 20
    order.loc[3, '时间'] = '2018-02-02 09:15:00'
    order.loc[3, '品种'] = 'rb'
    order.loc[3, '买卖'] = '买开'
    order.loc[3, '成交价'] = 4050
    order.loc[3, '数量'] = 20

    order.loc[4, '时间'] = '2018-02-02 09:20:00'
    order.loc[4, '品种'] = 'rb'
    order.loc[4, '买卖'] = '卖平'
    order.loc[4, '成交价'] = 4060
    order.loc[4, '数量'] = 24

    self.process_control(md, order)
    md = self.marketdata_new()
    order = self.order_new()
    md.loc[0, '时间'] = '2018-02-02 09:30:00'
    md.loc[0, '品种'] = 'rb'
    md.loc[0, '昨收'] = 4020
    md.loc[0, '今收'] = 4040
    md.loc[0, '是否结算'] = '是'
    self.process_control(md, order)

    print("Done")