# -*- coding: utf-8 -*-
# author: WangYun 
# time :2018/9/25 


from backtest.Backtest_Data import dataload
from backtest.Backtest_Order_Drive import order_driven_backtest
from backtest.BackTest_Analysis import BackTestAnalysis
from strategy.jma_event import jmavalue

from data_get_save.futures_info import futures_info
import pandas as pd
import math
import time
import threading
import copy

class backtest_jma:
    # 构建最小模块
    def __init__(self):
        pass

    def time_print(self,strG):
        t = time.localtime(time.time())
        tS = time.strftime("%Y-%m-%d %H:%M:%S", t)
        print(tS + '  ' + strG)

    def log_wrong(self,strG):
        filename = r'F:\BackTest\Wrong_Log\log.txt'
        file_handle = open(filename, mode='a+')
        file_handle.write(strG + '\n')

    def spe_time_list(self):
        spe_list = ['ta', 'm', 'rb', 'v', 'ru', 'cu', 'j']
        time_list = [['2014-12-12 21:00:00', '2018-08-21 15:30:00'],
                     ['2014-12-26 21:00:00', '2018-08-21 15:30:00'],
                     ['2014-12-26 21:00:00', '2018-08-21 15:30:00'],
                     ['2009-05-25 09:00:00', '2018-08-21 15:30:00'],
                     ['2014-12-26 09:00:00', '2018-08-21 15:30:00'],
                     ['2013-12-20 21:00:00', '2018-08-21 15:30:00'],
                     ['2014-07-04 21:00:00', '2018-08-21 15:30:00'],
                     ]
        period_list = ['D']
        return spe_list, time_list, period_list

    def period_strategy_list(self):
        # 前面是快速线参数，后面是慢速线参数Length1, Lenght2, phase
        strategy_list = [[20, 25, 30, 35, 40, 45, 50, 55, 60], [6, 8, 10, 12, 14], [0]]

        return  strategy_list

    def analysis(self, strategy_name):
        class_analysis = BackTestAnalysis(strategy_name)
        try:
            class_analysis.backtest_main()
        except:
            self.log_wrong(strategy_name)
        self.time_print(strategy_name + ' analysis  Done')

    def analysis_all(self):
        spe_list, time_list, period_list = self.spe_time_list()
        strategy_list = self.period_strategy_list()

        for i in range(0, len(spe_list)):
            # 数据参数部分
            spe = spe_list[i]

            # 策略部分准备
            for Length_slow in strategy_list[0]:
                for Length_fast in strategy_list[1]:
                    # 回测参数
                    strategy_name = 'jma_' + spe + '_' + str(Length_slow) + '_' + str(Length_fast)
                    self.analysis(strategy_name)

    # 最小回测框架
    def min_unit(self, backtest_data, strategy_dict, backtest_dict):


        Length_slow = strategy_dict['Length_slow']
        Length_fast = strategy_dict['Length_fast']
        phase = strategy_dict ['phase']

        strategy_name = backtest_dict['name']
        initial_money = backtest_dict['initial_money']
        slip = backtest_dict['slip']

        self.time_print(strategy_name + '回测开始===========================')


        # 策略准备
        class_strategy_fast = jmavalue(Length_fast, phase)
        class_strategy_slow = jmavalue(Length_slow, phase)
        # 回测准备
        class_backtest = order_driven_backtest(strategy_name, slip, initial_money)

        #=============================循环开始=========================================
        for i in range(0, len(backtest_data)):
            if i == 0:
                self.time_print(str(0) + ' in ' + str(len(backtest_data)))
            elif i % 100 == 0:
                self.time_print(str(i) + ' in ' + str(len(backtest_data)))
            marketdata = pd.DataFrame(backtest_data.iloc[[i], :]).reset_index(drop=True)
            data = marketdata['今收'][0]
            position = pd.DataFrame(class_backtest.backtest['position'])
            account = pd.DataFrame(class_backtest.backtest['account'])
            # 初始化order
            order = class_backtest.order_new()
            ###########################################################
            # 快慢线计算
            class_strategy_fast.jma_calculate(data)
            class_strategy_slow.jma_calculate(data)

            # order计算
            # 过滤掉前120根K线，由于算法，导致前面的数据可信度不高
            datalen = len(class_strategy_fast.jma['data'])
            if datalen >= 120:
                # 计算仓位：以固定1手交易
                open_num = 1
                # 首次处理
                if datalen == 120:
                    # 如果快线超过慢线
                    if class_strategy_fast.jma['JMAValueBuffer'][-1] >= class_strategy_slow.jma['JMAValueBuffer'][-1]:
                        order.loc[0, '时间'] = marketdata.loc[0, '时间']
                        order.loc[0, '品种'] = marketdata.loc[0, '品种']
                        order.loc[0, '买卖'] = '卖开'
                        order.loc[0, '成交价'] = marketdata.loc[0, '今收']
                        order.loc[0, '数量'] = open_num
                    if class_strategy_fast.jma['JMAValueBuffer'][-1] < class_strategy_slow.jma['JMAValueBuffer'][-1]:
                        order.loc[0, '时间'] = marketdata.loc[0, '时间']
                        order.loc[0, '品种'] = marketdata.loc[0, '品种']
                        order.loc[0, '买卖'] = '买开'
                        order.loc[0, '成交价'] = marketdata.loc[0, '今收']
                        order.loc[0, '数量'] = open_num

                if position.loc[0, '多空'] == '多':
                    now_num = position['数量'][0]
                    if class_strategy_fast.jma['JMAValueBuffer'][-1] < class_strategy_slow.jma['JMAValueBuffer'][-1]:
                        order.loc[0, '时间'] = marketdata.loc[0, '时间']
                        order.loc[0, '品种'] = marketdata.loc[0, '品种']
                        order.loc[0, '买卖'] = '卖平'
                        order.loc[0, '成交价'] = marketdata.loc[0, '今收']
                        order.loc[0, '数量'] = now_num
                        order.loc[1, '时间'] = marketdata.loc[0, '时间']
                        order.loc[1, '品种'] = marketdata.loc[0, '品种']
                        order.loc[1, '买卖'] = '卖开'
                        order.loc[1, '成交价'] = marketdata.loc[0, '今收']
                        order.loc[1, '数量'] = open_num
                if position.loc[0, '多空'] == '空':
                    now_num = position['数量'][0]
                    if class_strategy_fast.jma['JMAValueBuffer'][-1] > class_strategy_slow.jma['JMAValueBuffer'][-1]:
                        order.loc[0, '时间'] = marketdata.loc[0, '时间']
                        order.loc[0, '品种'] = marketdata.loc[0, '品种']
                        order.loc[0, '买卖'] = '买平'
                        order.loc[0, '成交价'] = marketdata.loc[0, '今收']
                        order.loc[0, '数量'] = now_num
                        order.loc[1, '时间'] = marketdata.loc[0, '时间']
                        order.loc[1, '品种'] = marketdata.loc[0, '品种']
                        order.loc[1, '买卖'] = '买开'
                        order.loc[1, '成交价'] = marketdata.loc[0, '今收']
                        order.loc[1, '数量'] = open_num
                # 最后一根处理
                if len(class_strategy_fast.jma['data']) == len(backtest_data):
                    now_num = position['数量'][0]
                    if position.loc[0, '多空'] == '多':
                        order.loc[0, '时间'] = marketdata.loc[0, '时间']
                        order.loc[0, '品种'] = marketdata.loc[0, '品种']
                        order.loc[0, '买卖'] = '卖平'
                        order.loc[0, '成交价'] = marketdata.loc[0, '今收']
                        order.loc[0, '数量'] = now_num
                    if position.loc[0, '多空'] == '空':
                        order.loc[0, '时间'] = marketdata.loc[0, '时间']
                        order.loc[0, '品种'] = marketdata.loc[0, '品种']
                        order.loc[0, '买卖'] = '买平'
                        order.loc[0, '成交价'] = marketdata.loc[0, '今收']
                        order.loc[0, '数量'] = now_num
            #############################################################

            class_backtest.process_control(marketdata, pd.DataFrame(order))
        #=============================循环结束=========================================
        class_backtest.backtest_record_save()
        self.time_print(strategy_name + '回测结束==========================')

    def main(self):
        spe_list, time_list, period_list = self.spe_time_list()
        strategy_list = self.period_strategy_list()

        for i in range(0, len(spe_list)):
            # 数据参数部分
            spe = spe_list[i]
            begintime = time_list[i][0]
            endtime = time_list[i][1]
            period = period_list[0]

            # 首先，读取数据
            class_data = dataload(spe, begintime, endtime, period)
            backtest_data = class_data.backtest_data()

            # 策略部分准备
            for Length_slow in strategy_list[0]:


                # 策略参数
                phase = strategy_list[2][0]

                initialmoney = 1000000
                f_info = futures_info()
                commodity_info, finance_info, info = f_info.futures_info()
                info = info[spe]
                slip = info['min_change']*2
                """
                data_dict = {}
                data_dict['spe'] = spe
                data_dict['begintime'] = begintime
                data_dict['endtime'] = endtime
                data_dict['period'] = period
                """

                strategy_dict1 = {}
                strategy_dict1['Length_slow'] = Length_slow
                strategy_dict1['Length_fast'] = strategy_list[1][0]
                strategy_dict1['phase'] = phase
                strategy_dict2 = copy.deepcopy(strategy_dict1)
                strategy_dict2['Length_fast'] = strategy_list[1][1]
                strategy_dict3 = copy.deepcopy(strategy_dict1)
                strategy_dict3['Length_fast'] = strategy_list[1][2]
                strategy_dict4 = copy.deepcopy(strategy_dict1)
                strategy_dict4['Length_fast'] = strategy_list[1][3]
                strategy_dict5 = copy.deepcopy(strategy_dict1)
                strategy_dict5['Length_fast'] = strategy_list[1][4]


                # 回测参数
                strategy_name1 = 'jma_' + spe + '_' + str(Length_slow) + '_' + str(strategy_dict1['Length_fast'])
                strategy_name2 = 'jma_' + spe + '_' + str(Length_slow) + '_' + str(strategy_dict2['Length_fast'])
                strategy_name3 = 'jma_' + spe + '_' + str(Length_slow) + '_' + str(strategy_dict3['Length_fast'])
                strategy_name4 = 'jma_' + spe + '_' + str(Length_slow) + '_' + str(strategy_dict4['Length_fast'])
                strategy_name5 = 'jma_' + spe + '_' + str(Length_slow) + '_' + str(strategy_dict5['Length_fast'])



                backtest_dict1 = {}
                backtest_dict1['name'] = strategy_name1
                backtest_dict1['initial_money'] = initialmoney
                backtest_dict1['slip'] = slip
                backtest_dict2 = copy.deepcopy(backtest_dict1)
                backtest_dict2['name'] = strategy_name2
                backtest_dict3 = copy.deepcopy(backtest_dict1)
                backtest_dict3['name'] = strategy_name3
                backtest_dict4 = copy.deepcopy(backtest_dict1)
                backtest_dict4['name'] = strategy_name4
                backtest_dict5 = copy.deepcopy(backtest_dict1)
                backtest_dict5['name'] = strategy_name5


                # self.min_unit(data_dict, strategy_dict, backtest_dict)
                # 查看本地是否有文件，如果没有文件，继续
                if BackTestAnalysis(strategy_name1).strategy_exist():
                    continue

                t1 = threading.Thread(target=self.min_unit, args=(backtest_data, strategy_dict1, backtest_dict1,))
                t2 = threading.Thread(target=self.min_unit, args=(backtest_data, strategy_dict2, backtest_dict2,))
                t3 = threading.Thread(target=self.min_unit, args=(backtest_data, strategy_dict3, backtest_dict3,))
                t4 = threading.Thread(target=self.min_unit, args=(backtest_data, strategy_dict4, backtest_dict4,))
                t5 = threading.Thread(target=self.min_unit, args=(backtest_data, strategy_dict5, backtest_dict5,))
                t1.start()
                t2.start()
                t3.start()
                t4.start()
                t5.start()
                t1.join()
                t2.join()
                t3.join()
                t4.join()
                t5.join()
        #==========================策略分析========================
        self.analysis_all()








if __name__ == '__main__':
    self = backtest_jma()
    #self.analysis_all()
    data_dict = {}
    data_dict['spe'] = 'j'
    data_dict['begintime'] = '2014-07-04 21:00:00'
    data_dict['endtime'] = '2018-08-21 15:30:00'
    data_dict['period'] = 'D'

    strategy_dict = {}
    strategy_dict['Length_slow'] = 21
    strategy_dict['Length_fast'] = 5
    strategy_dict['phase'] = 0

    backtest_dict = {}
    backtest_dict['name'] = 'jma_j_21_5'
    backtest_dict['initial_money'] = 100000
    backtest_dict['slip'] = 1

    # self.min_unit(data_dict, strategy_dict, backtest_dict)
    # self.analysis_all()
    self.main()