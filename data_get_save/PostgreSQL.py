#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author:@Jack.Wang
"""
python 操作SQL的封装
tick数据格式
'日期时间','最新价','数量','持仓量','涨停板价','跌停板价',
'申买价一','申买量一','申卖价一',申卖量一'
"""


import psycopg2
import pandas as pd

class PostgreSQL:

    # 初始化，包括连接，设置光标
    def __init__(self, database):
        self.database = database
        # 默认自动连接
        self.connect()

    def connect(self):
        self.user = "postgres"
        self.password = "wangyun199"
        self.host = "localhost"
        self.port = "5432"
        self.conn = psycopg2.connect(database=self.database, user=self.user,
                                     password=self.password, host=self.host, port=self.port)
        self.cur = self.conn.cursor()
        print("===================Python has connected to PostgreSQL!!!============================")

    def minute_head(self):
        head = "时间 timestamp NOT NULL, "
        head += "开盘价 float4, "
        head += "最高价 float4, "
        head += "最低价 float4, "
        head += "收盘价 float4, "
        head += "成交量 int, "
        head += "持仓量 int, "
        head += r"PRIMARY KEY (时间)"
        return head

    def minute_select_head(self):
        head = '时间, 开盘价, 最高价, 最低价, 收盘价, 成交量, 持仓量 '
        return head

    def tick_select_head(self):
        head = '时间, 最新价, 数量, 持仓量, 涨停板价, 跌停板价, 申买一价, 申买一量, 申卖一价, 申卖一量'
        return head

    def tick_head(self):
        head = "id serial NOT NULL, "
        head += "时间 timestamp NOT NULL, "
        head += "最新价 float4, "
        head += "数量 int, "
        head += "持仓量 int, "
        head += "涨停板价 float4, "
        head += "跌停板价 float4, "
        head += "申买一价 float4, "
        head += "申买一量 int, "
        head += "申卖一价 float4, "
        head += "申卖一量 int, "
        head += r"PRIMARY KEY (id)"
        return head

    def sql_creat_table(self):
        pass

    def minute_create_table(self, tablename): # 创建minute,table操作
        sql = r" create table %s ( %s ); " % (tablename, self.minute_head())
        try:
            self.cur.execute(sql)
            self.conn.commit()
            print("Table %s created successfully" % tablename)
        except psycopg2.ProgrammingError:
            self.connect()
            self.conn.commit()


    def tick_create_table(self, tablename): # 创建tick，table
        sql = r" create table %s ( %s ); " % (tablename, self.tick_head())
        try:
            self.cur.execute(sql)
            self.conn.commit()
            print("Table %s created successfully" % tablename)
        except psycopg2.ProgrammingError:
            self.connect()
            self.conn.commit()


    def sql_insert(self):
        pass

    # 插入minute 操作
    def minute_insert(self, tablename, time, open, high, low, close, vol, opi):
        # # company open high low close 3 4 5 2
        sql = r" INSERT INTO %s (时间, 开盘价, 最高价, 最低价, 收盘价, 成交量, 持仓量 )" \
               r" VALUES ( '%s', %f, %f, %f, %f, %d, %d ); " \
               % (tablename, time, open, high, low, close, vol, opi)
        self.cur.execute(sql)
        self.conn.commit()

    # 插入tick 操作
    def tick_insert(self, tablename, time, lastprice, volume, opi, upper, lower, bidp, bidv, askp, askv):
        sql = r" INSERT INTO %s (时间, 最新价, 数量, 持仓量, 涨停板价, 跌停板价, 申买一价, 申买一量, 申卖一价, 申卖一量 )" \
              r" VALUES ( '%s', %f, %d, %d, %f, %f, %f, %d, %f, %d ); " \
              % (tablename, time, lastprice, volume, opi, upper, lower, bidp, bidv, askp, askv)
        self.cur.execute(sql)
        self.conn.commit()

    def sql_select(self):
        pass


    # 选取table操作
    def minute_select(self, tablename):
        # 'rb1810' 'time,open,high,low'
        sql = r" SELECT %s from %s " % (self.minute_select_head(), tablename)
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def tick_select(self, tablename):
        sql = r" SELECT %s from %s " % (self.tick_select_head(), tablename)
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def tick_select_time(self, tablename, timestart, timeend):
        sql = r" SELECT 时间, 最新价, 数量, 持仓量 from %s where 时间 between '%s' and '%s' " % (tablename, timestart, timeend)
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    # 更新
    def update(self, tablename, old, new):
        # company name = ""3"" " id = 4
        sql = r" UPDATE %s set %s where %s " % (tablename, old, new)
        self.cur.execute(sql)
        self.conn.commit()

    # 删除
    def delete(self, tablename, old):
        # company id = 3
        sql = r" DELETE from %s where %s ;" % (tablename, old)
        self.cur.execute(sql)
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
        print("Python has shut down the connection to PostgreSQL")





if __name__ == '__main__':
    # 测试
    self = PostgreSQL('futures_tick')
    tablename = 'j1901'
    timestart = '2018-08-31 23:20:00'
    timeend = '2018-08-31 23:25:00'
    self.tick_select_time(tablename, timestart, timeend)



    self = PostgreSQL('test')


    tablename = 'minutetable'
    self.minute_create_table('minutetable')
    self.minute_create_table('minutetable')
    time = '2018-02-02 09:00:00'
    open = 323
    high = 342
    low = 432
    close = 654
    vol = 242345
    opi = 2423423
    self.minute_create_table('minutetable')
    self.minute_insert(tablename, time, open, high, low, close, vol, opi)
    data = self.minute_select('minutetable')

    tablename = 'ticktable'
    time = '2018-02-02 09:00:00'
    close = 3233
    vol = 23423534
    opi = 432423
    self.tick_create_table('ticktable')
    self.tick_insert(tablename, time, close, vol, opi)
    data = self.tick_select('ticktable')
    print('Test DOne!!!!')



