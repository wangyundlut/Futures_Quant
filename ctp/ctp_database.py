#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author:@Jack.Wang
# time :2018/8/16 19:51

import psycopg2
class ctp_postgresql:

    # 初始化，包括连接，设置光标
    def __init__(self):
        print("Python connect to PostgreSQL has start!!!")
        database = "futures_tick"
        user = "postgres"
        password = "wangyun199"
        host = "localhost"
        port = "5432"
        self.conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()
        print("Python has connected to PostgreSQL!!!")

    # 创建table操作
    def create_table(self, tablename):
        # company open high low close
        id = "id serial NOT NULL, "
        time = "time timestamp NOT NULL, "
        # open = "open float4, "
        # high = "high float4, "
        # low = "low float4, "
        close = "close float4, "
        vol = "vol int, "
        opi = "opi int, "
        primarykey = "PRIMARY KEY (""id"")"
        key_list_head = id + time + close + vol + opi + primarykey
        sql = r" create table %s ( %s ); " % (tablename, key_list_head)
        self.cur.execute(sql)
        print("Table %s created successfully" % tablename)
        self.conn.commit()

    # 插入table操作
    def insert_data(self, tablename, time, close, vol, opi):
        # # company open high low close 3 4 5 2
        sql = r" INSERT INTO %s (time, close, vol, opi )" \
               r" VALUES ( '%s', %f, %d, %d ); " \
               % (tablename, time, close, vol, opi)
        self.cur.execute(sql)
        self.conn.commit()

    # Select table操作
    def select_data(self,tablename,key_list):
        # 'rb1810' 'time,open,high,low'
        sql = r" SELECT %s from %s " % (key_list, tablename)
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        return rows

    # 更新
    def sql_update(self,tablename, old, new):
        # company name = ""3"" " id = 4
        sql = r" UPDATE %s set %s where %s " % (tablename, old, new)
        self.cur.execute(sql)
        self.conn.commit()

    # 删除
    def sql_delete(self,tablename,old):
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
    self = ctp_postgresql()
    tablename = 'rb1811'
    # self.select_data('rb1810', 'time,open,high,low')
    # self.create_table(tablename)
    try:
        self.create_table(tablename)
    except psycopg2.ProgrammingError:
        self.close()
        self = ctp_postgresql()
        pass
    self.select_data('rb1810', 'time,open,high,low')

    # value = ' "2018-02-02 02:02:11" , 123, 456, 432, 432, 4234, 423'
    # self.insert_data(tablename, "2018-02-02 02:02:20", 123, 456, 432, 432, 4234, 423)