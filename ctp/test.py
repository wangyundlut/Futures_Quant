#!/usr/bin/python
# -*- coding: UTF-8 -*-



from vnctpmd import MdApi
import time
import os
import pandas as pd
from data_get_save.PostgreSQL import PostgreSQL
import datetime
from data_get_save.futures_time import futures_time
import requests
import json


if __name__ == '__main__':
    # 测试
    result = requests.get('http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine5m?symbol=M1905')
    json_data = json.loads(result.text)
    print('Done')
    #由于是分线程的程序，所以，此时主线程必须等待分线程进行到了之后，才能加入
    # self.subscribeMarketData('cu1810')  # 登录成功了才能订阅行情
    """
    第一组：Trade：180.168.146.187:10000，Market：180.168.146.187:10010；【电信】
    第二组：Trade：180.168.146.187:10001，Market：180.168.146.187:10011；【电信】
    第三组：Trade：218.202.237.33 :10002，Market：218.202.237.33 :10012；【移动】
    交易前置：180.168.146.187:10030，行情前置：180.168.146.187:10031；【7x24】
    # 这是实盘
    # self.connect('999819992', '5172187a', '9000', 'tcp://61.140.230.188:41205')
    """






