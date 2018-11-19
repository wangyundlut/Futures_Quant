# -*- coding: UTF-8 -*-
# author:@Jack.Wang
# time :2018/8/27 11:23
import xlrd
import xlwt

def mytest():
    data = xlrd.open_workbook('F:\Quant\Daily\stocklist-2018-08-26.xlsx')
    data._sheet_names
    data.sheets[0]
    data.sheet_by_index(0)
    table = data.sheet_by_name(u'60日40%跌幅')

    print(data)
    print('Done')




if __name__ == '__main__':
    mytest()