# -*- coding: UTF-8 -*-
# author:@Jack.Wang
# time :2018/8/27 10:03


import numpy as np
import matplotlib
# matplotlib.use('qt4agg')
from matplotlib.font_manager import *
import matplotlib.pyplot as plt
from matplotlib import animation
import math
from data_get_save.PostgreSQL import PostgreSQL
import pandas as pd
from data_get_save.kline_process import kline_process
from strategy.macd_event import MACD_JW
from matplotlib import animation
import time

#定义自定义字体，文件名从1.b查看系统中文字体中来
myfont = FontProperties(fname=r'c:\windows\fonts\simkai.ttf')

matplotlib.rcParams['axes.unicode_minus']=False
class ani_plot:
    def __init__(self):
        # 动图显示的k线根数
        self.kline_num = 100
        sql = PostgreSQL('backtest')
        data = sql.minute_select('j')
        data = pd.DataFrame(data, columns=['时间', '开盘价', '最高价', '最低价', '收盘价', '成交量', '持仓量'])
        data.set_index(['时间'], inplace=True)
        k_p = kline_process()
        spe = 'j'
        begindate = '2014-07-07'
        enddate = '2018-08-28'
        data = k_p.minute_day(spe, begindate, enddate, data)
        self.data = data
        macd = MACD_JW()
        for i in range(0, len(data)):
            macd.macd_loop(data.loc[i, '收盘价'])
        self.macd = macd
        print('数据Done')


    def myplot(self):
        fig = plt.figure(figsize=(20, 10), dpi=80, facecolor=[199 / 255, 238 / 255, 206 / 255], edgecolor='g')
        fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.15)
        self.fig = fig
        self.fig.show()
        time.sleep(10)
        print('是否显示图片？？？？')
        ax1 = self.fig.add_subplot(2, 1, 1)
        ax2 = self.fig.add_subplot(2, 1, 2)
        ax1.set_facecolor([199 / 255, 238 / 255, 206 / 255])
        ax2.set_facecolor([199 / 255, 238 / 255, 206 / 255])
        self.fig = fig
        self.ax1 = ax1
        self.ax2 = ax2
        self.fig.tight_layout(pad=1)


        t = self.data['时间']
        o = self.data['开盘价']
        h = self.data['最高价']
        l = self.data['最低价']
        c = self.data['收盘价']
        len_sum = len(c)
        self.len_sum = len_sum
        # K线
        for i in range(0,len_sum):
            x0 = [i, i]
            y0 = [l[i], h[i]]
            self.ax1.plot(x0, y0, color='k')
        for i in range(0,len_sum):
            if c[i] > o[i]:
                self.ax1.fill_between([i - 0.5, i + 0.5], o[i], c[i], facecolor='r')
            else:
                self.ax1.fill_between([i - 0.5, i + 0.5], o[i], c[i], facecolor='g')
        # 画金叉死叉图
        red, green = self.macd_rise_fall()
        # 先画点
        for i in range(0, len(red)):
            x0 = [red[i][0], red[i][1]]
            y0 = [c[red[i][0]], c[red[i][1]]]
            self.ax1.scatter(x0, y0, color='k')
        for i in range(0, len(green)):
            x0 = [green[i][0], green[i][1]]
            y0 = [c[green[i][0]], c[green[i][1]]]
            self.ax1.scatter(x0, y0, color='k')
        for i in range(0, len(red)):
            x0 = [red[i][0], red[i][1]]
            y0 = [c[red[i][0]], c[red[i][1]]]
            self.ax1.plot(x0, y0, '--r')
        for i in range(0, len(green)):
            x0 = [green[i][0], green[i][1]]
            y0 = [c[green[i][0]], c[green[i][1]]]
            self.ax1.plot(x0, y0, '-.g')


        min_ticks = math.floor(len_sum / 30)
        # ax1.set_xlabel('time')
        # ax1.set_ylabel('price')

        xtick = []
        for i in range(0,len_sum):
            xtick.append(i)
        self.ax1.set_xticks(xtick)
        self.ax2.set_xticks(xtick)
        self.ax1.set_xticklabels([])

        xlable = []
        for i in xtick:
            xlable.append(str(i))
        self.ax2.set_xticklabels(xlable, rotation=-30)
        #xlable = []
        #for i in xtick:
        #    xlable.append(str(t[i]))

        # 画dif，dea
        self.ax2.plot(self.macd.macd['dif'][0:len_sum], '--r')
        self.ax2.plot(self.macd.macd['dea'][0:len_sum], '-.g')
        zeros = []
        for i in range(0,len_sum):
            zeros.append(0)
        self.ax2.plot(zeros, 'k')
        # 画macd_pillar图
        for i in range(0,len_sum):
            if self.macd.macd['macd_pillar'][i] > 0:
                self.ax2.bar(i, self.macd.macd['macd_pillar'][i], facecolor='r')
            elif self.macd.macd['macd_pillar'][i] < 0:
                self.ax2.bar(i, self.macd.macd['macd_pillar'][i], facecolor='g')

        # ax2.set_ylim((-30,30))

        # self.ax1.set_xticklabels(xlable, rotation=90)

        ext = math.floor(0.01 * len(o))

        self.ax1.set_xlim((0, 100))
        self.ax2.set_xlim((0, 100))


        self.ax1.grid()
        self.ax2.grid()
        self.fig.show()

        for i in range(99, len_sum):
            self.fig_loop(i)
            """
            print(str(i))
            ax1_y_max = h[i-99:i].max() * 1.01
            ax1_y_min = l[i-99:i].min() * 0.99
            x1_max = max(self.macd.macd['macd_pillar'][i-99:i])
            x2_max = max(self.macd.macd['dif'][i-99:i])
            x3_max = max(self.macd.macd['dea'][i-99:i])
            x1_min = min(self.macd.macd['macd_pillar'][i-99:i])
            x2_min = min(self.macd.macd['dif'][i-99:i])
            x3_min = min(self.macd.macd['dea'][i-99:i])
            ax2_y_max = max(x1_max, x2_max, x3_max)
            ax2_y_min = min(x1_min, x2_min, x3_min)
            # self.ax1.set_ylim(bottom=ax1_y_max,top=ax1_y_min)
            # self.ax2.set_ylim(bottom=ax2_y_max,top=ax2_y_min)
            self.ax1.set_ylim((ax1_y_min, ax1_y_max))
            self.ax2.set_ylim((ax2_y_min, ax2_y_max))
            self.ax1.set_xlim((i - 99, i+0.49))
            self.ax2.set_xlim((i - 99, i+0.49))
            """

            # self.fig.show()
            # time.sleep(10)

    def fig_loop(self, i):
        len_sum = self.len_sum
        t = self.data['时间']
        o = self.data['开盘价']
        h = self.data['最高价']
        l = self.data['最低价']
        c = self.data['收盘价']

        ax1_y_max = h[i-99:i].max() * 1.01
        ax1_y_min = l[i-99:i].min() * 0.99
        x1_max = max(self.macd.macd['macd_pillar'][i-99:i])
        x2_max = max(self.macd.macd['dif'][i-99:i])
        x3_max = max(self.macd.macd['dea'][i-99:i])
        x1_min = min(self.macd.macd['macd_pillar'][i-99:i])
        x2_min = min(self.macd.macd['dif'][i-99:i])
        x3_min = min(self.macd.macd['dea'][i-99:i])
        ax2_y_max = max(x1_max, x2_max, x3_max)
        ax2_y_min = min(x1_min, x2_min, x3_min)
        # self.ax1.set_ylim(bottom=ax1_y_max,top=ax1_y_min)
        # self.ax2.set_ylim(bottom=ax2_y_max,top=ax2_y_min)
        self.ax1.set_ylim((ax1_y_min, ax1_y_max))
        self.ax2.set_ylim((ax2_y_min, ax2_y_max))
        self.ax1.set_xlim((i - 99, i+0.49))
        self.ax2.set_xlim((i - 99, i+0.49))

        self.fig.show()

        """
        
        # 重新设置lim
        """
    def macd_rise_fall(self):
        num = 2
        len_sum = self.len_sum
        red = []
        green = []
        macd = self.macd.macd['macd_pillar']
        if macd[1] < 0:
            green.append([1, 1])
        if macd[1] > 0:
            red.append([1, 1])
        while num <= len_sum-1:
            # 上一根是红柱子，这根还是红柱子
            if macd[num-1] > 0 and macd[num] > 0:
                num += 1
            # 上一根是红柱子，这根是绿柱子
            elif macd[num-1] > 0 and macd[num] < 0:
                # 先修改red，再增加green
                red[-1][1] = num
                green.append([num, num])
                num += 1
            # 上一根是绿柱子，这一根是红柱子
            elif macd[num-1] < 0 and macd[num] > 0:
                # 先修改green，再增加red
                green[-1][1] = num
                red.append([num, num])
                num += 1
            # 上一根是绿柱子，这一根是绿柱子
            elif macd[num-1] < 0 and macd[num] < 0:
                num += 1
            # 最后一根情况的修改
            if num == len_sum -1:
                if macd[num] > 0 and macd[num-1] > 0:
                    red[-1][1] = num
                if macd[num] < 0 and macd[num-1] < 0:
                    green[-1][1] = num
                break
        return red, green







if __name__ == '__main__':

    self = ani_plot()
    self.myplot()
    # self.fig_loop()
    print('Done')