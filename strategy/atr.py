# -*- coding: utf-8 -*-
# author:@Jack.Wang
# time :2018/9/12 22:32
import pandas as pd
import scipy.io as sio
import numpy as np


class atr_event:
    def __init__(self, atr_num=20):
        self.atr_para = atr_num
        self.data = []  # 数据是一个字典，包括时间list，开高收低list
        self.num = []  # 数据数目
        self.wave = [] # 最大波幅
        self.atr = []

    def data_num(self):
        if len(self.num) == 0:
            self.num.append(0)
        else:
            num = self.num[-1] + 1
            self.num.append(num)

    def atr_cal(self):
        length = len(self.data)
        if length == 1:
            wave = self.data[-1][2] - self.data[-1][3]
            self.wave.append(wave)
            self.atr.append(wave)
        else:
            num1 = abs(self.data[-1][2] - self.data[-1][3])  # 当日最高价-最低价
            num2 = abs(self.data[-1][2] - self.data[-2][4])  # 当日最高价-昨日收盘价
            num3 = abs(self.data[-1][3] - self.data[-2][4])  # 当日最低价-昨日收盘价
            wave = max(num1, num2, num3)

            self.wave.append(wave)
            if length <= self.atr_para:
                self.atr.append(np.mean(self.wave))
            elif length > self.atr_para:
                self.atr.append(np.mean(self.wave[-length-1:-1]))

    def atr_main(self, data):
        # 收到新的数据，先添加到data里面去
        self.data.append([data.time, data.open, data.high, data.low, data.close])
        # 计算数据num
        self.data_num()
        # 计算atr
        self.atr_cal()


def main():
    data_file = r"F:\Quant\Data\Futures_KLine\Day\J201901.mat"
    matdata = sio.loadmat(data_file)
    df = []
    time_raw = matdata['time_str']
    data_raw = matdata['data']
    for i in range(0, len(time_raw)):
        df.append([time_raw[i][0][0], data_raw[i][0], data_raw[i][1], data_raw[i][2], data_raw[i][3]])
    data = pd.DataFrame(df, columns=['time', 'open', 'high', 'low', 'close'])
    self = atr_event()
    for d in range(0, len(data)):
        self.atr_main(data.iloc[d])
    print('Done')


if __name__ == '__main__':
    main()