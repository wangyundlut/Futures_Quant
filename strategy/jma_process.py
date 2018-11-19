# -*- coding: UTF-8 -*-
# author:@Jack.Wang
# time :2018/8/19 11:13

import numpy as np
import pandas as pd
import math
import scipy.io as sio
import datetime

class jmavalue:
    def __init__(self):
        self.initFlag = True

    def jma_calculate(self, time, data ,Length ,phase):
        self.time = time
        self.data = data
        self.Length = Length
        self.phase = phase
        print('正在计算JMAValue，请稍等......')
        data = self.data
        lis = pd.DataFrame(np.zeros([128, 1]))
        ring1 = pd.DataFrame(np.zeros([128, 1]))
        ring2 = pd.DataFrame(np.zeros([11, 1]))
        buffer = pd.DataFrame(np.zeros([62, 1]))

        limitValue = 63
        startValue = 64

        lis.iloc[0:64,:] = -1000000
        lis.iloc[64:128,:] = 1000000

        if self.Length < 1:
            lengthParam = 0.00000001
        else:
            lengthParam = (self.Length - 1)/2

        if self.phase < -100:
            phaseParam = 0.5
        elif self.phase > 100:
            phaseParam = 2.5
        else:
            phaseParam = self.phase/101.5
        logParam = math.log(math.sqrt(lengthParam),10)/math.log(2,10)
        if logParam + 2 < 0:
            logParam = 0
        else:
            logParam = logParam + 2

        sqrtParam = math.sqrt(lengthParam)*logParam
        lengthParam = lengthParam*0.9
        lengthDivider = lengthParam/(lengthParam + 2)

        nr = self.time.size

        JMAValueBuffer = pd.DataFrame(np.zeros([nr, 1]))
        fC0Buffer = pd.DataFrame(np.zeros([nr, 1]))
        fC8Buffer = pd.DataFrame(np.zeros([nr, 1]))
        fA8Buffer = pd.DataFrame(np.zeros([nr, 1]))

        loopParam = 0
        cycleLimit = 0
        cycleDelta = 0
        loopCriteria = 0
        counterA = 0
        counterB = 0
        lowDValue = 0

        for shift in range(0, nr):
            print(str(datetime.datetime.now()) + ' '+str(shift) + ' in ' + str(nr))
            series = data.iloc[shift, 0]
            if loopParam < 61:
                loopParam += 1
                buffer.iloc[loopParam, 0] = series
            if loopParam <= 30:
                JMATempValue = 0
            if loopParam > 30:
                if self.initFlag:
                    highlimit, paramB, paramA = self.Firsttime(buffer, series)
                for i in range(highlimit, -1, -1):
                    # 计算sValue 1
                    sValue = self.s1(buffer, i, series)
                    # 计算absValue 1
                    absValue = self.s2(sValue, paramA, paramB)
                    # 计算dValue 1
                    dValue = self.s3(absValue)
                    # 计算counterA 1
                    counterA = self.s4(counterA)
                    # 计算counterB 1
                    counterB = self.s5(counterB)
                    # 更新cycleDelta ring2
                    if cycleLimit < 128:
                        cycleLimit, cycleDelta, ring2 = self.s6(cycleLimit, cycleDelta, dValue, ring2, counterB)
                    # highDValue 1
                    highDValue = self.s7(cycleDelta, cycleLimit)
                    if cycleLimit > 127:
                        dValue, ring1, s68, s58 = self.s8(ring1, counterA, highDValue, lis)
                    else:
                        ring1, startValue, limitValue, s58, s38, s40 = self.s9(ring1, counterA, highDValue, limitValue, startValue)
                    # s68 s60 1
                    s68, s60 = self.s10(lis, highDValue)
                    if cycleLimit > 127:
                        lowDValue = self.s11(s58, s60, s40, s38, lowDValue, highDValue, lis)
                        lowDValue = self.s12(s58, s60, s40, s38, lowDValue, lis)
                        lis = self.s13(s58, s60, lis, highDValue)
                        """
                        if cycleLimit <= 127
                            lowDValue = 0
                            for j in range(s40,s38 + 1):
                                lowDValue = lowDValue + lis.iloc[j,0]
                        """
                        loopCriteria = self.s14(loopCriteria)
                        JMATempValue = 0
                        sqrtDivider = sqrtParam/(sqrtParam + 1)
                        if loopCriteria <= 30:
                            paramA, paramB = self.s15(sValue, paramA, paramB, sqrtDivider)
                            JMATempValue = series
                            if loopCriteria == 30:
                                # ????
                                fC0Buffer.iloc[shift, 0] = series
                                leftInt, rightPart, dValue, upShift, dnShift = self.s16(sqrtParam)
                                fA8Buffer.iloc[shift, 0] = series - buffer.iloc[loopParam - upShift, 0]*(1 - dValue) / rightPart + \
                                    (series - buffer.iloc[loopParam - dnShift, 0]) * dValue / leftInt
                        elif loopCriteria > 30:
                            dValue, powerValue = self.s17(lowDValue, s38, s40, logParam, absValue, sqrtDivider)
                            paramA, paramB = self.s18(sValue, paramA, paramB, powerValue)
                if loopCriteria > 30:
                    JMATempValue = self.s19(fC0Buffer,fA8Buffer,fC8Buffer,JMAValueBuffer,shift,lengthDivider, dValue, series,phaseParam)
            JMAValueBuffer.iloc[shift, 0] = JMATempValue
            if nr % 1000 == 0:
                print(str(nr/1000) + ' in ', str(nr))
        print('JMAValue计算完毕！！！')
        return JMAValueBuffer

    def Firsttime(self, buffer, c):
        self.initFlag = False
        diffflag = 0
        for i1 in range(0, 29):
            if buffer.iloc[i1 + 1, 0] != buffer.iloc[i1, 0]:
                diffflag = 1
        highlimit = diffflag * 30
        if highlimit == 0:
            paramB = c
        else:
            paramB = buffer.iloc[1]
        paramA = paramB
        if highlimit > 29:
            highlimit = 29
        else:
            highlimit = 0
        paramA = paramA[0]
        paramB = paramB[0]
        return highlimit, paramB, paramA
    def s1(self, buffer, i, c):
        if i == 0:
            sValue = c
        else:
            sValue = buffer.iloc[31 - i, 0]
        return sValue
    def s2(self, sValue, paramA, paramB):
        if abs(sValue - paramA) > abs(sValue - paramB):
            absValue = sValue - paramA
        else:
            absValue = sValue - paramB
        return absValue
    def s3(self, absValue):
        dValue = absValue + 0.0000000001
        return dValue
    def s4(self, counterA):
        if counterA <= 1:
            counterA = 127
        else:
            counterA = counterA - 1
        return counterA
    def s5(self, counterB):
        if counterB <= 1:
            counterB = 10
        else:
            counterB = counterB - 1
        return counterB
    def s6(self, cycleLimit, cycleDelta, dValue, ring2, counterB):
        cycleLimit = cycleLimit + 1
        cycleDelta = cycleDelta + dValue - ring2.iloc[counterB, 0]
        ring2.iloc[counterB, 0] = dValue
        return cycleLimit, cycleDelta, ring2
    def s7(self, cycleDelta, cycleLimit):
        if cycleLimit > 10:
            highDValue = cycleDelta/10.0
        else:
            highDValue = cycleDelta/cycleLimit
        return highDValue
    def s8(self,ring1, counterA, highDValue, lis):
        dValue = ring1.iloc[counterA, 0]
        ring1.iloc[counterA, 0] = highDValue
        s68 = 64
        s58 = s68
        while s68 > 1:
            if lis.iloc[s58, 0] < dValue:
                s68 = int(s68/2)
                s58 = s58 + s68
            else:
                if lis.iloc[s58, 0] <= dValue:
                    s68 = 1
                else:
                    s68 = int(s68/2)
                    s58 = s58 - s68
        return dValue, ring1, s68, s58
    def s9(self, ring1, counterA, highDValue, limitValue, startValue):
        ring1.iloc[counterA, 0] = highDValue
        if limitValue + startValue > 127:
            startValue = startValue - 1
            s58 = startValue
        else:
            limitValue = limitValue + 1
            s58 = limitValue

        if limitValue > 96:
            s38 = 96
        else:
            s38 = limitValue

        if startValue < 32:
            s40 = 32
        else:
            s40 = startValue

        return ring1, startValue, limitValue, s58, s38, s40
    def s10(self, lis, highDValue):
        s68 = 64
        s60 = s68
        while s68 > 1:
            if lis.iloc[s60, 0] >= highDValue:
                if lis.iloc[s60 - 1, 0] <= highDValue:
                    s68 = 1
                else:
                    s68 = int(s68/2)
                    s60 = s60 - s68
            else:
                s68 = int(s68/2)
                s60 = s60 + s68
            if s60 == 127 and highDValue > lis.iloc[127, 0]:
                s60 = 128
        return s68, s60
    def s11(self, s58, s60, s40, s38, lowDValue, highDValue, lis):
        if s58 >= s60:
            if ((s38 + 1) > s60) and ((s40 - 1) < s60):
                lowDValue = lowDValue + highDValue
            elif (s40 > s60) and ((s40 - 1) < s58):
                lowDValue = lowDValue + lis.iloc[s40 - 1, 0]
        elif s40 >= s60:
            if ((s38 + 1) < s60) and ((s38 + 1) > s58):
                lowDValue = lowDValue + lis.iloc[s38 + 1, 0]
        elif (s38 + 2) > s60:
            lowDValue = lowDValue + highDValue
        elif (s38 + 1) < s60 and (s38 + 1) > s58:
            lowDValue = lowDValue +lis.iloc[s38 + 1,0]
        return lowDValue
    def s12(self, s58, s60, s40, s38, lowDValue, lis):
        if s58 > s60:
            if ((s40 - 1) < s58) and ((s38 + 1) > s58):
                lowDValue = lowDValue - lis.iloc[s58, 0]
            elif (s38 < s58) and ((s38 + 1) > s60):
                lowDValue = lowDValue - lis.iloc[s38, 0]
        else:
            if ((s38 + 1) > s58) and ((s40 - 1) < s58):
                lowDValue = lowDValue - lis.iloc[s58, 0]
            elif (s40 > s58) and (s40 < s60):
                lowDValue = lowDValue - lis.iloc[s40, 0]
        return lowDValue
    def s13(self, s58, s60, lis, highDValue):
        if s58 <= s60:
            if s58 >= s60:
                lis.iloc[s60, 0] = highDValue
            else:
                for j in range(s58 + 1, s60):
                    lis.iloc[j - 1, 0] = lis.iloc[j, 0]
                lis.iloc[s60 - 1, 0] = highDValue
        else:
            for j in range(s58 - 1, s60 + 1, -1):
                lis.iloc[j + 1, 0] = lis.iloc[j, 0]
            lis.iloc[s60, 0] = highDValue
        return lis
    def s14(self, loopCriteria):
        if loopCriteria + 1 > 31:
            loopCriteria = 31
        else:
            loopCriteria = loopCriteria + 1
        return loopCriteria
    def s15(self,sValue, paramA, paramB,sqrtDivider):
        if sValue - paramA > 0:
            paramA = sValue
        else:
            paramA = sValue - (sValue - paramA)*sqrtDivider
        if sValue - paramB < 0:
            paramB = sValue
        else:
            paramB = sValue - (sValue - paramB)*sqrtDivider
        return paramA, paramB
    def s16(self, sqrtParam):
        if math.ceil(sqrtParam) >= 1:
            intPart = math.ceil(sqrtParam)
        else:
            intPart = 1
        leftInt = self.IntPortion(intPart)
        if math.floor(sqrtParam) >= 1:
            intPart = math.floor(sqrtParam)
        else:
            intPart = 1
        rightPart = self.IntPortion(intPart)
        if leftInt == rightPart:
            dValue = 1
        else:
            dValue = (sqrtParam - rightPart)/(leftInt - rightPart)
        upShift = min(rightPart, 29)
        dnShift = min(leftInt, 29)
        return leftInt, rightPart, dValue, upShift, dnShift
    def s17(self, lowDValue, s38, s40, logParam, absValue, sqrtDivider):
        dValue = lowDValue/(s38 - s40 + 1)
        if 0.5 <= logParam - 2:
            powerValue = logParam - 2
        else:
            powerValue = 0.5
        if abs(absValue/dValue) < 0.1:
            dValue = 0
        elif logParam >= abs(pow(absValue/dValue, powerValue)):
            dValue = abs(math.pow((absValue/dValue), powerValue))
        else:
            dValue = logParam
        if dValue < 1:
            dValue = 1
        powerValue = math.pow(sqrtDivider, math.sqrt((dValue)))
        return dValue, powerValue
    def s18(self, sValue, paramA, paramB, powerValue):
        if sValue - paramA > 0:
            paramA = sValue
        else:
            paramA = sValue - (sValue - paramA)*powerValue
        if sValue - paramB < 0:
            paramB = sValue
        else:
            paramB = sValue - (sValue - paramB)*powerValue
        return paramA, paramB
    def s19(self,fC0Buffer,fA8Buffer,fC8Buffer,JMAValueBuffer,shift,lengthDivider, dValue, c,phaseParam):
        JMATempValue = JMAValueBuffer.iloc[shift - 1, 0]
        powerValue = math.pow(lengthDivider, dValue)
        squareValue = math.pow(powerValue, 2)
        fC0Buffer.iloc[shift, 0] = (1 - powerValue) * c + powerValue * fC0Buffer.iloc[shift - 1, 0]
        fC8Buffer.iloc[shift, 0] = (c - fC0Buffer.iloc[shift, 0]) * (1 - lengthDivider) + lengthDivider * \
                                        fC8Buffer.iloc[shift - 1, 0]
        temp1 = (phaseParam * fC8Buffer.iloc[shift, 0] + fC0Buffer.iloc[shift, 0] - JMATempValue)
        temp2 = (powerValue * (-2.0) + squareValue + 1)
        fA8Buffer.iloc[shift, 0] = temp1*temp2 + squareValue*fA8Buffer.iloc[shift - 1, 0]

        JMATempValue = JMATempValue + fA8Buffer.iloc[shift, 0]
        return JMATempValue

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


    self = jmavalue(time,data)
    jma = self.jma_calculate
    print(jma)

