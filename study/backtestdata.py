# -*- coding: UTF-8 -*-
# author:@Jack.Wang


"""
数据导入Phthon和导入到数据库里

"""
from data_get_save.futures_info_process import futures_cal
from data_get_save.PostgreSQL import PostgreSQL
import pandas as pd

class backtestdata(PostgreSQL):
    def __init__(self):
        PostgreSQL.__init__(self, 'backtest')
        self.connect()
        pass

    def data_load(self):
        fc = futures_cal()
        info_all = fc.futu_info
        """
        commo_list, fina_list = self.futures_list()
        commodity_info, finance_info = self.futures_info()
        commo_list = ['CU', 'AP', 'CS', 'JD', 'PP', 'V', 'SC']
        for fi in fina_list:
            commo_list.append(fi)
        # 读入数据
        """
        commo_list = ['J']

        filename = r'F:\tbdata'

        for code in commo_list:
            tablename = code.lower()
            self.minute_create_table(code.lower())
            info = info_all[code.lower()]

            time_start = info['begintime_local']
            time_end = '2018-08-28 23:29:00'

            file = filename + '\\' + code.lower() + '.csv'
            data = pd.read_csv(file)
            # 数据处理
            data.columns = ['time','open','high','low','close','vol','opi']
            # 时间转化
            data['time'] = pd.to_datetime(data['time'])
            data.set_index(['time'], inplace=True)
            data = data[(data.index >= time_start)]
            data = data[(data.index <= time_end)]
            for i in range(0, len(data)):
                time = data.index[i]
                open = data['open'][i]
                high = data['high'][i]
                low = data['low'][i]
                close = data['close'][i]
                vol = int(data['vol'][i])
                opi = int(data['opi'][i])
                self.minute_insert(tablename, time, open, high, low, close, vol, opi)
            print(tablename + 'Done!')





if __name__ == '__main__':
    self = backtestdata()
    self.data_load()

