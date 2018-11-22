# -*- coding: utf-8 -*-
# author:@Jack.Wang


"""
开发基于MACD的策略，
新的数据，要记录下来
macd的各项值要记录下来
对macd的分析要记录下来

"""
import scipy.io as sio
import pandas as pd
import copy


class MACD_JW:
    def __init__(self, ema_fast=12, ema_slow=26, dea_num=9):
        self.ema_fast_para = ema_fast
        self.ema_slow_para = ema_slow
        self.dea_para = dea_num
        self.data = [] # 数据是一个字典，包括时间list，开高收低list
        self.num = [] # 数据数目
        self.ema_fast = []
        self.ema_slow = []
        self.dif = []
        self.dea = []
        self.macd_pillar = []

        # 接下来为需要分析的数据
        self.rise_fall = [] # 记录当前涨跌
        self.gold_dead = [] # 记录金叉死叉
        self.red_pile_record = [] # 记录当前是属于第几堆红柱，以及红柱堆整体情况
        self.green_pile_record = [] # 记录当前是属于第几堆绿柱，以及绿柱堆整体情况
        self.pile = [] # 每个数据，对应的堆的记录以及更新


    def macd_main(self, data):
        # 收到新的数据，先添加到data里面去
        self.data.append([data.time, data.open, data.high, data.low, data.close])
        # 计算数据num
        self.data_num()
        # 计算快速ema值
        self.ema_fast_loop()
        # 计算慢速ema值
        self.ema_slow_loop()
        # 计算快慢线diff值
        self.dif_loop()
        # 计算dea值
        self.dea_loop()
        # 计算macd柱子的值
        self.macd_pillar_loop()
        # 涨势跌势
        self.rise_fall_cal()
        # 金叉死叉
        self.gold_dead_cal()
        # 堆的记录
        self.pile_cal()

    def data_num(self):
        if len(self.num) == 0:
            self.num.append(0)
        else:
            num = self.num[-1] + 1
            self.num.append(num)


    def ema_fast_loop(self):
        new_data = self.data[-1][-1]
        ema_fast_para = self.ema_fast_para  # 12
        if len(self.ema_fast) == 0:
            self.ema_fast.append(new_data)
        else:
            new_ema = self.ema_fast[-1]*(ema_fast_para - 1)/(ema_fast_para + 1) + \
                      2/(ema_fast_para + 1)*new_data
            self.ema_fast.append(new_ema)

    def ema_slow_loop(self):
        new_data = self.data[-1][-1]
        ema_slow_para = self.ema_slow_para  # 26
        if len(self.ema_slow) == 0:
            self.ema_slow.append(new_data)
        else:
            new_ema = self.ema_slow[-1]*(ema_slow_para - 1)/(ema_slow_para + 1) + \
                      2/(ema_slow_para + 1)*new_data
            self.ema_slow.append(new_ema)

    def dif_loop(self):
        new_diff = self.ema_fast[-1] - self.ema_slow[-1]
        self.dif.append(new_diff)

    def dea_loop(self):
        dea_num = self.dea_para

        if len(self.dea) == 0:
            self.dea.append(self.dif[-1])
        else:
            new_dea = self.dea[-1]*(dea_num - 1)/(dea_num + 1) + \
                      self.dif[-1]*2/(dea_num + 1)
            self.dea.append(new_dea)

    def macd_pillar_loop(self):
        self.macd_pillar.append(2*(self.dif[-1] - self.dea[-1]))

    def list_average(self, lis):
        n = len(lis)
        s = 0
        for li in lis:
            s += li
        ave = s/n
        return ave

    def rise_fall_cal(self):
        if self.dea[-1] > 0:
            self.rise_fall.append('rise')
        elif self.dea[-1] == 0:
            self.rise_fall.append('zero')
        elif self.dea[-1] < 0:
            self.rise_fall.append('fall')

    def gold_dead_cal(self):
        # 第一根
        if len(self.macd_pillar) == 1:
            self.gold_dead.append(None)
        else:
            last = self.macd_pillar[-2]
            this = self.macd_pillar[-1]
            if last == 0 and this > 0:
                self.gold_dead.append('gold')
            elif last == 0 and this < 0:
                self.gold_dead.append('dead')
            elif last > 0 and this > 0:
                self.gold_dead.append('rise')
            elif last > 0 and this < 0:
                self.gold_dead.append('dead')
            elif last < 0 and this < 0:
                self.gold_dead.append('fall')
            elif last < 0 and this > 0:
                self.gold_dead.append('gold')

    def pile_cal(self):
        # 更新红绿堆数据，以及堆数据
        # 首次数据记录
        dic = {}
        dic['data'] = []
        dic['data_num'] = []
        dic['ema_fast'] = []
        dic['ema_slow'] = []
        dic['dif'] = []
        dic['dea'] = []
        dic['macd_pillar'] = []

        dic['pillar_color'] = [] # 柱子的颜色
        dic['data_ave'] = [] # 数据的平均值
        dic['datanum_len'] = [] # 数据时间的跨度，几根K线
        dic['macd_ave'] = [] # macd的均值
        dic['diff_ave'] = [] # dif的均值
        dic['dea_ave'] = [] # dea的均值
        # 其中diff创新高或新低，而macd_pillar不创新高或新低，则代表一种背离

        data = self.data[-1][-1]
        data_num = self.num[-1]
        ema_fast = self.ema_fast[-1]
        ema_slow = self.ema_slow[-1]
        dif = self.dif[-1]
        dea = self.dea[-1]
        macd_pillar = self.macd_pillar[-1]
        red_record = self.red_pile_record
        green_record = self.green_pile_record

        # 如果是本次第一次加入，则macd首个柱子值为0，启用这个
        if macd_pillar == 0 and len(red_record) == 0 and len(green_record) == 0:
            self.pile.append(dic)
        # 如果现在是红柱子
        if macd_pillar > 0:
            # 首次记录，没有[-1]的概念
           if len(red_record) == 0:
               # 先记录数据
               dic['data'].append(data)
               dic['data_num'].append(data_num)
               dic['ema_fast'].append(ema_fast)
               dic['ema_slow'].append(ema_slow)
               dic['dif'].append(dif)
               dic['dea'].append(dea)
               dic['macd_pillar'].append(macd_pillar)

               dic['pillar_color'].append('red')  # 柱子的颜色
               dic['data_ave'].append(self.list_average(dic['data']))  # 数据的平均值
               dic['datanum_len'].append(len(dic['data_num']))  # 数据时间的跨度，几根K线
               dic['macd_ave'].append(self.list_average(dic['macd_pillar']))  # macd的均值
               dic['diff_ave'].append(self.list_average(dic['dif']))  # dif的均值
               dic['dea_ave'].append(self.list_average(dic['dea']))  # dea的均值

               self.red_pile_record.append(dic)
               self.pile.append(dic)
           # 非首次记录
           else:
               # 接着上个来
               if self.macd_pillar[-2] > 0:
                   dic = copy.deepcopy(red_record[-1])

                   dic['data'].append(data)
                   dic['data_num'].append(data_num)
                   dic['ema_fast'].append(ema_fast)
                   dic['ema_slow'].append(ema_slow)
                   dic['dif'].append(dif)
                   dic['dea'].append(dea)
                   dic['macd_pillar'].append(macd_pillar)

                   dic['pillar_color'].append('red')  # 柱子的颜色
                   dic['data_ave'].append(self.list_average(dic['data']))  # 数据的平均值
                   dic['datanum_len'].append(len(dic['data_num']))  # 数据时间的跨度，几根K线
                   dic['macd_ave'].append(self.list_average(dic['macd_pillar']))  # macd的均值
                   dic['diff_ave'].append(self.list_average(dic['dif']))  # dif的均值
                   dic['dea_ave'].append(self.list_average(dic['dea']))  # dea的均值

                   self.red_pile_record[-1] = dic
                   self.pile.append(dic)
               # 如果改变颜色，那么开启新的一个记录
               elif self.macd_pillar[-2] <= 0:
                   dic['data'].append(data)
                   dic['data_num'].append(data_num)
                   dic['ema_fast'].append(ema_fast)
                   dic['ema_slow'].append(ema_slow)
                   dic['dif'].append(dif)
                   dic['dea'].append(dea)
                   dic['macd_pillar'].append(macd_pillar)

                   dic['pillar_color'].append('red')  # 柱子的颜色
                   dic['data_ave'].append(self.list_average(dic['data']))  # 数据的平均值
                   dic['datanum_len'].append(len(dic['data_num']))  # 数据时间的跨度，几根K线
                   dic['macd_ave'].append(self.list_average(dic['macd_pillar']))  # macd的均值
                   dic['diff_ave'].append(self.list_average(dic['dif']))  # dif的均值
                   dic['dea_ave'].append(self.list_average(dic['dea']))  # dea的均值

                   self.red_pile_record.append(dic)
                   self.pile.append(dic)

        if self.macd_pillar[-1] < 0:
            # 首次记录，没有【-1】的概念
            if len(green_record) == 0:
                # 先记录数据
                dic['data'].append(data)
                dic['data_num'].append(data_num)
                dic['ema_fast'].append(ema_fast)
                dic['ema_slow'].append(ema_slow)
                dic['dif'].append(dif)
                dic['dea'].append(dea)
                dic['macd_pillar'].append(macd_pillar)

                dic['pillar_color'].append('green')  # 柱子的颜色
                dic['data_ave'].append(self.list_average(dic['data']))  # 数据的平均值
                dic['datanum_len'].append(len(dic['data_num']))  # 数据时间的跨度，几根K线
                dic['macd_ave'].append(self.list_average(dic['macd_pillar']))  # macd的均值
                dic['diff_ave'].append(self.list_average(dic['dif']))  # dif的均值
                dic['dea_ave'].append(self.list_average(dic['dea']))  # dea的均值

                self.green_pile_record.append(dic)
                self.pile.append(dic)
            # 非首次记录
            else:
                # 继续记录
                if self.macd_pillar[-2] < 0:
                    dic = copy.deepcopy(green_record[-1])

                    dic['data'].append(data)
                    dic['data_num'].append(data_num)
                    dic['ema_fast'].append(ema_fast)
                    dic['ema_slow'].append(ema_slow)
                    dic['dif'].append(dif)
                    dic['dea'].append(dea)
                    dic['macd_pillar'].append(macd_pillar)

                    dic['pillar_color'].append('green')  # 柱子的颜色
                    dic['data_ave'].append(self.list_average(dic['data']))  # 数据的平均值
                    dic['datanum_len'].append(len(dic['data_num']))  # 数据时间的跨度，几根K线
                    dic['macd_ave'].append(self.list_average(dic['macd_pillar']))  # macd的均值
                    dic['diff_ave'].append(self.list_average(dic['dif']))  # dif的均值
                    dic['dea_ave'].append(self.list_average(dic['dea']))  # dea的均值

                    self.green_pile_record[-1] = dic
                    self.pile.append(dic)
                # 新的记录
                else:
                    dic['data'].append(data)
                    dic['data_num'].append(data_num)
                    dic['ema_fast'].append(ema_fast)
                    dic['ema_slow'].append(ema_slow)
                    dic['dif'].append(dif)
                    dic['dea'].append(dea)
                    dic['macd_pillar'].append(macd_pillar)

                    dic['pillar_color'].append('green')  # 柱子的颜色
                    dic['data_ave'].append(self.list_average(dic['data']))  # 数据的平均值
                    dic['datanum_len'].append(len(dic['data_num']))  # 数据时间的跨度，几根K线
                    dic['macd_ave'].append(self.list_average(dic['macd_pillar']))  # macd的均值
                    dic['diff_ave'].append(self.list_average(dic['dif']))  # dif的均值
                    dic['dea_ave'].append(self.list_average(dic['dea']))  # dea的均值

                    self.green_pile_record.append(dic)
                    self.pile.append(dic)


if __name__=='__main__':
    data_file = r"F:\Quant\Data\Futures_KLine\Day\J201901.mat"
    matdata = sio.loadmat(data_file)
    df = []
    time_raw = matdata['time_str']
    data_raw = matdata['data']
    for i in range(0, len(time_raw)):
        df.append([time_raw[i][0][0], data_raw[i][0], data_raw[i][1], data_raw[i][2], data_raw[i][3]])
    data = pd.DataFrame(df, columns=['time', 'open', 'high', 'low', 'close'])
    self = MACD_JW()
    for d in range(0,len(data)):
        self.macd_main(data.iloc[d])

    print('Done')












