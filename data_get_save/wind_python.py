# -*- coding: UTF-8 -*-
# author:@Jack.Wang
# time :2018/8/21 16:33
"""
从wind获取数据
tick数据

"""

from WindPy import *
from data_get_save.PostgreSQL import PostgreSQL
from data_get_save.futures_info_process import futures_cal
from data_get_save.futures_time import futures_time
import time
import datetime
import numpy as np

class py_wind(PostgreSQL):
    def __init__(self):
        PostgreSQL.__init__(self, 'futures_tick')
        w.start()
        time.sleep(5)

    def wind_start(self, date): # 获取所有某一日期所有需要更新的list
        ###################################
        # 起始，终止时间处理
        # timebegin = '2018-08-22 09:00:00'
        # timeend = str(datetime.datetime.now())[0:19]
        f_t = futures_time()
        o_fcal = futures_cal()


        ####################################

        list_futures = o_fcal.commo_list
        info_futures = o_fcal.commo_info

        list_wind = []
        for id in list_futures:
            id = id.lower()

            codes = o_fcal.instrument_allcontract(id, date)
            for co in codes:

                field = 'last,volume,oi,limit_up,limit_down,bid1,bsize1,ask1,asize1'
                if info_futures[id]['exchange_id'] == 'shfe':
                    exchange_id = '.SHF'
                elif info_futures[id]['exchange_id'] == 'dce':
                    exchange_id = '.DCE'
                elif info_futures[id]['exchange_id'] == 'czce':
                    exchange_id = '.CZC'
                elif info_futures[id]['exchange_id'] == 'ine':
                    exchange_id = '.INE'
                elif info_futures[id]['exchange_id'] == 'cffex':
                    exchange_id = '.CFE'
                code = id.upper() + co[0][2:4] + co[1] + exchange_id
                ######################
                #tablename = code.split('.')[0].lower()
                #timebegin = self.wind_data_begintime(tablename)
                #####################
                period = f_t.trade_time_period(id, date)
                for per in period:
                    list_wind.append([code, field, per[0], per[1]])
        self.list_wind = list_wind
        self.wind_create_table()

    def wind_tick_data(self): # wind获取数据最小单元
        for li in self.list_wind:
            tablename = li[0].split('.')[0].lower()
            codes = li[0]
            field = li[1]
            begintime = li[2]
            endtime = li[3]
            data = w.wst(codes=codes, fields=field, beginTime=begintime, endTime=endtime)
            try:
                ti = data.Times
                la = data.Data[0]
                vo = data.Data[1]
                op = data.Data[2]
                up = data.Data[3]
                lo = data.Data[4]
                bip = data.Data[5]
                biv = data.Data[6]
                asp = data.Data[7]
                asv = data.Data[8]
                print(str(datetime.datetime.now()) + ' 正在存入数据 ' + codes + ' from ' + begintime + ' to ' + endtime)
                for i in range(0, len(ti)):
                    self.tick_insert(tablename, str(ti[i])[0:19], la[i], vo[i], op[i], up[i],
                                     lo[i], bip[i], biv[i], asp[i], asv[i])
            except IndexError:
                print(str(datetime.datetime.now()) + ' '+codes + '  wrong!!!')

    def wind_create_table(self): # 查看本地是否有此数据，如果没有，则创建table
        list_wind = self.list_wind
        for li in list_wind:
            tablename = li[0].split('.')[0].lower()
            self.tick_create_table(tablename)
        self.wind_tick_data()

    def wind_data_begintime(self, code):
        sql = r" SELECT %s from %s " % ('时间', code)
        self.cur.execute(sql)
        data = self.cur.fetchall()
        if len(data) != 0:
            timebegin = data[-1][0] + datetime.timedelta(seconds=1)
            timebegin = str(timebegin)
        else:
            timebegin = '2008-02-02 02:00:00'
        return timebegin


if __name__ == '__main__':
    # 测试
    # wind更新的tick数据，只能一天一天的更新，不能一下子输入很多天的日期，然后更新
    self = py_wind()
    # today = '2018-08-21'
    # today = datetime.datetime.today()
    # self.wind_list(today)
    # codes ='RB1901.SHF'
    # date_begin = '2018-08-20'
    # date_end = '2018-08-31'

    list_date = [['2018-08-24'],
                 ['2018-08-27'],
                 ['2018-08-28'],
                 ['2018-08-29'],
                 ['2018-08-30'],
                 ['2018-08-31'],
                 ['2018-09-03']]
    for li in list_date:
        self.wind_start(li[0])
    # codes = 'RB1901.SHF'

    # data = self.wind_get_tick_data(codes,  begintime, endtime)
    # tablename = 'rb1811'
    # self.select_data('rb1810', 'time,open,high,low')
    # self.create_table(tablename)
    # self.select_data('rb1810', 'time,open,high,low')