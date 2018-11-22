# -*- coding: utf-8 -*-
# author: WangYun 


import numpy as np
import scipy.io as sio
import pandas as pd

class strategy_ma:
    def __init__(self, fast_index, slow_index):
        self.fast_index = fast_index
        self.slow_index = slow_index
        self.fast_ma = [] # 快速线
        self.slow_ma = [] # 慢速线
        self.data = [] # 数据记录

    def ma_calculate(self, data):
        self.data.append(data)
        # 计算快速线
        if len(self.fast_ma) < self.fast_index:
            mean = np.mean(self.data)
            self.fast_ma.append(mean)
        if len(self.fast_ma) >= self.fast_index:
            mean = np.mean(self.data[-self.fast_index-1:len(self.data)])
            self.fast_ma.append(mean)
        # 计算慢速线
        if len(self.slow_ma) < self.slow_index:
            mean = np.mean(self.data)
            self.slow_ma.append(mean)
        if len(self.slow_ma) >= self.slow_index:
            mean = np.mean(self.data[-self.slow_index-1:len(self.data)])
            self.slow_ma.append(mean)

        pass

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
    self = strategy_ma(fast_index=5, slow_index=20)
    for d in data:
        self.ma_calculate(d)

    print('Done')


if __name__ == '__main__':
    main()