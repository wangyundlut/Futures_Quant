#!/usr/bin/python
# -*- coding: utf-8 -*-


from vnpy_change.trader import constant_common
from vnpy_change.trader.gateway.ctpGateway.ctpGateway import CtpGateway

gatewayClass = CtpGateway
gatewayName = 'CTP'
gatewayDisplayName = 'CTP'
gatewayType = constant_common.GATEWAYTYPE_FUTURES
gatewayQryEnabled = True
