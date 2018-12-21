#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test的时候，引入的gateway也是模块，而不是类
"""


from vnpy_change.trader.gateway import ctpGateway
from vnpy_change.trader.vtEngine import MainEngine
from vnpy_change.event.eventEngine import EventEngine
from vnpy_change.trader.vtObject import VtSubscribeReq
from vnpy_change.trader.app import dataRecorder
import time


def main():
    ee = EventEngine()
    me = MainEngine(ee)
    me.addGateway(ctpGateway)
    me.addApp(dataRecorder)
    me.dbConnect()
    me.connect('CTP')
    while True:
        try:
            print("time:{0} ,price:{1:.2f}".format(me.dataEngine.tickDict['rb1905'].time,
                                                   me.dataEngine.tickDict['rb1905'].lastPrice))
            time.sleep(3)
        except Exception:
            time.sleep(3)




if __name__ == '__main__':
    main()