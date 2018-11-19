# -*- coding: utf-8 -*-
# author: WangYun 
# time :2018/9/22

from backtest.Backtest_Data import dataload
from backtest.Backtest_Order_Drive import order_driven_backtest
from backtest.BackTest_Analysis import BackTestAnalysis
from strategy.ma_event import strategy_ma

from data_get_save.futures_info import futures_info
import pandas as pd
import math
import time
import threading
import copy


# 构建最小模块
class backtest_ma:
    def __init__(self):
        pass

    def time_print(self,strG):
        t = time.localtime(time.time())
        tS = time.strftime("%Y-%m-%d %H:%M:%S", t)
        print(tS + '  ' + strG)

    def log_wrong(self,strG):
        filename = r'F:\BackTest\Wrong_Log\log.txt'
        file_handle = open(filename,mode='a+')
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
        spe_list = ['j']
        time_list = [
                     ['2014-07-04 21:00:00', '2018-08-21 15:30:00'],
                     ]
        period_list = ['D']
        return spe_list, time_list, period_list

    def period_strategy_list(self):
        # 前面是快速线参数，后面是慢速线参数Length1, Lenght2,
        strategy_list = [[20, 25, 30,35, 40, 45, 50, 55, 60],[7, 9, 10, 11, 13, 15]]
        strategy_list = [[40], [7, 9, 10, 11, 13, 15]]

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
            for slow in strategy_list[0]:
                for fast in strategy_list[1]:
                    # 回测参数
                    strategy_name = 'ma_' + spe + '_' + str(slow) + '_' + str(fast)
                    self.analysis(strategy_name)

    def min_unit(self, backtest_data, strategy_dict, backtest_dict):

        info = strategy_dict['info']
        fast = strategy_dict['fast_index']
        slow = strategy_dict['slow_index']


        strategy_name = backtest_dict['strategy_name']
        initialmoney = backtest_dict['initial_money']
        slip = backtest_dict['slip']


        # 策略类
        class_strategy = strategy_ma(fast, slow)
        # 回测类
        class_backtest = order_driven_backtest(strategy_name, slip, initialmoney)

        # ========================循环读取数据=================================================
        # 提取数据
        self.time_print(strategy_name + '回测开始===========================')
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
            class_strategy.ma_calculate(data)

            # order计算
            # 过滤掉前slow_index根K线，由于算法，导致前面的数据可信度不高
            datalen = len(class_strategy.data)
            if datalen >= class_strategy.slow_index:
                # 计算仓位：以固定1手交易
                open_num = 1
                # 首次处理
                if datalen == class_strategy.slow_index:
                    if class_strategy.slow_ma[-1] >= class_strategy.fast_ma[-1]:
                        order.loc[0, '时间'] = marketdata.loc[0, '时间']
                        order.loc[0, '品种'] = marketdata.loc[0, '品种']
                        order.loc[0, '买卖'] = '卖开'
                        order.loc[0, '成交价'] = marketdata.loc[0, '今收']
                        order.loc[0, '数量'] = open_num
                    if class_strategy.slow_ma[-1] < class_strategy.fast_ma[-1]:
                        order.loc[0, '时间'] = marketdata.loc[0, '时间']
                        order.loc[0, '品种'] = marketdata.loc[0, '品种']
                        order.loc[0, '买卖'] = '买开'
                        order.loc[0, '成交价'] = marketdata.loc[0, '今收']
                        order.loc[0, '数量'] = open_num

                if position.loc[0, '多空'] == '多':
                    now_num = position['数量'][0]
                    if class_strategy.slow_ma[-1] >= class_strategy.fast_ma[-1]:
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
                    if class_strategy.slow_ma[-1] < class_strategy.fast_ma[-1]:
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
                if len(class_strategy.data) == len(backtest_data):
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
        # =============================循环结束=========================================
        class_backtest.backtest_record_save()
        self.time_print(strategy_name + '回测结束==========================')

    def main(self):
        spe_list, time_list, period_list = self.spe_time_list()
        strategy_list = self.period_strategy_list()

        for i in range(0, len(spe_list)):

            spe = spe_list[i]
            begintime = time_list[i][0]
            endtime = time_list[i][1]
            # 回测数据获取
            class_data = dataload(spe, begintime, endtime, period_list[0])
            backtest_data = class_data.backtest_data()
            # 策略部分准备
            for slow in strategy_list[0]:

                strategy_name = 'ma_' + spe + '_' + str(slow) + '-' + str(strategy_list[1][0])
                # 分析类
                class_analysis = BackTestAnalysis(strategy_name)
                # 查看本地是否有文件，如果没有文件，继续
                if class_analysis.strategy_exist():
                    continue

                f_info = futures_info()
                commodity_info, finance_info, info = f_info.futures_info()
                info = info[spe]


                initialmoney = 1000000
                slip = info['min_change'] * 2

                backtest_dict = {}
                backtest_dict['strategy_name'] = strategy_name
                backtest_dict['initial_money'] = initialmoney
                backtest_dict['slip'] = slip


                strategy_dict1 = {}
                strategy_dict1['slow_index'] = slow
                strategy_dict1['fast_index'] = strategy_list[1][0]
                strategy_dict1['info'] = info
                strategy_dict2 = copy.deepcopy(strategy_dict1)
                strategy_dict2['fast_index'] = strategy_list[1][1]
                strategy_dict3 = copy.deepcopy(strategy_dict1)
                strategy_dict3['fast_index'] = strategy_list[1][2]
                strategy_dict4 = copy.deepcopy(strategy_dict1)
                strategy_dict4['fast_index'] = strategy_list[1][3]
                strategy_dict5 = copy.deepcopy(strategy_dict1)
                strategy_dict5['fast_index'] = strategy_list[1][4]
                strategy_dict6 = copy.deepcopy(strategy_dict1)
                strategy_dict6['fast_index'] = strategy_list[1][5]

                # 回测参数
                strategy_name1 = 'ma_' + spe + '_' + str(slow) + '_' + str(strategy_dict1['fast_index'])
                strategy_name2 = 'ma_' + spe + '_' + str(slow) + '_' + str(strategy_dict2['fast_index'])
                strategy_name3 = 'ma_' + spe + '_' + str(slow) + '_' + str(strategy_dict3['fast_index'])
                strategy_name4 = 'ma_' + spe + '_' + str(slow) + '_' + str(strategy_dict4['fast_index'])
                strategy_name5 = 'ma_' + spe + '_' + str(slow) + '_' + str(strategy_dict5['fast_index'])
                strategy_name6 = 'ma_' + spe + '_' + str(slow) + '_' + str(strategy_dict6['fast_index'])

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
                backtest_dict6 = copy.deepcopy(backtest_dict1)
                backtest_dict6['name'] = strategy_name6

                # self.min_unit(data_dict, strategy_dict, backtest_dict)
                # 查看本地是否有文件，如果没有文件，继续
                if BackTestAnalysis(strategy_name1).strategy_exist():
                    continue


                t1 = threading.Thread(target=self.min_unit, args=(backtest_data, strategy_dict1, backtest_dict1,))
                t2 = threading.Thread(target=self.min_unit, args=(backtest_data, strategy_dict2, backtest_dict2,))
                t3 = threading.Thread(target=self.min_unit, args=(backtest_data, strategy_dict3, backtest_dict3,))
                t4 = threading.Thread(target=self.min_unit, args=(backtest_data, strategy_dict4, backtest_dict4,))
                t5 = threading.Thread(target=self.min_unit, args=(backtest_data, strategy_dict5, backtest_dict5,))
                t6 = threading.Thread(target=self.min_unit, args=(backtest_data, strategy_dict6, backtest_dict6,))
                t1.start()
                t2.start()
                t3.start()
                t4.start()
                t5.start()
                t6.start()
                t1.join()
                t2.join()
                t3.join()
                t4.join()
                t5.join()
                t6.join()


        # 数据回测完之后，要分析
        self.analysis_all()


if __name__ == '__main__':
    self = backtest_ma()
    self.main()