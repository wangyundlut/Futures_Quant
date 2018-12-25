#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 默认空值
EMPTY_STRING = ''
EMPTY_UNICODE = u''
EMPTY_INT = 0
EMPTY_FLOAT = 0.0

# 方向常量，买卖方向
DIRECTION_NONE = u'无方向'
DIRECTION_LONG = u'多'
DIRECTION_SHORT = u'空'
DIRECTION_UNKNOWN = u'未知'
DIRECTION_NET = u'净'
DIRECTION_SELL = u'卖出'              # IB接口
DIRECTION_COVEREDSHORT = u'备兑空'    # 证券期权

# 开平常量，offset就是抵消，补偿的意思
OFFSET_NONE = u'无开平'
OFFSET_OPEN = u'开仓'
OFFSET_CLOSE = u'平仓'
OFFSET_CLOSETODAY = u'平今'
OFFSET_CLOSEYESTERDAY = u'平昨'
OFFSET_UNKNOWN = u'未知'

# 状态常量，订单的状态，有成交，未成交，部分成交等
STATUS_NOTTRADED = u'未成交'
STATUS_PARTTRADED = u'部分成交'
STATUS_ALLTRADED = u'全部成交'
STATUS_CANCELLED = u'已撤销'
STATUS_REJECTED = u'拒单'
STATUS_UNKNOWN = u'未知'

# 合约类型常量，资产大类

PRODUCT_FUTURES = u'期货'
PRODUCT_UNKNOWN = u'未知'
PRODUCT_DIGITAL_CURRENCY = u'数字货币'
PRODUCT_OPTION = u'期权'



# 价格类型常量，这个是下单常量，下什么单，一般都是下限价单
PRICETYPE_LIMITPRICE = u'限价'
PRICETYPE_MARKETPRICE = u'市价'
PRICETYPE_FAK = u'FAK'
PRICETYPE_FOK = u'FOK'

# 交易所类型，交易所名称，股票，期货，期权，数字货币等

EXCHANGE_SSE = 'SSE'       # 上交所
EXCHANGE_SZSE = 'SZSE'     # 深交所
EXCHANGE_CFFEX = 'CFFEX'   # 中金所
EXCHANGE_SHFE = 'SHFE'     # 上期所
EXCHANGE_CZCE = 'CZCE'     # 郑商所
EXCHANGE_DCE = 'DCE'       # 大商所
EXCHANGE_SGE = 'SGE'       # 上金所
EXCHANGE_INE = 'INE'       # 国际能源交易中心
EXCHANGE_UNKNOWN = 'UNKNOWN'# 未知交易所
EXCHANGE_NONE = ''          # 空交易所
EXCHANGE_HKEX = 'HKEX'      # 港交所
EXCHANGE_HKFE = 'HKFE'      # 香港期货交易所

EXCHANGE_OKCOIN = 'OKCOIN'       # OKCOIN比特币交易所
EXCHANGE_HUOBI = 'HUOBI'         # 火币比特币交易所
EXCHANGE_LBANK = 'LBANK'         # LBANK比特币交易所
EXCHANGE_ZB = 'ZB'		 # 比特币中国比特币交易所
EXCHANGE_OKEX = 'OKEX'		 # OKEX比特币交易所
EXCHANGE_OKEXFUTURE = 'OKEXFUTURE'		 # OKEX比特币交易所-期货
EXCHANGE_BINANCE = "BINANCE"     # 币安比特币交易所
EXCHANGE_BITFINEX = "BITFINEX"   # Bitfinex比特币交易所
EXCHANGE_BITMEX = 'BITMEX'       # BitMEX比特币交易所
EXCHANGE_FCOIN = 'FCOIN'         # FCoin比特币交易所
EXCHANGE_BIGONE = 'BIGONE'       # BigOne比特币交易所
EXCHANGE_COINBASE = 'COINBASE'   # Coinbase交易所
EXCHANGE_BITHUMB = 'BITHUMB'     # Bithumb比特币交易所


# 货币类型，美元，人民币，未知货币，你拿什么东西买，可以拿BTC
CURRENCY_USD = 'USD'            # 美元
CURRENCY_CNY = 'CNY'            # 人民币
CURRENCY_HKD = 'HKD'            # 港币
CURRENCY_UNKNOWN = 'UNKNOWN'    # 未知货币
CURRENCY_NONE = ''              # 空货币
CURRENCY_BTC = 'BTC'            # 比特币

# 数据库，这里说的事日志的数据库了
LOG_DB_NAME = 'VnTrader_Log_Db'

# 期权类型
OPTION_CALL = u'看涨期权'
OPTION_PUT = u'看跌期权'


# 接口类型
GATEWAYTYPE_EQUITY = 'equity'                   # 股票、ETF、债券
GATEWAYTYPE_FUTURES = 'futures'                 # 期货、期权、贵金属
GATEWAYTYPE_INTERNATIONAL = 'international'     # 外盘
GATEWAYTYPE_BTC = 'btc'                         # 比特币
GATEWAYTYPE_DATA = 'data'                       # 数据（非交易）

# K线周期类型
INTERVAL_1M = u'1分钟'
INTERVAL_5M = u'5分钟'
INTERVAL_15M = u'15分钟'
INTERVAL_30M = u'30分钟'
INTERVAL_1H = u'1小时'
INTERVAL_4H = u'4小时'
INTERVAL_DAILY = u'日线'
INTERVAL_WEEKLY = u'周线'

# 数据库名称
SETTING_DB_NAME = 'VnTrader_Setting_Db'
TICK_DB_NAME = 'FUTURES_Tick_Db'
DAILY_DB_NAME = 'FUTURES_Daily_Db'

MINUTE_01_DB_NAME = 'FUTURES_01Min_Db'
MINUTE_05_DB_NAME = 'FUTURES_05Min_Db'
MINUTE_30_DB_NAME = 'FUTURES_30Min_Db'
MINUTE_60_DB_NAME = 'FUTURES_60Min_Db'
# 这里数据库的更正数据从新浪来的无错误的数据
# 盘中的时候，要从tick数据更新数据
# 盘后要更正数据，从新浪数据获取

# 行情记录模块事件
EVENT_DATARECORDER_LOG = 'eDataRecorderLog'     # 行情记录日志更新事件