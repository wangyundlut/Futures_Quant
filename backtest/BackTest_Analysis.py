# -*- coding: UTF-8 -*-
# author:@Jack.Wang
# time :2018/8/28 8:46

import matplotlib.pyplot as plt
import math
import time
import pandas as pd
import numpy as np
import os
from openpyxl import load_workbook

"""
策略分析：
1 资金曲线图保存
2 年化盈利
3 年化收益
4 夏普比率
5 最大回撤
6 胜率
7 策略盈亏比
8 交易天数


"""


class BackTestAnalysis:
    def __init__(self, strategyname):
        # print('==============策略数据读取开始================')
        filename = 'F:\BackTest\BackTest_Excel\\'
        filename = filename + strategyname + '.xlsx'
        self.strategyname = strategyname
        self.filename = filename
        # print('==============策略数据读取完毕================')

    def backtest_main(self):
        filename = self.filename
        marketdata = pd.read_excel(filename, sheet_name='marketdata')
        order = pd.read_excel(filename, sheet_name='order')
        position = pd.read_excel(filename, sheet_name='position')
        positions = pd.read_excel(filename, sheet_name='positions')
        account = pd.read_excel(filename, sheet_name='account')
        trade = pd.read_excel(filename, sheet_name='trade')
        marketdata = marketdata.to_dict()
        order = order.to_dict()
        position = position.to_dict()
        positions = positions.to_dict()
        account = account.to_dict()
        trade = trade.to_dict()
        self.marketdata = marketdata
        self.order = order
        self.position = position
        self.positions = positions
        self.account = account
        self.trade = trade

        # 画K线和
        """
        fig, ax = self.KLine()
        time.sleep(10)
        self.trade_show()
        self.money_trace()

        time.sleep(5)
        self.analysis()
        self.trade_times()
        
        """




        # return fig, ax

    def strategy_exist(self):
        filename = 'F:\BackTest\BackTest_Excel\\'
        filename = filename + self.strategyname + '.xlsx'
        flag = os.path.exists(filename)
        return flag


    def KLine(self):
        # 数据准备
        print('==============正在绘制交易K线图===============')
        data = self.marketdata
        order = self.order
        t = data['时间']
        o = data['开盘']
        h = data['最高']
        l = data['最低']
        c = data['今收']
        # 作图准备

        fig = plt.figure(figsize=(20, 10), dpi=80, facecolor=[199/255, 238/255, 206/255], edgecolor='g')
        fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.15)
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor([199 / 255, 238 / 255, 206 / 255])
        # 先画高底线
        for i in range(0, len(o)):
            x0 = [i, i]
            y0 = [l[i], h[i]]
            ax.plot(x0, y0, color='k')
            """
            x0 = [i-0.5, i+0.5]
            y0 = [c[i], c[i]]
            ax.plot(x0, y0, color='k')
            """

        # 再画填充线
        for i in range(0, len(o)):
            if c[i] > o[i]:
                ax.fill_between([i-0.5, i+0.5], o[i], c[i], facecolor='r')
            else:
                ax.fill_between([i-0.5, i+0.5], o[i], c[i], facecolor='g')

        # 设置xticklable
        min_ticks = math.floor(len(o)/30)
        ax.set_xlabel('time')
        ax.set_ylabel('price')

        xtick = []
        for i in range(0, len(o), min_ticks):
            xtick.append(i)
        ax.set_xticks(xtick)
        xlable = []
        for i in xtick:
            xlable.append(str(t[i]))
        ax.set_xticklabels(xlable, rotation=90)
        ext = math.floor(0.01 * len(o))
        ax.set_xlim((0 - ext, len(o) + ext))
        ylimfix = ax.get_ylim()
        ax.set_ylim(ylimfix)
        ax.set_title(self.strategyname)
        order = pd.DataFrame(order)

        # 画order
        for i in range(0, len(t)):
            text_draw = ''
            o_group = order.loc[order['时间'] == t[i]]
            # 提取text
            for j in range(0, len(o_group)):
                num = o_group.loc[o_group.index[j], '数量']
                price = o_group.loc[o_group.index[j], '成交价']
                if o_group.loc[o_group.index[j], '买卖'] == '买开':
                    text_draw +=u'longopen' + str(num)
                    x0 = [i - 0.6, i + 0.6]
                    y0 = [price, price]
                    ax.plot(x0, y0, color='blue')
                    plt.annotate(text_draw, xy=(i+0.6, price))
                elif o_group.loc[o_group.index[j], '买卖'] == '卖平':
                    text_draw +=u'sellclose' + str(num)
                    x0 = [i - 0.6, i + 0.6]
                    y0 = [price, price]
                    ax.plot(x0, y0, color='blue')
                    plt.annotate(text_draw, xy=(i + 0.6, price))
                elif o_group.loc[o_group.index[j], '买卖'] == '卖开':
                    text_draw +=u'shortopen' + str(num)
                    x0 = [i - 0.6, i + 0.6]
                    y0 = [price, price]
                    ax.plot(x0, y0, color='purple')
                    plt.annotate(text_draw, xy=(i + 0.6, price))
                elif o_group.loc[o_group.index[j], '买卖'] == '买平':
                    text_draw +=u'buyclose' + str(num)
                    x0 = [i - 0.6, i + 0.6]
                    y0 = [price, price]
                    ax.plot(x0, y0, color='purple')
                    plt.annotate(text_draw, xy=(i + 0.6, price))

            """
            plt.annotate(r'dfsfsd',xy=(x0,y0),xycoords='data',xytext=(+30,-30),
                         textcoords='offset points',
                         arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=0.2'))
            plt.text(-3.7, 3, text_draw)
            """

        plt.show()
        return fig, ax

    def Kline_MACD(self):
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
        for i in range(0, len_sum):
            x0 = [i, i]
            y0 = [l[i], h[i]]
            self.ax1.plot(x0, y0, color='k')
        for i in range(0, len_sum):
            if c[i] > o[i]:
                self.ax1.fill_between([i - 0.5, i + 0.5], o[i], c[i], facecolor='r')
            else:
                self.ax1.fill_between([i - 0.5, i + 0.5], o[i], c[i], facecolor='g')
        min_ticks = math.floor(len_sum / 30)
        # ax1.set_xlabel('time')
        # ax1.set_ylabel('price')

        xtick = []
        for i in range(0, len_sum):
            xtick.append(i)
        self.ax1.set_xticks(xtick)
        self.ax2.set_xticks(xtick)
        self.ax1.set_xticklabels([])
        # xlable = []
        # for i in xtick:
        #    xlable.append(str(t[i]))

        self.ax2.plot(self.macd.macd['dif'][0:len_sum], '--r')
        self.ax2.plot(self.macd.macd['dea'][0:len_sum], '-.g')
        zeros = []
        for i in range(0, len_sum):
            zeros.append(0)
        self.ax2.plot(zeros, 'k')

        for i in range(0, len_sum):
            if self.macd.macd['macd_pillar'][i] > 0:
                self.ax2.bar(i, self.macd.macd['macd_pillar'][i], facecolor='r')
            elif self.macd.macd['macd_pillar'][i] < 0:
                self.ax2.bar(i, self.macd.macd['macd_pillar'][i], facecolor='g')

        # ax2.set_ylim((-30,30))

        # self.ax1.set_xticklabels(xlable, rotation=90)

        ext = math.floor(0.01 * len(o))

        self.ax1.set_xlim((0, 100))
        self.ax2.set_xlim((0, 100))
        xlable = []
        for i in xtick:
            xlable.append(str(i))
        self.ax2.set_xticklabels(xlable, rotation=-30)

        self.ax1.grid()
        self.ax2.grid()
        self.fig.show()

        for i in range(99, len_sum):
            self.fig_loop(i)
        """
        len_sum = self.len_sum
        t = self.data['时间']
        o = self.data['开盘价']
        h = self.data['最高价']
        l = self.data['最低价']
        c = self.data['收盘价']

        ax1_y_max = h[i - 99:i].max() * 1.01
        ax1_y_min = l[i - 99:i].min() * 0.99
        x1_max = max(self.macd.macd['macd_pillar'][i - 99:i])
        x2_max = max(self.macd.macd['dif'][i - 99:i])
        x3_max = max(self.macd.macd['dea'][i - 99:i])
        x1_min = min(self.macd.macd['macd_pillar'][i - 99:i])
        x2_min = min(self.macd.macd['dif'][i - 99:i])
        x3_min = min(self.macd.macd['dea'][i - 99:i])
        ax2_y_max = max(x1_max, x2_max, x3_max)
        ax2_y_min = min(x1_min, x2_min, x3_min)
        # self.ax1.set_ylim(bottom=ax1_y_max,top=ax1_y_min)
        # self.ax2.set_ylim(bottom=ax2_y_max,top=ax2_y_min)
        self.ax1.set_ylim((ax1_y_min, ax1_y_max))
        self.ax2.set_ylim((ax2_y_min, ax2_y_max))
        self.ax1.set_xlim((i - 99, i + 0.49))
        self.ax2.set_xlim((i - 99, i + 0.49))

        self.fig.show()
        """

    def money_trace(self):
        print('==============正在绘制资金曲线图==============')
        account = self.account
        account = pd.DataFrame(account)
        fig = plt.figure(figsize=(20, 10), dpi=80, facecolor=[199 / 255, 238 / 255, 206 / 255], edgecolor='g')
        fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.15)
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor([199 / 255, 238 / 255, 206 / 255])
        # 设置xticklable
        money = account['期末']
        t = account['时间']
        min_ticks = math.floor(len(money) / 30)
        ax.set_xlabel('time')
        ax.set_ylabel('money')

        xtick = []
        for i in range(0, len(money), min_ticks):
            xtick.append(i)
        ax.set_xticks(xtick)
        xlable = []
        for i in xtick:
            xlable.append(str(t[i]))
        ax.set_xticklabels(xlable, rotation=90)
        ext = math.floor(0.01 * len(money))
        ax.set_xlim((0 - ext, len(money) + ext))
        ax.set_title(self.strategyname + ' account_change')
        ax.plot(money, 'k--')
        """
        ylimfix = ax.get_ylim()
        ax.set_ylim(ylimfix)
        """
        filename = 'F:\BackTest\BackTest_Fig\\'
        filename = filename + self.strategyname + '.png'
        plt.savefig(filename)
        plt.close()
        # plt.show()

    def trade_show(self):
        print('==============正在绘制交易盈亏图==============')
        trade = self.trade
        trade = pd.DataFrame(trade)
        fig = plt.figure(figsize=(20, 10), dpi=80, facecolor=[199 / 255, 238 / 255, 206 / 255], edgecolor='g')
        fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.15)
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor([199 / 255, 238 / 255, 206 / 255])
        # 设置xticklable
        trade_bar = trade['平仓盈亏']
        t = trade['开仓时间']
        min_ticks = 1
        ax.set_xlabel('open_time')
        ax.set_ylabel('trade_bar')

        xtick = []
        for i in range(0, len(trade_bar), min_ticks):
            xtick.append(i)
        ax.set_xticks(xtick)
        xlable = []
        for i in xtick:
            xlable.append(str(t[i]))
        ax.set_xticklabels(xlable, rotation=90)
        ext = 1
        ax.set_xlim((0 - ext, len(trade_bar) + ext))
        ax.set_title(self.strategyname + ' trade_bar')

        for i in range(0, len(trade_bar)):
            if trade_bar[i] > 0:
                ax.bar(i, trade_bar[i], facecolor='r')
            elif trade_bar[i] < 0:
                ax.bar(i, trade_bar[i], facecolor='g')

        """
        ylimfix = ax.get_ylim()
        ax.set_ylim(ylimfix)
        """
        filename = 'F:\BackTest\BackTest_Fig\\'
        filename = filename + 'trade_' + self.strategyname + '.png'
        plt.savefig(filename)
        plt.close()

    def trade_analysis(self):
        trade = self.trade
        trade = pd.DataFrame(trade)
        marketdata = self.marketdata
        marketdata = pd.DataFrame(marketdata)
        record = []
        columns_name = ['第几次交易','方向','开仓时间','开仓价格','平仓时间',
                        '平仓价格','持续时间','期间最高价','期间最低价','最终收益']
        for i in range(0,trade.shape[0]):
            trade_unit = trade.iloc[i]
            if trade_unit['开仓操作'] == '买开':
                buysell = 1
            elif trade_unit['开仓操作'] == '卖开':
                buysell = -1
            open_num = marketdata.loc[(marketdata['时间'] == trade_unit['开仓时间'])]
            clos_num = marketdata.loc[(marketdata['时间'] == trade_unit['平仓时间'])]
            market_unit = marketdata.loc[(marketdata['时间'] >= trade_unit['开仓时间']) &
                                         (marketdata['时间'] <= trade_unit['平仓时间'])]
            max_during = max(market_unit['最高'])
            min_during = min(market_unit['最低'])
            record.append([i, buysell, trade_unit['开仓时间'],
                           trade_unit['开仓价'],trade_unit['平仓时间'],
                           trade_unit['平仓价'],clos_num.index[0] - open_num.index[0] + 1,
                           max_during, min_during, trade_unit['平仓盈亏']]
                          )
        record = pd.DataFrame(record, columns=columns_name)
        filename = r'F:\BackTest\BackTest_Excel\trade_analysis.xlsx'
        writer = pd.ExcelWriter(filename, engine='openpyxl')
        if os.path.exists(filename) != True:
            record.to_excel(excel_writer=writer, sheet_name=self.strategyname)
        else:
            book = load_workbook(writer.path)
            writer.book = book
            record.to_excel(excel_writer=writer, sheet_name=self.strategyname)
        writer.save()
        writer.close()

    def analysis(self):
        # 起始时间
        time_start = self.marketdata['时间'][0]
        time_end = self.marketdata['时间'][len(self.marketdata['时间'])-1]
        # 年化盈利
        money_init = self.account['期初'][0]
        money = list(self.account['期末'].values())
        pl_year = (money[-1] - money_init)/ (len(money)/250)
        # 年化盈利率
        pl_year_ratio = (money[-1]/money_init)**(250/len(money)) - 1
        # 计算夏普比率
        dataDiff = np.diff(np.append(money_init, money))
        sharp_ratio = (np.mean(dataDiff) * 250 - 0.03) / (np.std(dataDiff) * np.sqrt(250))
        # 最大回撤
        maxdraw = 0
        for i in range(len(money)):
            highest = np.max(money[:i + 1])
            draw = (highest - money[i]) / highest
            if draw > maxdraw:
                maxdraw = draw
        # 胜率

        data = self.trade['净盈亏']
        win_times = 0
        for i in range(0, len(data)):
            if data[i] > 0:
                win_times += 1
        win_rate = win_times/len(data)
        # 平均盈利
        win_times = 0
        win_money = 0
        for i in range(0, len(data)):
            if data[i] > 0:
                win_times += 1
                win_money += data[i]
        ave_profit = win_money/win_times
        # 平均亏损
        loss_times = 0
        loss_money = 0
        for i in range(0, len(data)):
            if data[i] < 0:
                loss_times += 1
                loss_money += data[i]
        ave_loss = loss_money / loss_times
        # 策略盈亏比：平均盈利 / 平均亏损
        profit_to_margin = abs(ave_profit/ave_loss)

        statistic_dict = {'起始时间':time_start,
                          '终止时间':time_end,
                          '策略名称':self.strategyname,
                          '年化盈利':round(pl_year),
                          '年化盈利率':round(pl_year_ratio*100)/100,
                          '夏普比率':round(sharp_ratio*100)/100,
                          '最大回撤':round(maxdraw*10000)/10000,
                          '胜率':round(win_rate*10000)/10000,
                          '平均盈利':round(ave_profit),
                          '平均亏损':round(ave_loss),
                          '策略盈亏比':round(profit_to_margin*100)/100
                          }

        statistic_dict = pd.DataFrame(statistic_dict, index=['策略统计结果'])
        #statistic_dict = [self.strategyname, pl_year, pl_year_ratio, sharp_ratio, maxdraw,win_rate, ave_profit, ave_loss, profit_to_margin]

        statistic_dict = pd.DataFrame(statistic_dict)
        filename = 'F:\BackTest\BackTest_Excel\statistic.csv'
        # xlswriter = pd.ExcelWriter(filename)
        # statistic_dict.to_csv()

        statistic_dict.to_csv(filename, mode='a', header=0, encoding='gb2312')
        # xlswriter.save()
        print('===================' + self.strategyname + ' Done!!!======================')




if __name__ == '__main__':
    strategy_list = [[20, 25, 30, 35, 40, 45, 50, 55, 60],
                     [6, 8, 10, 12, 14, 16]]
    strategy_list = [[40],
                     [10]]
    spe_list = ['m', 'rb', 'v', 'ru', 'cu', 'j', 'cf']
    trade_accord = []
    for i in range(0, len(spe_list)):
        # 数据参数部分
        spe = spe_list[i]

        # 策略部分准备
        for slow in strategy_list[0]:
            for fast in strategy_list[1]:
                # 只分析短期参数为10的情况
                if fast == 10:
                    # 回测参数
                    strategy_name = 'ema_' + spe + '_' + str(slow) + '_' + str(fast)
                    self = BackTestAnalysis(strategy_name)
                    self.backtest_main()
                    self.trade_analysis()
                    print(strategy_name + " Done!!!")
    pass
    # fig, ax = self.KLine()
    # self.money_trace()