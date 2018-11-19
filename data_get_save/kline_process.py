# -*- coding: UTF-8 -*-
# author:@Jack.Wang
# time :2018/9/1 16:03

"""
k线的处理工作，tick to minute，tick数据转成1分钟数据
分钟数据转成多分钟数据
分钟数据转成日线数据

"""
import numpy as np
import pandas as pd
import scipy.io as sio
from data_get_save.PostgreSQL import PostgreSQL
from data_get_save.futures_time import futures_time
import datetime

class kline_process:
    def __init__(self):
        pass


    def tick_to_minute(self, tick):
        df = pd.DataFrame(tick, columns=['日期时间', '最新价', '数量', '持仓量', '涨停板价', '跌停板价', '申买价一', '申买量一', '申卖价一', '申卖量一'])
        num = df['数量'].values
        numdiff = np.diff(num)
        df['数量diff'] = 0
        df['数量diff'].values[1:] = numdiff
        # df['数量diff'].values[0]=数量[0]

        df['日期时间'] = pd.to_datetime(df['日期时间'])
        df.set_index('日期时间', inplace=True)
        periodS = '1min'
        kdata = df.resample(periodS).last()
        kdata['开盘价'] = df['最新价'].resample(periodS).first()
        kdata['最高价'] = df['最新价'].resample(periodS).max()
        kdata['最低价'] = df['最新价'].resample(periodS).min()
        kdata['收盘价'] = df['最新价'].resample(periodS).last()
        kdata['数量'] = df['数量diff'].resample(periodS).sum()
        kdata['持仓量'] = df['持仓量'].resample(periodS).last()
        dd = kdata
        dd = dd[~np.isnan(dd['开盘价'])]
        dd = dd[['开盘价', '最高价', '最低价', '收盘价', '数量', '持仓量']]
        return dd

    def minute_combine(self, df, periods='30min'):
        print('正在合成数据......')
        kdata = df.resample(periods).last()
        kdata['开盘价'] = df['开盘价'].resample(periods).first()
        kdata['最高价'] = df['最高价'].resample(periods).max()
        kdata['最低价'] = df['最低价'].resample(periods).min()
        kdata['收盘价'] = df['收盘价'].resample(periods).last()
        kdata['成交量'] = df['成交量'].resample(periods).sum()
        kdata['持仓量'] = df['持仓量'].resample(periods).last()
        dd = kdata
        dd = dd[~np.isnan(dd['开盘价'])]
        dd = dd.drop(['时间'], axis=1)
        print('数据合成完毕......')
        return dd

    def minute_day(self, spe, begindate, enddate, df):
        # 数据合成日线，由于存在夜盘，和假日等信息，数据合成出现问
        # 此处需要交易日期的信息
        if len(begindate) > 10:
            begindate = begindate[0:10]
        if len(enddate) > 10:
            enddate = enddate[0:10]
        f_time = futures_time()
        period = f_time.trade_dayline_combine(spe, begindate, enddate)
        data = pd.DataFrame(columns=['时间', '开盘价','最高价','最低价','收盘价','成交量','持仓量'])
        for pe in period:
            time_start = pe[0]
            time_end = pe[1]
            da = df[df.index >= time_start]
            da = da[da.index <= time_end]
            # 存在数据
            if len(da) != 0:
                # 提取时间，开盘价，最高价，最低价，收盘价，成交量，持仓量等
                dic = {}
                dic['时间'] = [time_end[0:10]]
                dic['开盘价'] = [da['开盘价'][0]]
                dic['最高价'] = [da['最高价'].max()]
                dic['最低价'] = [da['最低价'].min()]
                dic['收盘价'] = [da['收盘价'][-1]]
                dic['成交量'] = [da['成交量'].sum()]
                dic['持仓量'] = [da['持仓量'][-1]]
                target_data = pd.DataFrame(dic)
                data = data.append(target_data, ignore_index=True)

        data.reset_index(drop=True)
        return data

def main():
    sql = PostgreSQL('backtest')
    data = sql.minute_select('j')
    data = pd.DataFrame(data, columns=['时间', '开盘价', '最高价', '最低价', '收盘价', '成交量', '持仓量'])
    data.set_index(['时间'], inplace=True)
    self = kline_process()
    spe = 'j'
    begindate = '2014-07-07'
    enddate = '2018-08-28'
    data = self.minute_day(spe, begindate, enddate, data)
    pass

if __name__ == '__main__':
    main()



    """
    data_list = []
    for i in range(0, len(data)):
        data_list.append(data.loc[i][0])
    data = data_list

    for d in data:
        self.macd_loop(d)
    """