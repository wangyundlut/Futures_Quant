# -*- coding: UTF-8 -*-
# author:@Jack.Wang
# time :2018/8/23 16:38

from data_get_save.futures_info import futures_info


class futures_cal():
    def __init__(self):
        info = futures_info()

        commo_list, fina_list, futu_list = info.futures_list()
        commo_info, fina_info, futu_info = info.futures_info()
        self.commo_list = commo_list
        self.fina_list = fina_list
        self.futu_list = futu_list
        self.commo_info = commo_info
        self.fina_info = fina_info
        self.futu_info = futu_info

    def instrumentid_info(self, id):
        commodity_info = self.commo_info
        futures_info = self.fina_info

        # 获取id的info
        try:
            info = commodity_info[id.lower()]
        except KeyError:
            info = futures_info[id.lower()]
        return info

    def instrument_allcontract(self, id, date):
        commodity_info = self.commo_info
        futures_info = self.fina_info

        # 获取id的info
        try:
            domi_mon = commodity_info[id.lower()]['domi_month']
        except KeyError:
            domi_mon = futures_info[id.lower()]['domi_month']
        # 年份当年和下一年，月份
        year_1 = date[0:4]
        year_2 = str(int(date[0:4]) + 1)
        mon = date[5:7]
        # 当年的list 和下一年的list
        li = []
        for m in domi_mon:
            li.append([year_1, m])
        for m in domi_mon:
            li.append([year_2, m])
        return li

    # 输入id，date，获取当前“可能”运行的主力合约，只要运行时间在一年内的，1809，只认为它在17年10月份之后再“运行”
    def instrumentid_contract(self, id, date):
        commodity_info = self.commo_info
        futures_info = self.fina_info

        # 获取id的info
        try:
            domi_mon = commodity_info[id.lower()]['domi_month']
        except KeyError:
            domi_mon = futures_info[id.lower()]['domi_month']
        # 年份当年和下一年，月份
        year_1 = date[0:4]
        year_2 = str(int(date[0:4]) + 1)
        mon = date[5:7]
        # 当年的list 和下一年的list
        li1 = []
        li2 = []
        for m in domi_mon:
            li1.append([year_1, m])
            li2.append([year_2, m])
        i = 0
        while i < len(domi_mon):
            if domi_mon[i] > mon:
                li = li1[i:]
                for j in li2:
                    li.append(j)
                break
            # 如果主力合约循环至最后也没有大于当前月份
            elif i == len(domi_mon) - 1:
                li = li2
                break
            else:
                i += 1
        # 只要合约长度那么多的list
        li = li[0:len(domi_mon)]
        # 查看最后的合约，如果月份大于当前月份，不要这个月份的
        """
        if li[-1][1] >= mon:
            li.remove(li[-1])
        """
        return li

    def next_domi(self, id, y, m): # 输入id，年份，月份，获取下一个主力合约
        commodity_info = self.commo_info
        futures_info = self.fina_info

        try:
            domi_mon = commodity_info[id.lower()]['domi_month']
        except KeyError:
            domi_mon = futures_info[id.lower()]['domi_month']
        year_1 = y
        year_2 = str(int(y) + 1)
        li = []
        for y_ in [year_1, year_2]:
            for m_ in domi_mon:
                li.append([y_, m_])
        i = 0
        while i < len(li):
            if li[i][0] == y and li[i][1] == m:
                out_y = li[i + 1][0]
                out_m = li[i + 1][1]
                break
            else:
                i += 1

        return out_y, out_m

    def pre_domi(self, id, y, m): # 输入id，年份，月份，获取上一个主力合约
        commodity_info = self.commo_info
        futures_info = self.fina_info

        try:
            domi_mon = commodity_info[id.lower()]['domi_month']
        except KeyError:
            domi_mon = futures_info[id.lower()]['domi_month']
        year_1 = str(int(y) - 1)
        year_2 = y
        li = []
        for y_ in [year_1, year_2]:
            for m_ in domi_mon:
                li.append([y_, m_])
        i = 0
        while i < len(li):
            if li[i][0] == y and li[i][1] == m:
                out_y = li[i - 1][0]
                out_m = li[i - 1][1]
                break
            else:
                i += 1
        return out_y, out_m

    # 用于ctp方法更新数据的方法date='2018-02-02'，所有品种不适合，对网络造成较大压力
    def ctp_list(self, date):
        commodity_list = self.commo_list
        commo_list = []
        for id in commodity_list:
            id = id.lower()
            codes = self.instrumentid_contract(id, date)  # 解决codes
            for tempt in codes:
                code = id + tempt[0][2:4] + tempt[1]
                commo_list.append(code)
        return commo_list




if __name__ == '__main__':
    self = futures_cal()
    info = self.instrumentid_info('rb')
    li = self.instrumentid_contract('cu', '2018-08-21')
    y, m = self.next_domi('cu', '2018', '01')
    y, m = self.pre_domi('cu', '2018', '01')
    self.ctp_list('2018-09-03')