# -*- coding: utf-8 -*-
# author: WangYun 


from scipy import io as spio
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

a = np.ones((3,3))
generated = stats.norm.rvs(size=900)
# 拟合正太分布
mean,std = stats.norm.fit(generated)
# 峰度
stats.skewtest(generated)
# 偏度
stats.kurtosistest(generated)
# 服从正态分布的概率
stats.normaltest(generated)
# 百分位数
stats.scoreatpercentile(generated,50)
plt.hist(generated)
# 均值检验，检验两组不同的样本是否有想通的均值，返回值有两个
gen1 = np.random.normal(size=300)
gen2 = np.random.normal(size=300)
stats.ttest_ind(gen1, gen2)
# Kolmogorov-Smirnov检验两组样本同分布的可能性
stats.ks_2samp(gen1, gen2)
# 运用Jarque-Bera正态性检验
stats.jarque_bera(gen1-gen2)[-1]


def main():
    pass


if __name__ == '__main__':
    main()