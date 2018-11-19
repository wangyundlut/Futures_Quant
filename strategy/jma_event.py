# -*- coding: UTF-8 -*-
# author:@Jack.Wang
# time :2018/8/19 11:13


import pandas as pd
import math
import scipy.io as sio

class jmavalue: # 将JMA改成事件模式，即，输入进来一个K线，驱动算一次JMAValueBuffer的值
    def __init__(self, Length, phase):
        self.jma = {}
        # 初始化
        self.jma['initFlag'] = True
        self.jma['Length'] = Length
        self.jma['phase'] = phase

        self.jma['list'] = [0 for i in range(128)]
        self.jma['ring1'] = [0 for i in range(128)]
        self.jma['ring2'] = [0 for i in range(11)]
        self.jma['buffer'] = [0 for i in range(62)]

        self.jma['limitValue'] = 63
        self.jma['startValue'] = 64

        for i in range(0, 64):
            self.jma['list'][i] = -1000000
        for i in range(64, 128):
            self.jma['list'][i] = 1000000


        if self.jma['Length'] < 1:
            self.jma['lengthParam'] = 0.00000001
        else:
            self.jma['lengthParam'] = (self.jma['Length'] - 1) / 2

        if self.jma['phase'] < -100:
            self.jma['phaseParam'] = 0.5
        elif self.jma['phase'] > 100:
            self.jma['phaseParam'] = 2.5
        else:
            self.jma['phaseParam'] = self.jma['phase'] / 101.5
        self.jma['logParam'] = math.log(math.sqrt(self.jma['lengthParam']), 10) / math.log(2, 10)
        if self.jma['logParam'] + 2 < 0:
            self.jma['logParam'] = 0
        else:
            self.jma['logParam'] = self.jma['logParam'] + 2

            self.jma['sqrtParam'] = math.sqrt(self.jma['lengthParam']) * self.jma['logParam']
        self.jma['lengthParam'] = self.jma['lengthParam'] * 0.9
        self.jma['lengthDivider'] = self.jma['lengthParam'] / (self.jma['lengthParam'] + 2)

        self.jma['loopParam'] = 0
        self.jma['cycleLimit'] = 0
        self.jma['cycleDelta'] = 0
        self.jma['loopCriteria'] = 0
        self.jma['counterA'] = 0
        self.jma['counterB'] = 0
        self.jma['lowDValue'] = 0
        self.jma['JMATempValue'] = 0

        self.jma['fC0Buffer'] = []
        self.jma['fC8Buffer'] = []
        self.jma['fA8Buffer'] = []
        self.jma['JMAValueBuffer'] = []
        self.jma['data'] = []

    def jma_calculate(self, data):
        self.jma['data'].append(data)
        if self.jma['loopParam'] < 61:
            self.jma['loopParam'] = self.jma['loopParam'] + 1
            self.jma['buffer'][self.jma['loopParam']] = data
        if self.jma['loopParam'] <= 30:
            self.jma['JMATempValue'] = 0
        if self.jma['loopParam'] > 30:
            if self.jma['initFlag']:
                self.Firsttime(data)
            for i in range(self.jma['highlimit'], -1, -1):
                # 计算sValue
                self.step1(i, data)
                self.step2()
                self.step3()
                self.step4()
                self.step5()
                if self.jma['cycleLimit'] < 128:
                    self.step6()

                self.step7()
                if self.jma['cycleLimit'] > 127:
                    self.step8()
                else:
                    self.step9()

                self.step10()
                if self.jma['cycleLimit'] > 127:
                    self.step11()
                    self.step12()
                    self.step13()

                    self.step14()

                    self.jma['JMATempValue'] = 0
                    self.jma['sqrtDivider'] = self.jma['sqrtParam'] / (self.jma['sqrtParam'] + 1)
                    if self.jma['loopCriteria'] <= 30:
                        self.step15()
                        self.jma['JMATempValue'] = data
                        if self.jma['loopCriteria'] == 30:
                            # ????
                            self.jma['fC0Buffer'].append(data)
                            self.step16()
                            fA8 = data - self.jma['buffer'][self.jma['loopParam'] - self.jma['upShift']] * (1 - self.jma['dValue']) / self.jma['rightPart'] + \
                                                       (data - self.jma['buffer'][self.jma['loopParam'] - self.jma['dnShift']]) * self.jma['dValue'] / self.jma['leftInt']
                            self.jma['fA8Buffer'].append(fA8)
                    elif self.jma['loopCriteria'] > 30:
                        self.step17()
                        self.step18()
            if self.jma['loopCriteria'] > 30:
                self.step19(data)
        self.jma['JMAValueBuffer'].append(self.jma['JMATempValue'])
        if len(self.jma['fC0Buffer']) < len(self.jma['JMAValueBuffer']):
            self.jma['fC0Buffer'].append(0)
        if len(self.jma['fC8Buffer']) < len(self.jma['JMAValueBuffer']):
            self.jma['fC8Buffer'].append(0)
        if len(self.jma['fA8Buffer']) < len(self.jma['JMAValueBuffer']):
            self.jma['fA8Buffer'].append(0)

    def Firsttime(self, data):
        self.jma['initFlag'] = False
        diffflag = 0
        for i1 in range(0, 29):
            if self.jma['buffer'][i1 + 1] != self.jma['buffer'][i1]:
                diffflag = 1

        self.jma['highlimit'] = diffflag * 30
        if self.jma['highlimit'] == 0:
            self.jma['paramB'] = data
        else:
            self.jma['paramB'] = self.jma['buffer'][1]

        self.jma['paramA'] = self.jma['paramB']
        if self.jma['highlimit'] > 29:
            self.jma['highlimit'] = 29
        else:
            self.jma['highlimit'] = 0

    def step1(self, i, data):
        if i == 0:
            self.jma['sValue'] = data
        else:
            self.jma['sValue'] = self.jma['buffer'][31 - i]

    def step2(self):
        if abs(self.jma['sValue'] - self.jma['paramA']) > abs(self.jma['sValue'] - self.jma['paramB']):
            self.jma['absValue'] = self.jma['sValue'] - self.jma['paramA']
        else:
            self.jma['absValue'] = self.jma['sValue'] - self.jma['paramB']

    def step3(self):
        self.jma['dValue'] = self.jma['absValue'] + 0.0000000001

    def step4(self):
        if self.jma['counterA'] <= 1:
            self.jma['counterA'] = 127
        else:
            self.jma['counterA'] = self.jma['counterA'] - 1

    def step5(self):
        if self.jma['counterB'] <= 1:
            self.jma['counterB'] = 10
        else:
            self.jma['counterB'] = self.jma['counterB'] - 1

    def step6(self):
        self.jma['cycleLimit'] = self.jma['cycleLimit'] + 1
        self.jma['cycleDelta'] = self.jma['cycleDelta'] + self.jma['dValue'] - self.jma['ring2'][self.jma['counterB']]
        self.jma['ring2'][self.jma['counterB']] = self.jma['dValue']

    def step7(self):
        if self.jma['cycleLimit'] > 10:
            self.jma['highDValue'] = self.jma['cycleDelta']/10.0
        else:
            self.jma['highDValue'] = self.jma['cycleDelta']/self.jma['cycleLimit']
        if self.jma['cycleLimit'] == 0:
            print('cyclielimit == 0')

    def step8(self):
        self.jma['dValue'] = self.jma['ring1'][self.jma['counterA']]
        self.jma['ring1'][self.jma['counterA']] = self.jma['highDValue']
        self.jma['s68'] = 64
        self.jma['s58'] = self.jma['s68']
        while self.jma['s68'] > 1:
            if self.jma['list'][self.jma['s58']] < self.jma['dValue']:
                self.jma['s68'] = int(self.jma['s68']/2)
                self.jma['s58'] = self.jma['s58'] + self.jma['s68']
            else:
                if self.jma['list'][self.jma['s58']] <= self.jma['dValue']:
                    self.jma['s68'] = 1
                else:
                    self.jma['s68'] = int(self.jma['s68']/2)
                    self.jma['s58'] = self.jma['s58'] - self.jma['s68']

    def step9(self):
        self.jma['ring1'][self.jma['counterA']] = self.jma['highDValue']
        if self.jma['limitValue'] + self.jma['startValue'] > 127:
            self.jma['startValue'] = self.jma['startValue'] - 1
            self.jma['s58'] = self.jma['startValue']
        else:
            self.jma['limitValue'] = self.jma['limitValue'] + 1
            self.jma['s58'] = self.jma['limitValue']

        if self.jma['limitValue'] > 96:
            self.jma['s38'] = 96
        else:
            self.jma['s38'] = self.jma['limitValue']

        if self.jma['startValue'] < 32:
            self.jma['s40'] = 32
        else:
            self.jma['s40'] = self.jma['startValue']

    def step10(self):
        self.jma['s68'] = 64
        self.jma['s60'] = self.jma['s68']
        while self.jma['s68'] > 1:
            if self.jma['list'][self.jma['s60']] >= self.jma['highDValue']:
                if self.jma['list'][self.jma['s60'] - 1] <= self.jma['highDValue']:
                    self.jma['s68'] = 1
                else:
                    self.jma['s68'] = int(self.jma['s68']/2)
                    self.jma['s60'] = self.jma['s60'] - self.jma['s68']
            else:
                self.jma['s68'] = int(self.jma['s68']/2)
                self.jma['s60'] = self.jma['s60'] + self.jma['s68']
            if self.jma['s60'] == 127 and self.jma['highDValue'] > self.jma['list'][127]:
                self.jma['s60'] = 128

    def step11(self):
        if self.jma['s58'] >= self.jma['s60']:
            if ((self.jma['s38'] + 1) > self.jma['s60']) and ((self.jma['s40'] - 1) < self.jma['s60']):
                self.jma['lowDValue'] = self.jma['lowDValue'] + self.jma['highDValue']
            elif (self.jma['s40'] > self.jma['s60']) and ((self.jma['s40'] - 1) < self.jma['s58']):
                self.jma['lowDValue'] = self.jma['lowDValue'] + self.jma['list'][self.jma['s40'] - 1]
        elif self.jma['s40'] >= self.jma['s60']:
            if ((self.jma['s38'] + 1) < self.jma['s60']) and ((self.jma['s38'] + 1) > self.jma['s58']):
                self.jma['lowDValue'] = self.jma['lowDValue'] + self.jma['list'][self.jma['s38'] + 1]
        elif (self.jma['s38'] + 2) > self.jma['s60']:
            self.jma['lowDValue'] = self.jma['lowDValue'] + self.jma['highDValue']
        elif (self.jma['s38'] + 1) < self.jma['s60'] and (self.jma['s38'] + 1) > self.jma['s58']:
            self.jma['lowDValue'] = self.jma['lowDValue'] + self.jma['list'][self.jma['s38'] + 1]

    def step12(self):
        if self.jma['s58'] > self.jma['s60']:
            if ((self.jma['s40'] - 1) < self.jma['s58']) and ((self.jma['s38'] + 1) > self.jma['s58']):
                self.jma['lowDValue'] = self.jma['lowDValue'] - self.jma['list'][self.jma['s58']]
            elif (self.jma['s38'] < self.jma['s58']) and ((self.jma['s38'] + 1) > self.jma['s60']):
                self.jma['lowDValue'] = self.jma['lowDValue'] - self.jma['list'][self.jma['s38']]
        else:
            if ((self.jma['s38'] + 1) > self.jma['s58']) and ((self.jma['s40'] - 1) < self.jma['s58']):
                self.jma['lowDValue'] = self.jma['lowDValue'] - self.jma['list'][self.jma['s58']]
            elif (self.jma['s40'] > self.jma['s58']) and (self.jma['s40'] < self.jma['s60']):
                self.jma['lowDValue'] = self.jma['lowDValue'] - self.jma['list'][self.jma['s40']]

    def step13(self):
        if self.jma['s58'] <= self.jma['s60']:
            if self.jma['s58'] >= self.jma['s60']:
                self.jma['list'][self.jma['s60']] = self.jma['highDValue']
            else:
                for j in range(self.jma['s58'] + 1, self.jma['s60']):
                    self.jma['list'][j - 1] = self.jma['list'][j]
                self.jma['list'][self.jma['s60'] - 1] = self.jma['highDValue']
        else:
            for j in range(self.jma['s58'] - 1, self.jma['s60'] - 1, -1):
                self.jma['list'][j + 1] = self.jma['list'][j]
            self.jma['list'][self.jma['s60']] = self.jma['highDValue']

    def step14(self):
        if self.jma['loopCriteria'] + 1 > 31:
            self.jma['loopCriteria'] = 31
        else:
            self.jma['loopCriteria'] = self.jma['loopCriteria'] + 1

    def step15(self):
        if self.jma['sValue'] - self.jma['paramA'] > 0:
            self.jma['paramA'] = self.jma['sValue']
        else:
            self.jma['paramA'] = self.jma['sValue'] - (self.jma['sValue'] - self.jma['paramA'])*self.jma['sqrtDivider']
        if self.jma['sValue'] - self.jma['paramB'] < 0:
            self.jma['paramB'] = self.jma['sValue']
        else:
            self.jma['paramB'] = self.jma['sValue'] - (self.jma['sValue'] - self.jma['paramB'])*self.jma['sqrtDivider']

    def step16(self):
        if math.ceil(self.jma['sqrtParam']) >= 1:
            self.jma['intPart'] = math.ceil(self.jma['sqrtParam'])
        else:
            self.jma['intPart'] = 1
        self.jma['leftInt'] = self.IntPortion(self.jma['intPart'])
        if math.floor(self.jma['sqrtParam']) >= 1:
            self.jma['intPart'] = math.floor(self.jma['sqrtParam'])
        else:
            self.jma['intPart'] = 1

        self.jma['rightPart'] = self.IntPortion(self.jma['intPart'])
        if self.jma['leftInt'] == self.jma['rightPart']:
            self.jma['dValue'] = 1
        else:
            self.jma['dValue'] = (self.jma['sqrtParam'] - self.jma['rightPart'])/\
                                 (self.jma['leftInt'] - self.jma['rightPart'])
        self.jma['upShift'] = min(self.jma['rightPart'], 29)
        self.jma['dnShift'] = min(self.jma['leftInt'], 29)

    def step17(self):
        self.jma['dValue'] = self.jma['lowDValue']/(self.jma['s38'] - self.jma['s40'] + 1)
        if 0.5 <= self.jma['logParam'] - 2:
            self.jma['powerValue'] = self.jma['logParam'] - 2
        else:
            self.jma['powerValue'] = 0.5
        # 这个地方最容易出错，经常除0
        if abs(self.jma['absValue']/self.jma['dValue']) < 0.1:
            self.jma['dValue'] = 0
        elif self.jma['logParam'] >= abs(pow(self.jma['absValue']/self.jma['dValue'], self.jma['powerValue'])):
            self.jma['dValue'] = abs(math.pow((self.jma['absValue']/self.jma['dValue']), self.jma['powerValue']))
        else:
            self.jma['dValue'] = self.jma['logParam']

        if self.jma['dValue'] < 1:
            self.jma['dValue'] = 1
        self.jma['powerValue'] = math.pow(self.jma['sqrtDivider'], math.sqrt((self.jma['dValue'])))

    def step18(self):
        if self.jma['sValue'] - self.jma['paramA'] > 0:
            self.jma['paramA'] = self.jma['sValue']
        else:
            self.jma['paramA'] = self.jma['sValue'] - (self.jma['sValue'] - self.jma['paramA'])*self.jma['powerValue']
        if self.jma['sValue'] - self.jma['paramB'] < 0:
            self.jma['paramB'] = self.jma['sValue']
        else:
            self.jma['paramB'] = self.jma['sValue'] - (self.jma['sValue'] - self.jma['paramB'])*self.jma['powerValue']

    def step19(self, data):
        self.jma['JMATempValue'] = self.jma['JMAValueBuffer'][-1]
        self.jma['powerValue'] = math.pow(self.jma['lengthDivider'], self.jma['dValue'])
        self.jma['squareValue'] = math.pow(self.jma['powerValue'], 2)
        fC0 = (1 - self.jma['powerValue']) * data + self.jma['powerValue'] * self.jma['fC0Buffer'][-1]
        self.jma['fC0Buffer'].append(fC0)
        fC8 = (data - fC0) * (1 - self.jma['lengthDivider']) + self.jma['lengthDivider'] * \
              self.jma['fC8Buffer'][-1]
        self.jma['fC8Buffer'].append(fC8)
        temp1 = (self.jma['phaseParam'] * fC8 + fC0 - self.jma['JMATempValue'])
        temp2 = (self.jma['powerValue'] * (-2.0) + self.jma['squareValue'] + 1)
        fA8 = temp1*temp2 + self.jma['squareValue']*self.jma['fA8Buffer'][-1]
        self.jma['fA8Buffer'].append(fA8)
        self.jma['JMATempValue'] = self.jma['JMATempValue'] + fA8

    def IntPortion(self, param):
        if param > 0:
            out = math.floor(param)
        elif param < 0 :
            out = math.ceil(param)
        if param == 0:
            out = 0
        return out

if __name__=='__main__':
    file_name = "F:\Quant\Data\Futures_KLine\Day\J201809.mat"
    d = sio.loadmat(file_name)
    time = d['time_str']
    data = d['data']
    time_list = []
    for t in time:
        time_list.append(t[0][0])
    time = pd.DataFrame(time_list)
    data = pd.DataFrame(data, columns=['o','h','l','c'])
    data = pd.DataFrame(data.iloc[:, 3])
    data_list = []
    for i in range(0, len(data)):
        data_list.append(data.loc[i][0])
    data = data_list
    self = jmavalue(Length=21, phase=101)
    for d in data:
        self.jma_calculate(d)

    print('Done')

