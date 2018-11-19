# -*- coding: utf-8 -*-
# author: WangYun 
# time :2018/10/15 
"""
ema refer
trade limination
"""
import pandas as pd
import scipy.io as sio
from strategy.ema_event import strategy_ema
import matplotlib.pyplot as plt
import datetime
import os
import xlwt
import math
import docx

class ema_refer:
    def __init__(self):
        # 初始化，保存当前日期
        nowdate = datetime.datetime.now()
        nowdate = datetime.datetime.strftime(nowdate, '%Y-%m-%d')
        self.nowdate = nowdate

    def ema_futures_list(self):
        # 要进行统计的数据
        li=['J201901','RB201901','BU201812','TA201901','AP201901',
            'CF201901','SR201901','MA201901','M201901','RU201901',
            'AU201812']
        # 这个函数很有用，合并文件名称
        return li

    def ema_futures_data_get(self, name):
        # 数据的读取
        data_file = r"F:\Quant\Data\Futures_KLine\Day"
        file_name = os.path.join(data_file, name + ".mat")
        matdata = sio.loadmat(file_name)
        df = []
        time_raw = matdata['time_str']
        data_raw = matdata['data']
        for i in range(0, len(time_raw)):
            df.append([time_raw[i][0][0], data_raw[i][0], data_raw[i][1], data_raw[i][2], data_raw[i][3]])
        data = pd.DataFrame(df, columns=['time', 'open', 'high', 'low', 'close'])
        data = data.set_index('time', drop=True)
        return data

    def ema_figure(self, data):
        fig = plt.figure(figsize=(20, 10), dpi=80, facecolor=[199 / 255, 238 / 255, 206 / 255], edgecolor='g')
        fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.15)
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor([199 / 255, 238 / 255, 206 / 255])
        min_ticks = math.floor(len(data) / 30)
        ax.set_xlabel('time')
        ax.set_ylabel('price')
        xtick = []
        for i in range(0, len(data), min_ticks):
            xtick.append(i)
        ax.set_xticks(xtick)
        xlable = []
        for i in xtick:
            xlable.append(str(data.index[i]))
        ax.set_xticklabels(xlable, rotation=90)
        ext = math.floor(0.01 * len(data))
        ax.set_xlim((0 - ext, len(data) + ext))
        # 这里规定了输入数据的格式，包括columns name，输入时如果格式不对，会报错
        t = data.index
        o = data['open']
        h = data['high']
        l = data['low']
        c = data['close']
        len_sum = len(c)
        # K线
        for i in range(0, len_sum):
            x0 = [i, i]
            y0 = [l[i], h[i]]
            ax.plot(x0, y0, color='k')
        for i in range(0, len_sum):
            if c[i] > o[i]:
                ax.fill_between([i - 0.5, i + 0.5], o[i], c[i], facecolor='r')
            else:
                ax.fill_between([i - 0.5, i + 0.5], o[i], c[i], facecolor='g')

        return fig, ax

    def ema_info(self, data, date, titlename):
        # 输入数据，日期，ema处理，返回：
        # 1 K线图与EMA交叉情况，2 ema信息
        # 输入数据的格式为DataFrame，index为日期
        fig, ax = self.ema_figure(data)
        ema = strategy_ema(10, 40)
        for i in range(0, len(data)):
            d = data.iloc[i]
            ema.ma_calculate(d['close'])
        line1, = ax.plot(ema.fast_ema, label='ema_fast')
        line2, = ax.plot(ema.slow_ema, label='ema_slow')
        ax.legend(handles=[line1,line2],labels=['ema_fast','ema_slow'])
        ax.set_title(titlename + '  ' + date)
        cond1 = ema.fast_ema[-1] > ema.slow_ema[-1]
        cond2 = ema.fast_ema[-2] < ema.slow_ema[-2]

        cond3 = ema.fast_ema[-1] < ema.slow_ema[-1]
        cond4 = ema.fast_ema[-2] > ema.slow_ema[-2]
        cond_info = ""
        if cond1 & cond2:
            cond_info = "down_to_up"
        elif cond3 & cond4:
            cond_info = "up_to_down"
        elif cond1 & cond4:
            cond_info = "keep_up"
        elif cond2 & cond3:
            cond_info = "keep_down"
        info = [date, titlename, cond_info]
        return fig, ax, info

    def ema_word(self):
        # 将图片插入word
        pass

    def ema_excel(self):
        # 将ema信息插入excel
        pass

    def futures_main(self):
        file_name = r'F:\daily_work'
        filename = os.path.join(file_name, self.nowdate)

        if not os.path.exists(filename):
            os.mkdir(filename)

        # 期货的ema监控
        li_ = self.ema_futures_list()
        all_info = []
        for li in li_:
            data = self.ema_futures_data_get(li)
            date = self.nowdate
            titlename = li
            fig, ax, info = self.ema_info(data, date, titlename)
            all_info.append(info)
            png_name = os.path.join(filename, titlename + '.png')
            plt.savefig(png_name)
            plt.close()


        file_name = r'F:\daily_work'
        filename = os.path.join(file_name, self.nowdate, self.nowdate + ".xlsx")

        if not os.path.exists(filename):
            wb = xlwt.Workbook()
            wb.add_sheet('ema')
            # wb.add_sheet('summary')
            wb.save(filename)

        xlswriter = pd.ExcelWriter(filename)

        df = pd.DataFrame(all_info, columns=['日期', '品种', '状态'])
        print(df)
        df.to_excel(xlswriter, sheet_name='ema')
        xlswriter.save()



def main():
    self = ema_refer()
    self.futures_main()
    """
    li = self.ema_futures_list()
    data = self.ema_futures_data_get("AU201812")
    self.ema_info(data,date='2018-10-15',titlename='AU201812')
    """
    pass




if __name__ == '__main__':
    main()