# -*- coding: utf-8 -*-

"""
从新浪获取商品期货和金融期货的数据
5分钟 15分钟 30分钟 60分钟 数据
日线数据
分别插入到不同的数据库中
"""

import requests
import json
from sina_web.constant import *

class get_data_sina(object):
    def __init__(self):
        pass
    def get_futures_min(self, xMin, instrumentID):
        if int(xMin) == 5:
            web = FUTURES_MIN_FIRST + MIN_5 + FUTURES_MIN_SECOND + instrumentID.upper()
            web_content = requests.get(web).text
            json_content = json.loads(web_content)
        elif int(xMin) == 15:
            pass
        elif int(xMin) == 30:
            web = FUTURES_MIN_FIRST + MIN_30 + FUTURES_MIN_SECOND + instrumentID.upper()
            web_content = requests.get(web).text
            json_content = json.loads(web_content)
        elif int(xMin) == 60:
            pass


def my_test():
    self = get_data_sina()
    self.get_futures_min(xMin=30, instrumentID='j1905')


if __name__ == '__main__':
    my_test()