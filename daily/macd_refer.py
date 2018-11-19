# -*- coding: utf-8 -*-
# author:@Jack.Wang
# time :2018/9/12 19:21
"""
每天做macd的交易策略参考
想做什么品种，添加上什么品种
时间 品种 涨跌 四个价位 对应手数
"""
import pandas as pd
import scipy.io as sio
from strategy.macd_event import MACD_JW
from strategy.atr import atr_event
from data_get_save.futures_info import futures_info
import datetime
import os
import xlwt

class macd_refer:
    def __init__(self):
        self.money = 80000
        nowdate = datetime.datetime.now()
        nowdate = datetime.datetime.strftime(nowdate, '%Y-%m-%d')
        self.nowdate = nowdate

    def macd_list(self):
        li=['J201901','RB201901','BU201812','TA201901','AP201901',
            'CF201901','SR201901','MA201901','M201901','RU201901']
        return li

    def macd_data_read(self, name):
        data_file = r"F:\Quant\Data\Futures_KLine\Day" + "\\"
        file_name = data_file + name + ".mat"
        matdata = sio.loadmat(file_name)
        df = []
        time_raw = matdata['time_str']
        data_raw = matdata['data']
        for i in range(0, len(time_raw)):
            df.append([time_raw[i][0][0], data_raw[i][0], data_raw[i][1], data_raw[i][2], data_raw[i][3]])
        data = pd.DataFrame(df, columns=['time', 'open', 'high', 'low', 'close'])
        return data

    def macd_refer_excel(self, list_cal):
        filename = 'E:\交易养成\日期文件\\'
        filename += self.nowdate + '.xlsx'
        if not os.path.exists(filename):
            wb = xlwt.Workbook()
            wb.add_sheet('macd')
            # wb.add_sheet('summary')
            wb.save(filename)

        xlswriter = pd.ExcelWriter(filename)

        df = pd.DataFrame(list_cal, columns=['日期' ,'品种', '涨跌', '价一', '价二', '价三', '价四', '止损', '对应手数'])

        df.to_excel(xlswriter, sheet_name='macd')
        xlswriter.save()
        print(self.nowdate + '   has new infomation!!!')


    def main(self):
        macd = MACD_JW()
        atr = atr_event()
        f_info = futures_info()
        commodity_info, finance_info, info = f_info.futures_info()

        lis = self.macd_list()
        list_cal = [] # 时间 品种 涨跌 四个价位 止损 对应手数
        for li in lis:
            # 提取品种
            spe = ''
            for sp in li:
                if sp > '9':
                    spe = spe + sp
            spe = spe.lower()
            # 获取品种交易单位
            trading_unit = info[spe]['trading_unit']
            # 读取pandas形式的数据
            data = self.macd_data_read(li)
            # 将数据macd处理
            for d in range(0, len(data)):
                macd.macd_main(data.iloc[d])
            # atr处理
            for d in range(0, len(data)):
                atr.atr_main(data.iloc[d])
            # 根据当前资金，以及atr，计算当前对应手数
            mini_posi = self.money*0.01/trading_unit/atr.atr[-1]
            mini_posi = float('%.2f' % mini_posi)

            # 时间
            lasttime = macd.data[-1][0]
            # 品种
            species = li
            # 对应手数
            position = mini_posi
            # 加仓点位
            posiadd = 0.5*float('%.2f' % atr.atr[-1])

            # 如果是金叉
            if macd.gold_dead[-1] == 'gold':
                # 涨跌
                rise_or_fall = 'rise'
                # 四个价位
                p1 = macd.data[-1][4]
                p2 = p1 + posiadd
                p3 = p2 + posiadd
                p4 = p3 + posiadd
                stop = p1 - 2*posiadd
                list_cal.append([lasttime, species, rise_or_fall, p1, p2, p3, p4, stop, position])

            if macd.gold_dead[-1] == 'dead':
                # 涨跌
                rise_or_fall = 'fall'
                # 四个价位
                p1 = macd.data[-1][4]
                p2 = p1 - posiadd
                p3 = p2 - posiadd
                p4 = p3 - posiadd
                stop = p1 + 2 * posiadd
                list_cal.append([lasttime, species, rise_or_fall, p1, p2, p3, p4, stop, position])

        if len(list_cal) != 0:
            self.macd_refer_excel(list_cal)

        print('Done!')






def main():
    self = macd_refer()
    lis = self.macd_list()
    self.main()



if __name__ == '__main__':
    main()