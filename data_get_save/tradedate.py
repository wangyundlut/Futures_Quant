# -*- coding: UTF-8 -*-
# author:@Jack.Wang
# time :2018/8/23 15:48


import scipy.io as sio
from data_get_save.PostgreSQL import PostgreSQL as sql
import psycopg2
import pandas as pd

class tradeday(sql):
    def __init__(self):
        sql.__init__(self, 'tradeday')
        self.connect()

    def local_load(self):
        file_name = "F:\Quant\Data\StockIndex_KLine\Day_Index_mat\sh000001_D.mat"
        data = sio.loadmat(file_name)
        data = data['time_str']
        li = []
        for d in data:
            li.append(d[0][0])
        data = pd.Series(li)
        return data

    def sql_creat_table(self):
        tablename = 'tradeday'
        time = "tradeday date NOT NULL, "
        primarykey = r"PRIMARY KEY (tradeday)"
        head = time + primarykey
        sql = r" create table %s ( %s ); " % (tablename, head)
        try:
            self.cur.execute(sql)
            print("Table %s created successfully" % tablename)
            self.conn.commit()
        except psycopg2.ProgrammingError:
            self.close()
            self.connect()
            pass

    def sql_insert(self, tradeday):
        sql = r" INSERT INTO %s (tradeday)" \
              r" VALUES ( '%s' ); " \
              % ('tradeday', tradeday)
        self.cur.execute(sql)
        self.conn.commit()

    def init(self):
        self.sql_creat_table()
        date = self.local_load()
        for d in date:
            self.sql_insert(d)
        print('Done')

    def get_tradeday(self):
        sql = r" SELECT %s from %s " % ('tradeday', 'tradeday')
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def update_tradeday(self):
        pass


if __name__ == '__main__':
    self = tradeday()
    # data = self.local_load()
    # self.init()
    data = self.get()
    print("Done")