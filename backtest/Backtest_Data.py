# -*- coding: UTF-8 -*-
# author:@Jack.Wang
# time :2018/8/23 20:09

"""
数据加载部分
主要为:
1 获取本地指数数据
2 合成分钟K线
"""

import pandas as pd
import time
import numpy as np
from data_get_save.PostgreSQL import PostgreSQL
from data_get_save.kline_process import kline_process



class dataload(PostgreSQL):

    def __init__(self, spe, begintime, endtime, periods):
        PostgreSQL.__init__(self, 'backtest')
        self.spe = spe
        self.begintime = begintime
        self.endtime = endtime
        self.periods = periods

    def time_print(self, strG):
        t = time.localtime(time.time())
        tS = time.strftime("%Y-%m-%d %H:%M:%S", t)
        print(tS + '  ' + strG)


    def backtest_data_get(self):
        tablename = self.spe
        self.time_print('正在获取数据......')
        data = self.minute_select( tablename)
        data = pd.DataFrame(data, columns=['时间', '开盘价', '最高价', '最低价', '收盘价', '成交量', '持仓量'])
        data.set_index(data['时间'], inplace=True)
        # hash算法找时间
        data = data[(data.index >= self.begintime)]
        data = data[(data.index <= self.endtime)]
        self.time_print('数据获取完毕......')
        self.data = data

    def kline_combine(self):
        self.time_print('数据正在合成......')
        data = self.data
        periodS = self.periods
        obj_klineprocess = kline_process()
        spe = self.spe
        begindate = self.begintime
        enddate = self.endtime
        if periodS == 'D':
            period_data = obj_klineprocess.minute_day(spe, begindate, enddate, data)
            period_data.set_index('时间', inplace=True)
            self.time_print('日线数据合成完毕......')
        else:
            period_data = obj_klineprocess.minute_combine(data, periods=periodS)
            self.time_print('分钟数据合成完毕......')
        self.period_data = period_data

    def backtest_data(self):

        self.backtest_data_get()
        self.kline_combine()
        data = self.period_data
        data = data.reset_index(drop=False)
        #### 组合出昨收
        data.columns = ['时间', '开盘', '最高', '最低', '今收', '成交', '持仓']
        last_close = pd.DataFrame(data['今收'])
        #### 准备一个None的DataFrame
        tempt = pd.DataFrame(last_close['今收'].head(1))
        ### 是否结算，应该结合时间，有个算法，此处暂时简单处理
        # self.settle_cal('time'， periods, mode)
        settle = pd.DataFrame(last_close['今收'])
        settle['今收'] = '是'
        settle.columns = ['是否结算']
        # 品种
        spe = pd.DataFrame(last_close['今收'])
        spe['今收'] = self.spe
        spe.columns = ['品种']
        ##########
        tempt.loc[0, '今收'] = None
        tempt = tempt.append(last_close)
        tempt.drop([tempt.index[-1]], inplace=True)
        last_close = tempt.reset_index(drop=True)
        last_close.columns = ['昨收']
        # 合并
        data.insert(1, '昨收', last_close)
        data.insert(6, '是否结算', settle)
        data.insert(1, '品种', spe)
        # 删除
        data.drop(['持仓', '成交'], axis=1, inplace=True)

        return data

    def settle_cal(self, time, periods=None, mode=None):
        pass

def main():
    id = 'rb'
    begintime = '2014-12-26 21:00:00'
    endtime = '2018-08-21 15:00:00'
    periods = 'D'
    periods = 'H'
    self = dataload(id, begintime, endtime, periods)
    data = self.backtest_data()
    self.backtest_data_get()
    self.kline_combine()
    pass


if __name__ == '__main__':
    main()
