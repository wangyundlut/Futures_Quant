# -*- coding: utf-8 -*-
FUTURES_COMMON = 'http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFutures'

FUTURES_MIN_FIRST = FUTURES_COMMON + 'MiniKLine'
FUTURES_MIN_SECOND = 'm?symbol='
FUTURES_DAY = FUTURES_COMMON + 'DailyKLine?symbol='

FINANCE_COMMON = 'http://stock2.finance.sina.com.cn/futures/api/json.php/CffexFuturesService.getCffexFutures'
FINANCE_MIN_FIRST = FINANCE_COMMON + 'MiniKLine'
FINANCE_MIN_SECOND = 'm?symbol='
FINANCE_DAY = FINANCE_COMMON + 'DailyKLine?symbol='

MIN_5 = '5'
MIN_15 = '15'
MIN_30 = '30'
MIN_60 = '60'




