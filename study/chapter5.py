# -*- coding: utf-8 -*-
# author: WangYun 
# time :2018/10/1 

import os
import pandas as pd
from sklearn.feature_selection import VarianceThreshold
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2



def main():
    data_folder = r"E:\Python"
    data_folder = os.path.join(data_folder, "adult.data")
    adult = pd.read_csv(data_folder, header=None,
                        names=["Age", "Work-Class", "fnlwgt",
                               "Education", "Education-Num",
                               "Marital-Status", "Occupation",
                               "Relationship", "Race", "Sex",
                               "Capital-gain", "Capital-loss",
                               "Hours-per-week", "Native-Country",
                               "Earning-Raw"])
    adult.drop_duplicates()
    adult.dropna(how='all', inplace=True)
    print(adult["Hours-per-week"].describe())
    print(adult["Education-Num"].median())
    # value_counts统计为某项值的数据个数
    print(adult["Education-Num"].value_counts()[16])
    print(adult["Work-Class"].unique())
    adult["LongHours"] = adult["Hours-per-week"] > 40
    print(adult["LongHours"][:5].astype(int))
    #==========================特征选择===============================
    x = np.arange(30).reshape((10,3))
    x[:,1] = 1
    vt = VarianceThreshold(threshold=2)
    xt = vt.fit_transform(x)
    print(vt.variances_)
    #================选择最优的特征=====================================
    x = adult[['Age','Education-Num','Capital-gain','Capital-loss','Hours-per-week']].values
    adult['Earning-Raw'] = adult['Earning-Raw'] == '>50K'
    adult['Earning-Raw'] = adult['Earning-Raw'].astype(int)
    y = adult['Earning-Raw'].values
    #================使用转换器 卡方函数打分
    transformer = SelectKBest(score_func=chi2, k=3)
    xt_chi2 = transformer.fit(x,y)
    print(transformer.scores_)
    pass

if __name__ == '__main__':
    main()