# -*- coding: utf-8 -*-
# author:@Jack.Wang


from data_get_save.PostgreSQL import PostgreSQL
from data_get_save.kline_process import kline_process
import pandas as pd


class statistics_data:
    def __init__(self):
        pass
    def data_test(self): # 获取试验数据
        class_sql = PostgreSQL('backtest')
        j_data = class_sql.minute_select('rb')
        data = pd.DataFrame(j_data, columns=['时间', '开盘价', '最高价', '最低价', '收盘价', '成交量', '持仓量'])
        data.set_index(['时间'], inplace=True)
        class_pro= kline_process()
        spe = 'rb'
        begindate = '2014-12-29'
        enddate = '2018-08-21'
        data = class_pro.minute_day(spe, begindate, enddate, data)
        return data

    def data_test_paring(self):
        class_sql = PostgreSQL('backtest')
        rb_data = class_sql.minute_select('j')
        data = pd.DataFrame(rb_data, columns=['时间', '开盘价', '最高价', '最低价', '收盘价', '成交量', '持仓量'])
        data.set_index(['时间'], inplace=True)
        class_pro = kline_process()
        spe = 'j'
        begindate = '2014-12-29'
        enddate = '2018-08-21'
        data = class_pro.minute_day(spe, begindate, enddate, data)
        return data

    def data_test_m(self): # 获取试验数据
        class_sql = PostgreSQL('backtest')
        j_data = class_sql.minute_select('m')
        data = pd.DataFrame(j_data, columns=['时间', '开盘价', '最高价', '最低价', '收盘价', '成交量', '持仓量'])
        data.set_index(['时间'], inplace=True)
        class_pro= kline_process()
        spe = 'm'
        begindate = '2014-12-29'
        enddate = '2018-08-21'
        data = class_pro.minute_day(spe, begindate, enddate, data)
        return data



def main():
    test = statistics_data()
    data1 = test.data_test()
    data2 = test.data_test_paring()
    pass


if __name__ == '__main__':
    main()