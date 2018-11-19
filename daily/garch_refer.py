# -*- coding: utf-8 -*-
# author: WangYun 
# time :2018/10/15


import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import *
import scipy.io as sio
import os
import math
import arch
import datetime



class garch_refer:
    def __init__(self):
        # 初始化，保存当前日期
        nowdate = datetime.datetime.now()
        nowdate = datetime.datetime.strftime(nowdate, '%Y-%m-%d')
        self.nowdate = nowdate

    def garch_futures_list(self):
        # 要进行统计的数据
        li=['商品指数','贵金属指数','有色指数','焦煤钢矿指数','非金属建材指数',
            '能源指数','化工指数','谷物指数','油脂油料指数','软商指数','农副产品指数',

            '沪金指数','沪银指数','沪铜指数','沪铝指数','沪锌指数',
            '沪铅指数','沪镍指数','沪锡指数',

            '沪胶指数','甲醇指数','塑料指数','沥青指数','PP指数','PVC指数','TA指数',

            '动煤指数','焦煤指数','焦炭指数','铁矿指数','螺纹指数','热卷指数','玻璃指数',

            '连豆指数','豆二指数','豆油指数','菜油指数','棕榈指数','豆粕指数','菜粕指数',
            '玉米指数','淀粉指数',

            '郑棉指数','郑糖指数','鸡蛋指数',

            '苹果指数','原油指数','燃油指数']

        return li

    def garch_stockindex_list(self):
        # 要进行统计的数据
        li=['sh000001_D', 'sz399006_D']

        return li

    def garch_futures_data_get(self, name):
        # 数据的读取
        data_file = r"E:\Matlab\toolbox\量化\Quant\GetDataAndSave\Basis\Data\Price"
        file_name = os.path.join(data_file, name + ".mat")
        matdata = sio.loadmat(file_name)
        df = []
        time_raw = matdata['time_str']
        data_raw = matdata['data']
        for i in range(0, len(time_raw)):
            df.append([time_raw[i][0][0], data_raw[i][0], data_raw[i][1], data_raw[i][2], data_raw[i][3]])
        data = pd.DataFrame(df, columns=['time', 'open', 'high', 'low', 'close'])
        data = data.set_index('time', drop=True)
        if len(data) > 1000:
            data = data[-1000:]
        return data

    def garch_stockindex_data_get(self, name):
        # 数据的读取
        data_file = r"F:\Quant\Data\StockIndex_KLine\Day_Index_mat"
        file_name = os.path.join(data_file, name + ".mat")
        matdata = sio.loadmat(file_name)
        df = []
        time_raw = matdata['time_str']
        data_raw = matdata['data']
        for i in range(0, len(time_raw)):
            df.append([time_raw[i][0][0], data_raw[i][0], data_raw[i][1], data_raw[i][2], data_raw[i][3]])
        data = pd.DataFrame(df, columns=['time', 'open', 'high', 'low', 'close'])
        data = data.set_index('time', drop=True)
        if len(data) > 1000:
            data = data[-1000:]
        return data

    def garch_figure(self, data, titlename):
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

        df = data['close']
        rate_log = np.log(df / df.shift(1))
        rate_log = rate_log.dropna()

        model3 = arch.arch_model(rate_log, mean='Constant', vol='GARCH')
        res = model3.fit()
        garch_data = res.conditional_volatility

        xtick = ax.get_xticks()
        xlabel = ax.get_xticklabels()
        ax2 = ax.twinx()
        ax2.plot(garch_data)

        ax.set_xticks(xtick)
        ax.set_xticklabels(xlabel)
        ax.set_title(titlename)
        """
        rate = res.conditional_volatility
        rate_right = rate[rate > rate.quantile(0.95)]
        for i in range(0, len(rate_right)):
            x = rate[rate.index == rate_right.index[i]]
            x[0] = ax.get_ylim()[0] * 1.05
            ax.plot(x, color='red', marker='*')
            x[0] = df[x.index[0]]
            ax.plot(x, color='red', marker='*')
        rate_left = rate[rate < rate.quantile(0.05)]
        for i in range(0, len(rate_left)):
            x = rate[rate.index == rate_left.index[i]]
            x[0] = ax.get_ylim()[0] * 1.03
            ax.plot(x, color='green', marker='^')
            x[0] = df[x.index[0]]
            ax.plot(x, color='green', marker='^')
        """

        return fig, ax


    def garch_futures_main(self):
        file_name = r'F:\daily_work'
        filename = os.path.join(file_name, self.nowdate)

        if not os.path.exists(filename):
            os.mkdir(filename)

        # 期货的garch监控
        li_ = self.garch_futures_list()

        for li in li_:
            data = self.garch_futures_data_get(li)
            date = self.nowdate
            titlename = li + '  ' + date
            fig, ax = self.garch_figure(data, titlename)
            png_name = os.path.join(filename, 'garch_' + titlename + '.png')
            plt.savefig(png_name)
            plt.close()
            nowdate = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
            print(titlename + " is done: @ " + nowdate)

    def garch_stockindex_main(self):
        # 上证指数的garch监控
        file_name = r'F:\daily_work'
        filename = os.path.join(file_name, self.nowdate)

        if not os.path.exists(filename):
            os.mkdir(filename)
        li_ = self.garch_stockindex_list()
        for li in li_:
            data = self.garch_stockindex_data_get(li)
            date = self.nowdate
            titlename = li + '  ' + date
            fig, ax = self.garch_figure(data, titlename)
            png_name = os.path.join(filename, 'garch_' + titlename + '.png')
            plt.savefig(png_name)
            plt.close()
        nowdate = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        print("stockindex is done: @ " + nowdate)


def main():
    garch = garch_refer()
    garch.garch_stockindex_main()
    # garch.garch_futures_main()


if __name__ == '__main__':
    main()