# -*- coding: utf-8 -*-
# author: WangYun 
# time :2018/9/21

import numpy as np
import scipy.io as sio
import pandas as pd

class strategy_ema:
    def __init__(self, fast_index, slow_index):
        self.fast_index = fast_index
        self.slow_index = slow_index
        self.fast_ema = [] # 快速线
        self.slow_ema = [] # 慢速线
        self.data = [] # 数据记录

    def ma_calculate(self, data):
        self.data.append(data)
        self.ema_cal()

    def ema_cal(self):
        # 计算快速线
        if len(self.fast_ema) < self.fast_index:
            mean = np.mean(self.data)
            self.fast_ema.append(mean)
        if len(self.fast_ema) >= self.fast_index:
            ema = (self.data[-1]*2 + self.fast_ema[-1]*(self.fast_index - 2))/self.fast_index
            self.fast_ema.append(ema)
        # 计算慢速线
        if len(self.slow_ema) < self.slow_index:
            mean = np.mean(self.data)
            self.slow_ema.append(mean)
        if len(self.slow_ema) >= self.slow_index:
            ema = (self.data[-1]*2 + self.slow_ema[-1]*(self.slow_index - 2)) / self.slow_index
            self.slow_ema.append(ema)


def main():
    file_name = "F:\Quant\Data\Futures_KLine\Day\J201809.mat"
    d = sio.loadmat(file_name)
    time = d['time_str']
    data = d['data']
    time_list = []
    for t in time:
        time_list.append(t[0][0])
    time = pd.DataFrame(time_list)
    data = pd.DataFrame(data, columns=['o', 'h', 'l', 'c'])
    data = pd.DataFrame(data.iloc[:, 3])
    data_list = []
    for i in range(0, len(data)):
        data_list.append(data.loc[i][0])
    data = data_list
    self = strategy_ema(fast_index=5, slow_index=20)
    for d in data:
        self.ma_calculate(d)

    print('Done')


if __name__ == '__main__':
    main()