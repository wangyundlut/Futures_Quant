# -*- coding: utf-8 -*-
# author: WangYun 
# time :2018/10/12 

from statistics.statistics_data import statistics_data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import statsmodels.stats.anova as anova
from statsmodels.formula.api import ols
import statsmodels.api as sm
import ffn
from statsmodels.tsa import stattools
from statsmodels.graphics.tsaplots import *
from arch.unitroot import ADF
import math
import arch

class model_statistic:
    def __init__(self):
        class_data = statistics_data()
        data = class_data.data_test_m()
        data.set_index(['时间'], inplace=True)
        self.data = data
        df = self.data['收盘价']
        rate_simple = (df - df.shift(1)) / df.shift(1)
        rate_simple = rate_simple.dropna()
        self.rate_simple = rate_simple
        rate_log = np.log(df / df.shift(1))
        rate_log = rate_log.dropna()
        self.rate_log = rate_log

    def descriptive(self):
        df = self.data['收盘价']
        close = self.data['收盘价']

        fig = plt.figure(figsize=(20, 10), dpi=80, facecolor=[199 / 255, 238 / 255, 206 / 255], edgecolor='g')
        fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.15)
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor([199 / 255, 238 / 255, 206 / 255])
        min_ticks = math.floor(len(close) / 30)
        ax.set_xlabel('time')
        ax.set_ylabel('price')
        xtick = []
        for i in range(0, len(close), min_ticks):
            xtick.append(i)
        ax.set_xticks(xtick)
        xlable = []
        for i in xtick:
            xlable.append(str(df.index[i]))
        ax.set_xticklabels(xlable, rotation=90)
        ext = math.floor(0.01 * len(close))
        ax.set_xlim((0 - ext, len(close) + ext))

        roll_mean = close.rolling(window=10).mean()
        roll_std = close.rolling(window=10).std()
        ax.plot(close, color='blue', label='origin')
        ax.plot(roll_mean, color='red', label='ma10')
        ax.plot(roll_std * 20, color='black', label='std10*20')
        ax.legend(loc='best')
        ax.set_title('Mprice')
        plt.show()
        plt.close()

        # 描述性统计
        rate = self.rate_log
        mean = rate.mean()  # 算均值
        abs_mean = abs(rate).mean()  # 绝对值的均值
        data_var = rate.var()  # 求方差
        data_std = rate.std()  # 求标准差
        abs_std = abs(rate).std()  # 求绝对值的标准差
        median = rate.median()  # 算中位数
        mode = rate.mode()  # 计算众数
        rate.quantile(0.25)  # 计算1/4分位数
        rate.quantile(0.75)  # 计算3/4分位数
        rate.quantile(0.05)  # 计算小概率左尾
        rate.quantile(0.95)  # 计算小概率右尾
        rate.max()
        rate.min()
        data_range = rate.max() - rate.min()  # 求极差
        mad = rate.mad()  # 求平均绝对偏差

        skew = stats.skew(rate)  # 求峰度
        kurtosis = stats.kurtosis(rate)  # 求偏度
        print("==========数据收益率情况==========")
        print("Mean is: {0}".format(mean))
        print("Median is {0}".format(rate.median()))
        print("Std is: {0}".format(rate.std()))
        print("Quantile 25% is: {0}".format(rate.quantile(0.25)))
        print("Quantile 75% is: {0}".format(rate.quantile(0.75)))
        print("Quantile  5% is: {0}".format(rate.quantile(0.05)))
        print("Quantile 95% is: {0}".format(rate.quantile(0.95)))
        print("Minimum value is: {0}".format(rate.min()))
        print("Maximum value is: {0}".format(rate.max()))
        print("Skewness is: {0}".format(stats.skew(rate)))
        print("Kurtosis is: {0}".format(stats.kurtosis(rate)))

        plt.hist(rate, bins=30)  # 绘制直方图，分成十份儿
        s = np.random.normal(mean, data_std, 100000)
        density = stats.kde.gaussian_kde(rate)
        # 设定分割
        bins = np.arange(-0.06, 0.06, 0.00005)
        # 画图，概率密度分布
        plt.plot(bins, density(bins))
        plt.title('M lograte distribution')

    def little_propably(self):
        rate = self.rate_log
        close = self.data['收盘价']
        fig = plt.figure(figsize=(20, 10), dpi=80, facecolor=[199 / 255, 238 / 255, 206 / 255], edgecolor='g')
        fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.15)
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor([199 / 255, 238 / 255, 206 / 255])
        min_ticks = math.floor(len(close) / 30)
        ax.set_xlabel('time')
        ax.set_ylabel('price')
        xtick = []
        for i in range(0, len(close), min_ticks):
            xtick.append(i)
        ax.set_xticks(xtick)
        xlable = []
        for i in xtick:
            xlable.append(str(close.index[i]))
        ax.set_xticklabels(xlable, rotation=90)
        ext = math.floor(0.01 * len(close))
        ax.set_xlim((0 - ext, len(close) + ext))
        ax.plot(close, color='blue', label='origin')
        # 画收盘线，然后画收益率小概率尾部事件发生的位置
        ax.plot(close)
        # plt.show()
        """
        rate_right = rate[(rate > rate.quantile(0.95)) | (rate < rate.quantile(0.05))]
        for i in range(0, len(rate_right)):
            x = rate[rate.index == rate_right.index[i]]
            x[0] = ax.get_ylim()[0]*1.05
            ax.plot(x, color='red', marker='*')
            x[0] = close[x.index[0]]
            ax.plot(x, color='red', marker='*')
        """
        rate_right = rate[rate>rate.quantile(0.95)]
        for i in range(0, len(rate_right)):
            x = rate[rate.index == rate_right.index[i]]
            x[0] = ax.get_ylim()[0]*1.05
            ax.plot(x, color='red', marker='*')
            x[0] = close[x.index[0]]
            ax.plot(x, color='red', marker='*')
        rate_left = rate[rate < rate.quantile(0.05)]
        for i in range(0, len(rate_left)):
            x = rate[rate.index == rate_left.index[i]]
            x[0] = ax.get_ylim()[0]*1.03
            ax.plot(x, color='green', marker='^')
            x[0] = close[x.index[0]]
            ax.plot(x, color='green', marker='^')
        # plt.show()
        plt.title('M rate tail distribution')
        plt.close()

        fig = plt.figure(figsize=(20, 10), dpi=80, facecolor=[199 / 255, 238 / 255, 206 / 255], edgecolor='g')
        fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.15)
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor([199 / 255, 238 / 255, 206 / 255])
        min_ticks = math.floor(len(close) / 30)
        ax.set_xlabel('time')
        ax.set_ylabel('price')
        xtick = []
        for i in range(0, len(close), min_ticks):
            xtick.append(i)
        ax.set_xticks(xtick)
        xlable = []
        for i in xtick:
            xlable.append(str(close.index[i]))
        ax.set_xticklabels(xlable, rotation=90)
        ext = math.floor(0.01 * len(close))
        ax.set_xlim((0 - ext, len(close) + ext))
        ax.plot(close, color='blue', label='origin')
        # 画收盘线，然后画收益率小概率尾部事件发生的位置
        ax.plot(close)
        # plt.show()
        rate_right = rate[(rate > rate.quantile(0.35)) & (rate < rate.quantile(0.65))]
        for i in range(0, len(rate_right)):
            x = rate[rate.index == rate_right.index[i]]
            x[0] = ax.get_ylim()[0] * 1.05
            ax.plot(x, color='red', marker='*')
            x[0] = close[x.index[0]]
            ax.plot(x, color='red', marker='*')

        rate_right = rate[(rate>rate.quantile(0.5))&(rate<rate.quantile(0.55))]
        for i in range(0, len(rate_right)):
            x = rate[rate.index == rate_right.index[i]]
            x[0] = ax.get_ylim()[0] * 1.05
            ax.plot(x, color='red', marker='*')
            x[0] = close[x.index[0]]
            ax.plot(x, color='red', marker='*')
        rate_left = rate[(rate>rate.quantile(0.45))&(rate<rate.quantile(0.5))]
        for i in range(0, len(rate_left)):
            x = rate[rate.index == rate_left.index[i]]
            x[0] = ax.get_ylim()[0] * 1.03
            ax.plot(x, color='green', marker='^')
            x[0] = close[x.index[0]]
            ax.plot(x, color='green', marker='^')
        plt.show()
        plt.title('M rate 0.35~0.65 distribution')
        plt.close()

        pass


    def series(self):
        rate = self.rate_log

        fig = plt.figure(figsize=(20, 10), dpi=80, facecolor=[199 / 255, 238 / 255, 206 / 255], edgecolor='g')
        fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.15)
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor([199 / 255, 238 / 255, 206 / 255])
        min_ticks = math.floor(len(rate) / 30)
        ax.set_xlabel('time')
        ax.set_ylabel('price')
        xtick = []
        for i in range(0, len(rate), min_ticks):
            xtick.append(i)
        ax.set_xticks(xtick)
        xlable = []
        for i in xtick:
            xlable.append(str(rate.index[i]))
        ax.set_xticklabels(xlable, rotation=90)
        ext = math.floor(0.01 * len(rate))
        ax.set_xlim((0 - ext, len(rate) + ext))


        ax.plot(rate, color='blue', label='origin')
        ax.legend(loc='best')
        ax.set_title("M Rate Series")
        # 计算自相关系数
        plot_acf(rate, use_vlines=True, lags=30)
        plot_acf(abs(rate), use_vlines=True, lags=30)
        # 自相关
        plot_acf(rate**2, use_vlines=True, lags=30)
        # 偏相关
        plot_pacf(rate, use_vlines=True, lags=30)
        acfs = stattools.acf(rate)
        # 计算偏自相关系数
        pacfs = stattools.pacf(rate)
        """
        1 通过建立均值方程或计量经济学模型，消除线性依赖
        2 对方程残差进行ARCH效应检验
        3 如果具有ARCH效应，建立波动率模型
        4 检验拟合的模型，如有必要进行改进
        """
        # 平稳性 1 看时序图 2 看自相关和偏自相关 3 单位根检验DF ADF PP检验
        # ADF检验
        adfrate = ADF(rate)
        print(adfrate.summary().as_text())
        plot_pacf(rate**2, use_vlines=True, lags=30)
        model3 = arch.arch_model(rate, mean='Constant', vol='ARCH',p=3)
        res = model3.fit()
        res.plot()
        model3 = arch.arch_model(rate, mean='Constant', vol='ARCH', p=10)
        res = model3.fit()
        res.plot()
        model3 = arch.arch_model(rate, mean='Constant', vol='GARCH')
        res = model3.fit()
        res.plot()

        close = self.data['收盘价']
        fig = plt.figure(figsize=(20, 10), dpi=80, facecolor=[199 / 255, 238 / 255, 206 / 255], edgecolor='g')
        fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.15)
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor([199 / 255, 238 / 255, 206 / 255])
        min_ticks = math.floor(len(close) / 30)
        ax.set_xlabel('time')
        ax.set_ylabel('price')
        xtick = []
        for i in range(0, len(close), min_ticks):
            xtick.append(i)
        ax.set_xticks(xtick)
        xlable = []
        for i in xtick:
            xlable.append(str(close.index[i]))
        ax.set_xticklabels(xlable, rotation=90)
        ext = math.floor(0.01 * len(close))
        ax.set_xlim((0 - ext, len(close) + ext))
        ax.plot(close, color='blue', label='close')
        ax2 = ax.twinx()
        pl2 = ax2.plot(res.conditional_volatility, color='m', linestyle='-', label='volatility')
        ax.legend(loc=1)
        ax2.legend(loc=2)
        # 画收盘线，然后画收益率小概率尾部事件发生的位置
        rate = res.conditional_volatility
        rate_right = rate[rate > rate.quantile(0.95)]
        for i in range(0, len(rate_right)):
            x = rate[rate.index == rate_right.index[i]]
            x[0] = ax.get_ylim()[0] * 1.05
            ax.plot(x, color='red', marker='*')
            x[0] = close[x.index[0]]
            ax.plot(x, color='red', marker='*')
        rate_left = rate[rate < rate.quantile(0.05)]
        for i in range(0, len(rate_left)):
            x = rate[rate.index == rate_left.index[i]]
            x[0] = ax.get_ylim()[0] * 1.03
            ax.plot(x, color='green', marker='^')
            x[0] = close[x.index[0]]
            ax.plot(x, color='green', marker='^')

        ax.set_xticks(xtick)
        ax.set_xticklabels(xlable, rotation=90)

        ax.set_title("GARCH model tail vs close price")





    def random_variable(self):
        rate = self.rate_log

        # 生成随机变量
        randomnum = np.random.choice([1, 2, 3, 4, 5], size=100, replace=True, p=[0.1, 0.2, 0.3, 0.15, 0.25])
        # 查看随机变量的分布
        pd.Series(randomnum).value_counts()
        # 概率密度
        density = stats.kde.gaussian_kde(rate)
        # 设定分割
        bins = np.arange(-0.1, 0.12, 0.005)
        # 画图，概率密度分布
        plt.plot(bins, density(bins))
        # 画图，累计概率分布
        plt.plot(bins, density(bins).cumsum())
        # 焦炭和螺纹钢的相关系数
        rate2 = self.rate2
        # 绘制散点图
        plt.scatter(rate, rate2)
        rate.corr(rate2)

        # 正态分布
        Norm = np.random.normal(size=10)
        # 求生成的正态分布的密度值probability distribution function 概率分布函数
        stats.norm.pdf(Norm)
        # 求生成的正态分布的累计密度值 cumulative distribution function 累计分布函数
        stats.norm.cdf(Norm)
        # 计算5%的分位数 percent point function 百分点函数
        stats.norm.ppf(0.05, rate.mean(), rate.std())

        # 卡方分布，画卡方分布 3 是自由度
        plt.plot(np.arange(0, 5, 0.002), stats.chi.pdf(np.arange(0, 5, 0.002), 3))
        plt.plot(np.arange(0, 5, 0.002), stats.chi.pdf(np.arange(0, 5, 0.002), 5))
        # 卡方分布的概率密度：自由度为3的，到2的累计概率分布
        stats.chi.cdf(2, 3)
        # 卡方分布的分位数计算:自由度为3，累计概率为0.85的分位数的计算
        stats.chi.ppf(0.85, 3)

        # t分布
        plt.plot(np.arange(-3, 3, 0.2), stats.t.pdf(np.arange(-3, 3, 0.2), 3))
        # t分布的累计概率分布
        stats.t.cdf(2, 3)
        # t分布的分位数的计算
        stats.t.ppf(0.93, 3)

        # F分布
        plt.plot(np.arange(0.01, 3, 0.02), stats.f.pdf(np.arange(0.01, 3, 0.02), 4, 40))

        # 二项分布
        np.random.binomial(100, 0.4, 20)
        # 二项分布的概率质量函数,100次试验，有20次朝上的概率
        stats.binom.pmf(20, 100, 0.5)
        # 求累计概率分布
        dd = stats.binom.pmf(np.arange(0, 21, 1), 100, 0.5)
        dd.sum()
        # 直接用累计概率函数
        stats.binom.cdf(20, 100, 0.5)


    def statistics_inference(self):  # 统计推断
        rate = self.rate
        # 求t分布，未知均值，未知方差的均值的95%置信区间的取值范围
        stats.t.interval(0.95, len(rate) - 1, rate.mean(), stats.sem(rate))
        # 画直方图
        plt.hist(rate)
        # 观察可知，“类似”正态分布,这里有个问题，就是样本数量的问题
        x = np.arange(-0.12, 0.12, 2 * 0.12 / len(rate))
        mean = rate.mean()
        std = rate.std()
        plt.plot(x, stats.t.pdf(x, mean, std))
        # 收益率是否均值为0,单样本t检验
        stats.ttest_1samp(rate, 0)
        # 独立样本t检验：两个服从正态分布的总体的均值是否显著差异,前提是方差相等
        rate2 = self.rate2
        stats.ttest_ind(rate, rate2)
        # 两个样本并不互相独立，使用配对样本t检验对总体的均值差异进行检验
        # 即假设这两个均值不互相独立
        stats.ttest_rel(rate, rate2)


    def anova(self):  # 方差分析，变量之间关系的定性分析方法——方差分析
        # 不同行业的收益率是否相同？
        # 焦炭的收益率会比螺纹的收益率更高吗
        # 一个因子变量是否影响某一个变量的数值
        # 两个不同水平下，反应变量如何取值，以及哪种情况取值更高
        # 准确的说，方差分析的研究对象是各个组别反应变量均值之间存在的差异，
        # 其中组别的划分是以因子变量为依据的，由于需要借助方差来观察均值是否相同，所以被称为方差分析
        test = [[0.57298, '货币金融服务'],
                [0.827567, '货币金融服务'],
                [0.336481, '房地产业'],
                [0.64, '医药制造业'],
                [0.477997, '房地产业'],
                ]
        df = pd.DataFrame(test, columns=['return', 'industry'])

        # model = ols(return - C(industry),data=df.dropna()).fit()
        # table1 = anova.anova_lm(model)
        # print(table1)
        pass


    def regression(self):  # 线性回归
        rate1 = self.rate
        rate2 = self.rate2
        model = sm.OLS(rate1, sm.add_constant(rate2)).fit()
        print(model.summary())
        model.fittedvalues  # 查看方程的拟合值
        model.resid  # 回归的残差项
        plt.scatter(model.fittedvalues, model.resid)
        plt.show()
        # 正态性，当因变量成正态分布，模型的残差应该是一个均值为0的正态分布
        # qq图
        sm.qqplot(model.resid_pearson, stats.norm, line='45')
        # 同方差性
        plt.scatter(model.fittedvalues, model.resid_pearson ** 0.5)
        pass


    def finance_basic(self):  # 金融基础理论
        rate1 = self.rate
        # 给的是日度的收益率，则按每年245个日度交易数据进行处理
        annualize = (1 + rate1).cumprod()[-1] ** (245 / len(rate1)) - 1
        # 计算ffn包中复利收益率的函数??????

        # 收益率的2阶对数收益图
        np.log(rate1 / rate1.shift(2))
        # 收益率的图
        np.log(rate1 / rate1.shift(1)).dropna().plot()
        # 累计收益率的图
        ((1 + rate1).cumprod() - 1).plot()
        # 历史模拟法计算VaR
        rate1.quantile(0.05)
        # 方差，协方差计算VaR
        stats.norm.ppf(0.05, rate1.mean(), rate1.std())
        # 期望亏空
        rate1[rate1 <= rate1.quantile(0.05)].mean()
        # 马科维茨 理论的python实现
        pass


    def time_series(self):  # 时间序列
        rate1 = self.rate
        # 计算自相关系数
        acfs = stattools.acf(rate1)
        # 计算偏自相关系数
        pacfs = stattools.pacf(rate1)
        # 绘制自相关系数图
        plot_acf(rate1, use_vlines=True, lags=30)
        # 绘制偏自相关系数图
        plot_pacf(rate1, use_vlines=True, lags=30)
        # 平稳性 1 看时序图 2 看自相关和偏自相关 3 单位根检验DF ADF PP检验
        # ADF检验
        adfrate = ADF(rate1)
        print(adfrate.summary().as_text())

        pass

def main():
    self = model_statistic()
    #self.descriptive()
    #self.series()
    self.little_propably()
    # 数据的平稳性
    # 序列的平均值不应该是时间的函数
    # 序列的方差不应该是时间的函数
    # 数据的协方差不应该是时间的函数
    # 一个平稳的时间序列是容易进行预测的，可以假设其未来与现在的统计属性是相同的或者成比例的
    # 我们用的大多数时间序列分析模型都是假设协方差平稳。
    # 对时间序列建模，分成三部分，趋势，周期和随机

    # 对数据作图
    pass


if __name__ == '__main__':
    main()