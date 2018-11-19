# -*- coding: UTF-8 -*-
# author:@Jack.Wang
# time :2018/9/2 10:57


from data_get_save.futures_info_process import futures_cal
import datetime
import pandas as pd
import numpy as np


class futures_time(futures_cal):
    def __init__(self):
        futures_cal.__init__(self)
        self.now_time_datetime = datetime.datetime.now()
        self.now_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        self.now_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    # 输入交易品种和日期，计算当前交易日期对应交易品种的交易时间段
    def trade_time_period(self, id, date):
        # 输入品种，日期，获取交易时间段
        datepre = self.trade_day_pre_cal(date)
        info = self.futu_info
        info = info[id]
        trading_peirod = info['trading_period']
        trading_mode = info['trading_period_mode']
        period = []
        if int(trading_peirod[0][0][0:2]) > 18:
            period.append([datepre + ' ' + trading_peirod[0][0], datepre + ' ' + trading_peirod[0][1]])
            for i in range(1, len(trading_peirod)):
                period.append([date + ' ' + trading_peirod[i][0], date + ' ' + trading_peirod[i][1]])
        if int(trading_peirod[0][0][0:2]) < 18:
            for i in range(0, len(trading_peirod)):
                period.append([date + ' ' + trading_peirod[i][0], date + ' ' + trading_peirod[i][1]])
        return period
    # 交易日期前推计算
    def trade_day_pre_cal(self, date):
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        if date.weekday() == 6:
            datepre = date - datetime.timedelta(days=2)
        elif date.weekday() == 0:
            datepre = date - datetime.timedelta(days=3)
        else:
            datepre = date - datetime.timedelta(days=1)
        datepre = datetime.datetime.strftime(datepre, '%Y-%m-%d')
        return datepre
    # 交易日期后推计算
    def trade_day_next_cal(self, date):
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        if date.weekday() == 5:
            datepre = date + datetime.timedelta(days=2)
        elif date.weekday() == 4:
            datepre = date + datetime.timedelta(days=3)
        else:
            datepre = date + datetime.timedelta(days=1)
        datepre = datetime.datetime.strftime(datepre, '%Y-%m-%d')
        return datepre
    # 计算当前时间所属的交易日期
    def trade_day_now_cal(self):
        now = datetime.datetime.now()
        now_date = datetime.datetime.strftime(now, '%Y-%m-%d')
        if now.hour > 18:
            trade_date = self.trade_day_next_cal(now_date)
        else:
            trade_date = now_date
        return trade_date
    # 计算当前时间，品种的交易时间段
    def trade_period_now_cal(self, id):
        trade_date = self.trade_day_now_cal()
        period = self.trade_time_period(id, trade_date)
        return period
    # 根据品种，日期，合成该日期一分钟线的时间起始情况
    def trade_time_min(self, id ,date):
        # 先根据品种和日期，获得该日期的交易的时间段
        period = self.trade_time_period(id, date)
        min_period = []
        sec_one = datetime.timedelta(seconds=1)
        min_one = datetime.timedelta(minutes=1)
        for lar_pe in period:
            time_start = datetime.datetime.strptime(lar_pe[0], '%Y-%m-%d %H:%M:%S')
            time_end = datetime.datetime.strptime(lar_pe[1], '%Y-%m-%d %H:%M:%S')
            while True:
                if time_start < time_end:
                    min_period.append([datetime.datetime.strftime(time_start, '%Y-%m-%d %H:%M:%S'),
                                       datetime.datetime.strftime(time_start + min_one - sec_one, '%Y-%m-%d %H:%M:%S')])
                    time_start += min_one
                elif time_start == time_end:
                    break
                else:
                    break
        # 定位到当前时间段
        i = 0
        while True:
            ts = min_period[i][0]
            te = min_period[i][1]
            if self.now_time_datetime > datetime.datetime.strptime(te, '%Y-%m-%d %H:%M:%S'):
                min_period.remove(min_period[0])
                if len(min_period) == 0:
                    break
            else:
                break
        return min_period
    # 根据品种，日期，合成periods长度的分钟线
    def trade_time_min_periods(self, id, date, periods, periodnum):
        min_period = self.trade_time_min(id, date)
        one_second = datetime.timedelta(seconds=1)
        unit_minute = datetime.timedelta(minutes=periodnum)
        min_period = pd.DataFrame(min_period, columns=['时间'])
        min_period = min_period.reset_index(drop=False)
        min_period.columns = ['id', '时间']
        min_period['时间'] = pd.to_datetime(min_period['时间'])
        min_period.set_index('时间', inplace=True)
        timestart = min_period.resample(periods).first()
        timestart = timestart[~np.isnan(timestart['id'])]
        timestart = timestart.reset_index(drop=False)
        timestart['id'] = timestart['时间']
        timestart.columns = ['时段开始', '时段结束']
        timestart['时段结束'] = timestart['时段结束'] + unit_minute - one_second

        return timestart
    # 输入品种，起始日期，终止日期，获得日期的起始终止时间
    def trade_dayline_combine(self, spe, date_begin, date_end):
        day_period = []
        while True:
            period = self.trade_time_period(spe, date_begin)
            day_period.append([period[0][0], period[-1][1]])
            date_begin = self.trade_day_next_cal(date_begin)
            if date_begin <= date_end:
                pass
            else:
                break
        return day_period



def mytest():

    self = futures_time()
    print(self.trade_time_period('rb', '2018-06-01'))
    print(self.trade_day_pre_cal('2018-08-31'))
    print(self.trade_day_pre_cal('2018-09-03'))
    print(self.trade_day_next_cal('2018-08-31'))
    print(self.trade_day_next_cal('2018-09-03'))
    self.trade_time_min('cu', '2018-09-03')
    # self.trade_time_min_periods( 'cu', '2018-09-03', '30min', 30)
    peirod = self.trade_dayline_combine('cu', '2015-05-05', '2018-02-02')

if __name__ == '__main__':
    mytest()