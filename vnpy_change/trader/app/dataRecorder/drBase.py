#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
本文件中包含的数据格式和CTA模块通用，用户有必要可以自行添加格式。
'''



# 数据库名称
SETTING_DB_NAME = 'VnTrader_Setting_Db'
TICK_DB_NAME = 'FUTURES_Tick_Db'
DAILY_DB_NAME = 'FUTURES_Daily_Db'

MINUTE_DB_NAME = 'FUTURES_1Min_Db'
MINUTE_5_DB_NAME = 'FUTURES_5Min_Db'
MINUTE_30_DB_NAME = 'FUTURES_30Min_Db'
MINUTE_60_DB_NAME = 'FUTURES_60Min_Db'

# 行情记录模块事件
EVENT_DATARECORDER_LOG = 'eDataRecorderLog'     # 行情记录日志更新事件

# CTA引擎中涉及的数据类定义
from vnpy_change.trader.constant_common import EMPTY_UNICODE, EMPTY_STRING, EMPTY_FLOAT, EMPTY_INT
