# -*- coding: UTF-8 -*-
# author:@Jack.Wang



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


fig = plt.figure(figsize=(20, 10), dpi=80, facecolor=[199 / 255, 238 / 255, 206 / 255], edgecolor='g')
fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.15)
ax1 = fig.add_subplot(2, 1, 1,xlim=(0,2),ylim=(-1,1))
ax2 = fig.add_subplot(2, 1, 2,xlim=(0,2),ylim=(-1,1))
line1, = ax1.plot([],[],'r-')
line2, = ax2.plot([],[],'g*')
def init():
    line1.set_data([], [])
    line2.set_data([], [])
    return line1, line2

def animate(i):
    x = np.linspace(0, 2, 1000)
    y1 = np.sin(2*np.pi*(x-0.01*i))
    y2 = np.cos(2*np.pi*(x-0.01*i))
    line1.set_data(x, y1)
    line2.set_data(x, y2)
    return ax1,ax2

anima1 = animation.FuncAnimation(fig, animate, init_func=init,
                                 frames=10, interval=1)
plt.show()
"""
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
        self.num = 0
        fig = plt.figure(figsize=(20, 10), dpi=80, facecolor=[199 / 255, 238 / 255, 206 / 255], edgecolor='g')
        fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.15)
        self.fig = fig

        print('Done')

    def init(self):
        # 初始化图形

        ax1 = self.fig.add_subplot(2, 1, 1)
        ax2 = self.fig.add_subplot(2, 1, 2)
        ax1.set_facecolor([199 / 255, 238 / 255, 206 / 255])
        ax2.set_facecolor([199 / 255, 238 / 255, 206 / 255])

        return ax1, ax2


    def x_gen(self):
        self.num += 1
        return self.num


    def animation_plot(self):
        ani = animation.FuncAnimation(self.fig, self.update, range(0, len(self.macd.macd['data'])),
                                      interval=100, init_func=self.init)

    def update(self, num):
        t = self.data['时间']
        o = self.data['开盘价']
        h = self.data['最高价']
        l = self.data['最低价']
        c = self.data['收盘价']
        # K线
        for i in range(num, self.kline_num + num):
            x0 = [i, i]
            y0 = [l[i], h[i]]
            ax1.plot(x0, y0, color='k')
        for i in range(num, self.kline_num + num):
            if c[i] > o[i]:
                self.ax1.fill_between([i - 0.5, i + 0.5], o[i], c[i], facecolor='r')
            else:
                self.ax1.fill_between([i - 0.5, i + 0.5], o[i], c[i], facecolor='g')
        min_ticks = math.floor(self.kline_num / 30)
        # ax1.set_xlabel('time')
        # ax1.set_ylabel('price')

        xtick = []
        for i in range(num, self.kline_num + num, min_ticks):
            xtick.append(i)
        self.ax1.set_xticks(xtick)
        xlable = []
        for i in xtick:
            xlable.append(str(t[i]))

        self.ax2.plot(self.macd.macd['dif'][num:self.kline_num + num], '--g')
        self.ax2.plot(self.macd.macd['dea'][num:self.kline_num + num], '--r')
        zeros = []
        for i in range(num, self.kline_num + num):
            zeros.append(0)
        self.ax2.plot(zeros, 'k')

        for i in range(num, self.kline_num + num):
            if self.macd.macd['macd_pillar'][i] > 0:
                self.ax2.bar(i, self.macd.macd['macd_pillar'][i], facecolor='r')
            elif self.macd.macd['macd_pillar'][i] < 0:
                self.ax2.bar(i, self.macd.macd['macd_pillar'][i], facecolor='g')

        # ax2.set_ylim((-30,30))

        self.ax1.set_xticklabels(xlable, rotation=90)
        ext = math.floor(0.01 * len(o))

        self.ax1.set_xlim((num, self.kline_num + num))
        self.ax2.set_xlim((num, self.kline_num + num))
        ax1_y_max = h[num:self.kline_num + num].max() * 1.01
        ax1_y_min = l[num:self.kline_num + num].min() * 0.99
        x1_max = max(self.macd.macd['macd_pillar'][num:self.kline_num + num])
        x2_max = max(self.macd.macd['dif'][num:self.kline_num + num])
        x3_max = max(self.macd.macd['dea'][num:self.kline_num + num])
        x1_min = min(self.macd.macd['macd_pillar'][num:self.kline_num + num])
        x2_min = min(self.macd.macd['dif'][num:self.kline_num + num])
        x3_min = min(self.macd.macd['dea'][num:self.kline_num + num])
        ax2_y_max = max(x1_max, x2_max, x3_max)
        ax2_y_min = min(x1_min, x2_min, x3_min)
        # self.ax1.set_ylim(bottom=ax1_y_max,top=ax1_y_min)
        # self.ax2.set_ylim(bottom=ax2_y_max,top=ax2_y_min)
        self.ax1.set_ylim((ax1_y_min, ax1_y_max))
        self.ax2.set_ylim((ax2_y_min, ax2_y_max))
        # 重新设置lim
        plt.show()
        print('init Done')
        print('Done!')
        return ax1, ax2

    def mytest(self, data, macd):
        print('==============正在绘制交易K线图===============')
        t = data['时间']
        o = data['开盘价']
        h = data['最高价']
        l = data['最低价']
        c = data['收盘价']
        # 作图准备


        # plt.show()
        # 先画高底线
        for i in range(0, len(o)):
            x0 = [i, i]
            y0 = [l[i], h[i]]
            ax1.plot(x0, y0, color='k')


            x0 = [i-0.5, i+0.5]
            y0 = [c[i], c[i]]
            ax.plot(x0, y0, color='k')


        # 再画填充线
        for i in range(0, len(o)):
            if c[i] > o[i]:
                ax1.fill_between([i - 0.5, i + 0.5], o[i], c[i], facecolor='r')
            else:
                ax1.fill_between([i - 0.5, i + 0.5], o[i], c[i], facecolor='g')

        # 设置xticklable
        min_ticks = math.floor(len(o) / 30)
        # ax1.set_xlabel('time')
        # ax1.set_ylabel('price')

        xtick = []
        for i in range(0, len(o), min_ticks):
            xtick.append(i)
        ax1.set_xticks(xtick)
        xlable = []
        for i in xtick:
            xlable.append(str(t[i]))

        ax2.plot(macd.macd['dif'], '--g')
        ax2.plot(macd.macd['dea'], '--r')
        zeros = []
        for i in range(0, len(macd.macd['macd_pillar'])):
            zeros.append(0)
        ax2.plot(zeros, 'k')

        for i in range(0, len(macd.macd['macd_pillar'])):
            if macd.macd['macd_pillar'][i] > 0:
                ax2.bar(i, macd.macd['macd_pillar'][i], facecolor='r')
            elif macd.macd['macd_pillar'][i] < 0:
                ax2.bar(i, macd.macd['macd_pillar'][i], facecolor='g')


        # ax2.set_ylim((-30,30))

        ax1.set_xticklabels(xlable, rotation=90)
        ext = math.floor(0.01 * len(o))

        ax1.set_xlim((0 - ext, len(o) + ext))
        ax2.set_xlim((0 - ext, len(o) + ext))

        plt.annotate(r'dfsfsd',xy=(x0,y0),xycoords='data',xytext=(+30,-30),
                     textcoords='offset points',
                     arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=0.2'))
        plt.text(-3.7, 3, text_draw)


        plt.show()
        return fig, ax1, ax2
"""


