# -*- coding: UTF-8 -*-
# author:@Jack.Wang
# time :2018/9/3 11:10

#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author:@Jack.Wang
"""
记录本地的local数据库
"""


import psycopg2
import pandas as pd

class local_trade:

    # 账户名称就是数据库名称
    def __init__(self, account):
        self.__database = 'trade'
        self.account = account
        # 默认自动连接
        self.connect()

    def connect(self):
        self.__user = "postgres"
        self.__password = "wangyun199"
        self.__host = "localhost"
        self.__port = "5432"
        self.conn = psycopg2.connect(database=self.__database, user=self.__user,
                                     password=self.__password, host=self.__host, port=self.__port)
        self.cur = self.conn.cursor()
        self.create_table_init()
        print("===================Python has connected to PostgreSQL!!!============================")
    def create_table_init(self):
        table_list = []
        talbe_list.append([[self.account + '_login'],[self.login_head()]])
        table_list.append([[self.account + '_onlogin'],[]])
        sql = r" create table %s ( %s ); " % (tablename, self.login_head())
        try:
            self.cur.execute(sql)
            self.conn.commit()
            print("Table %s created successfully" % tablename)
        except psycopg2.ProgrammingError:
            self.connect()
            self.conn.commit()

    def on_login_head(self):
        # 全部记录 #
        head = "LocalId serial NOT NULL, "
        head += "FFEXTime char, "
        head += "UserID char, "
        head += "TradingDay char, "
        head += "BrokerID char, "
        head += "SHFETime char, "
        head += "INETime char, "
        head += "DCETime char, "
        head += "LoginTime char, "
        head += "MaxOrderRef char, "
        head += "FrontID float4, "
        head += "SystemName char, "
        head += "SessionID float4, "
        head += r"PRIMARY KEY (LocalId)"
        return head

    def on_qryaccount_head(self):
        {'ReserveBalance': 0.0,
         'Reserve': 0.0,
         'SpecProductCommission': 0.0,
         'FrozenMargin': 0.0,
         'BrokerID': '9999',
         'CashIn': 0.0,
         'FundMortgageOut': 0.0,
         'FrozenCommission': 0.0,
         'SpecProductPositionProfitByAlg': 0.0,
         'Commission': 0.0,
         'SpecProductPositionProfit': 0.0,
         'Deposit': 0.0,
         'DeliveryMargin': 0.0,
         'TradingDay': '20180903',
         'CurrencyID': 'CNY',
         'Interest': 0.0,
         'PreDeposit': 938067.3300000001,
         'Available': 917307.3300000001,
         'SpecProductFrozenMargin': 0.0,
         'AccountID': '123609',
         'SpecProductMargin': 0.0,
         'PreFundMortgageOut': 0.0,
         'InterestBase': 0.0,
         'SpecProductExchangeMargin': 0.0,
         'PreBalance': 987385.8300000001,
         'Balance': 966625.8300000001,
         'MortgageableFund': 733845.8640000001,
         'Withdraw': 0.0,
         'SpecProductFrozenCommission': 0.0,
         'PreMortgage': 0.0,
         'SpecProductCloseProfit': 0.0,
         'WithdrawQuota': 733845.8640000001,
         'FundMortgageAvailable': 0.0,
         'BizType': '\x00',
         'PreCredit': 0.0,
         'FrozenCash': 0.0,
         'SettlementID': 1,
         'CloseProfit': 0.0,
         'ExchangeDeliveryMargin': 0.0,
         'Mortgage': 0.0,
         'Credit': 0.0,
         'CurrMargin': 49318.5,
         'FundMortgageIn': 0.0,
         'ExchangeMargin': 49318.5,
         'PreFundMortgageIn': 0.0,
         'PositionProfit': -20760.0,
         'PreMargin': 49318.5}

        tmp = {}
        tmp["投资者帐号"] = data["AccountID"]
        tmp["静态权益"] = data["PreBalance"]
        tmp["上次存款额"] = data["PreDeposit"]
        tmp["入金金额"] = data["Deposit"]
        tmp["出金金额"] = data["Withdraw"]
        tmp["冻结保证金"] = data["FrozenMargin"]
        tmp["总保证金"] = data["CurrMargin"]
        tmp["手续费"] = data["Commission"]
        tmp["平仓盈亏"] = data["CloseProfit"]
        tmp["持仓盈亏"] = data["PositionProfit"]
        tmp["动态权益"] = data["Balance"]
        tmp["可用资金"] = data["Available"]
        tmp["可取资金"] = data["WithdrawQuota"]
        tmp["交易日"] = data["TradingDay"]

    def position_head(self):
        {'ShortFrozen': 0,
         'FrozenMargin': 0.0,
         'BrokerID': '9999',
         'CashIn': 0.0,
         'FrozenCommission': 0.0,
         'UseMargin': 8424.0,
         'MarginRateByVolume': 0.0,
         'CloseProfitByDate': 0.0,
         'InstrumentID': 'ag1812',
         'StrikeFrozen': 0,
         'CombLongFrozen': 0,
         'CloseProfitByTrade': 0.0,
         'TodayPosition': 0,
         'TradingDay': '20180903',
         'CombShortFrozen': 0,
         'YdStrikeFrozen': 0,
         'PreSettlementPrice': 3510.0,
         'OpenVolume': 0,
         'CloseVolume': 0,
         'SettlementPrice': 3485.0,
         'OpenCost': 108000.0,
         'HedgeFlag': '1',
         'OpenAmount': 0.0,
         'StrikeFrozenAmount': 0.0,
         'InvestorID': '123609',
         'PositionCost': 105300.0,
         'LongFrozenAmount': 0.0,
         'ExchangeID': '',
         'PreMargin': 0.0,
         'CloseProfit': 0.0,
         'CloseAmount': 0.0,
         'LongFrozen': 0,
         'PosiDirection': '2',
         'CombPosition': 0,
         'YdPosition': 2,
         'PositionDate': '2',
         'AbandonFrozen': 0,
         'ShortFrozenAmount': 0.0,
         'FrozenCash': 0.0,
         'SettlementID': 1,
         'Position': 2,
         'ExchangeMargin': 8424.0,
         'MarginRateByMoney': 0.0,
         'PositionProfit': -750.0,
         'Commission': 0.0}


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



