#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
将所有主引擎的事件儿类型添加至此
主引擎通用的所有事件儿，在此，各个APP模块还会有其他的事件儿，在模块中添加
'''

# 系统相关
EVENT_TIMER = 'eTimer'                  # 计时器事件，每隔1秒发送一次
EVENT_LOG = 'eLog'                      # 日志事件，全局通用

# Gateway相关
EVENT_TICK = 'eTick.'                   # TICK行情事件，可后接具体的vtSymbol
EVENT_TRADE = 'eTrade.'                 # 成交回报事件
EVENT_ORDER = 'eOrder.'                 # 报单回报事件
EVENT_POSITION = 'ePosition.'           # 持仓回报事件
EVENT_ACCOUNT = 'eAccount.'             # 账户回报事件
EVENT_CONTRACT = 'eContract.'           # 合约基础信息回报事件
EVENT_ERROR = 'eError.'                 # 错误回报事件
EVENT_HISTORY = 'eHistory.'             # K线数据查询回报事件

EVENT_BAR_01MIN = 'eBar01min'           # 01分钟K线事件
EVENT_BAR_05MIN = 'eBar05min'           # 05分钟K线事件
EVENT_BAR_15MIN = 'eBar15min'           # 15分钟K线事件
EVENT_BAR_30MIN = 'eBar30min'           # 30分钟K线事件
EVENT_BAR_60MIN = 'eBar60min'           # 60分钟K线事件