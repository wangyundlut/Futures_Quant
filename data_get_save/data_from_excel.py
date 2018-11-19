# -*- coding: UTF-8 -*-
# author:@Jack.Wang
# time :2018/9/1 15:12

"""
从本地excel导入数据

"""
from data_get_save.PostgreSQL import PostgreSQL
import pandas as pd

class data_excel:
    def __init__(self):
        pass
    def database_connect(self, database, tablename):
        self.sql = PostgreSQL(database)
        self.sql.minute_create_table(tablename)

    def data_csv(self, tablename):
        filename = 'F:\BackTest\\'
        filename = filename + tablename + '.csv'
        marketdata = pd.read_csv(filename)
        for i in range(0, len(marketdata)):
            t = marketdata.iloc[i, 0]
            o = marketdata.iloc[i, 1]
            h = marketdata.iloc[i, 2]
            l = marketdata.iloc[i, 3]
            c = marketdata.iloc[i, 4]
            v = marketdata.iloc[i, 5]
            op = marketdata.iloc[i, 6]
            self.sql.minute_insert(tablename, t, o, h, l, c, v, op)
        print('Done')







def mytest():
    database = 'futures_min'
    tablename = 'j1901'
    self = data_excel()
    self.database_connect(database, tablename)
    self.data_csv(tablename)





if __name__ == '__main__':
    mytest()