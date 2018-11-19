# -*- coding: utf-8 -*-
"""
Created on Wed May  9 11:38:22 2018

@author: Administrator
"""
'''
BrokerID统一为：9999

第一套：

    标准CTP：

        第一组：Trade Front：180.168.146.187:10000，Market Front：180.168.146.187:10010；【电信】

        第二组：Trade Front：180.168.146.187:10001，Market Front：180.168.146.187:10011；【电信】

        第三组：Trade Front：218.202.237.33 :10002，Market Front：218.202.237.33 :10012；【移动】

        交易阶段(服务时间)：与实际生产环境保持一致

    CTPMini1：

        第一组：Trade Front：180.168.146.187:10003，Market Front：180.168.146.187:10013；【电信】

第二套：

    交易前置：180.168.146.187:10030，行情前置：180.168.146.187:10031；【7x24】

    第二套环境仅服务于CTP API开发爱好者，仅为用户提供CTP API测试需求，不提供结算等其它服务。

    新注册用户，需要等到第二个交易日才能使用第二套环境。

    账户、钱、仓跟第一套环境上一个交易日保持一致。

    交易阶段(服务时间)：交易日，16：00～次日09：00；非交易日，16：00～次日15：00。

    用户通过SimNow的账户（上一个交易日之前注册的账户都有效）接入环境，建议通过商业终端进行模拟交易的用户使用第一套环境。
    
    
///深度行情
struct CThostFtdcDepthMarketDataField
{
	///交易日
	TThostFtdcDateType	TradingDay;
	///合约代码
	TThostFtdcInstrumentIDType	InstrumentID;
	///交易所代码
	TThostFtdcExchangeIDType	ExchangeID;
	///合约在交易所的代码
	TThostFtdcExchangeInstIDType	ExchangeInstID;
	///最新价
	TThostFtdcPriceType	LastPrice;
	///上次结算价
	TThostFtdcPriceType	PreSettlementPrice;
	///昨收盘
	TThostFtdcPriceType	PreClosePrice;
	///昨持仓量
	TThostFtdcLargeVolumeType	PreOpenInterest;
	///今开盘
	TThostFtdcPriceType	OpenPrice;
	///最高价
	TThostFtdcPriceType	HighestPrice;
	///最低价
	TThostFtdcPriceType	LowestPrice;
	///数量
	TThostFtdcVolumeType	Volume;
	///成交金额
	TThostFtdcMoneyType	Turnover;
	///持仓量
	TThostFtdcLargeVolumeType	OpenInterest;
	///今收盘
	TThostFtdcPriceType	ClosePrice;
	///本次结算价
	TThostFtdcPriceType	SettlementPrice;
	///涨停板价
	TThostFtdcPriceType	UpperLimitPrice;
	///跌停板价
	TThostFtdcPriceType	LowerLimitPrice;
	///昨虚实度
	TThostFtdcRatioType	PreDelta;
	///今虚实度
	TThostFtdcRatioType	CurrDelta;
	///最后修改时间
	TThostFtdcTimeType	UpdateTime;
	///最后修改毫秒
	TThostFtdcMillisecType	UpdateMillisec;
	///申买价一
	TThostFtdcPriceType	BidPrice1;
	///申买量一
	TThostFtdcVolumeType	BidVolume1;
	///申卖价一
	TThostFtdcPriceType	AskPrice1;
	///申卖量一
	TThostFtdcVolumeType	AskVolume1;
	///申买价二
	TThostFtdcPriceType	BidPrice2;
	///申买量二
	TThostFtdcVolumeType	BidVolume2;
	///申卖价二
	TThostFtdcPriceType	AskPrice2;
	///申卖量二
	TThostFtdcVolumeType	AskVolume2;
	///申买价三
	TThostFtdcPriceType	BidPrice3;
	///申买量三
	TThostFtdcVolumeType	BidVolume3;
	///申卖价三
	TThostFtdcPriceType	AskPrice3;
	///申卖量三
	TThostFtdcVolumeType	AskVolume3;
	///申买价四
	TThostFtdcPriceType	BidPrice4;
	///申买量四
	TThostFtdcVolumeType	BidVolume4;
	///申卖价四
	TThostFtdcPriceType	AskPrice4;
	///申卖量四
	TThostFtdcVolumeType	AskVolume4;
	///申买价五
	TThostFtdcPriceType	BidPrice5;
	///申买量五
	TThostFtdcVolumeType	BidVolume5;
	///申卖价五
	TThostFtdcPriceType	AskPrice5;
	///申卖量五
	TThostFtdcVolumeType	AskVolume5;
	///当日均价
	TThostFtdcPriceType	AveragePrice;
	///业务日期
	TThostFtdcDateType	ActionDay;
};

 

///投资者持仓
struct CThostFtdcInvestorPositionField
{
	///合约代码
	TThostFtdcInstrumentIDType	InstrumentID;
	///经纪公司代码
	TThostFtdcBrokerIDType	BrokerID;
	///投资者代码
	TThostFtdcInvestorIDType	InvestorID;
	///持仓多空方向
	TThostFtdcPosiDirectionType	PosiDirection;
	///投机套保标志
	TThostFtdcHedgeFlagType	HedgeFlag;
	///持仓日期
	TThostFtdcPositionDateType	PositionDate;
	///上日持仓
	TThostFtdcVolumeType	YdPosition;
	///今日持仓
	TThostFtdcVolumeType	Position;
	///多头冻结
	TThostFtdcVolumeType	LongFrozen;
	///空头冻结
	TThostFtdcVolumeType	ShortFrozen;
	///开仓冻结金额
	TThostFtdcMoneyType	LongFrozenAmount;
	///开仓冻结金额
	TThostFtdcMoneyType	ShortFrozenAmount;
	///开仓量
	TThostFtdcVolumeType	OpenVolume;
	///平仓量
	TThostFtdcVolumeType	CloseVolume;
	///开仓金额
	TThostFtdcMoneyType	OpenAmount;
	///平仓金额
	TThostFtdcMoneyType	CloseAmount;
	///持仓成本
	TThostFtdcMoneyType	PositionCost;
	///上次占用的保证金
	TThostFtdcMoneyType	PreMargin;
	///占用的保证金
	TThostFtdcMoneyType	UseMargin;
	///冻结的保证金
	TThostFtdcMoneyType	FrozenMargin;
	///冻结的资金
	TThostFtdcMoneyType	FrozenCash;
	///冻结的手续费
	TThostFtdcMoneyType	FrozenCommission;
	///资金差额
	TThostFtdcMoneyType	CashIn;
	///手续费
	TThostFtdcMoneyType	Commission;
	///平仓盈亏
	TThostFtdcMoneyType	CloseProfit;
	///持仓盈亏
	TThostFtdcMoneyType	PositionProfit;
	///上次结算价
	TThostFtdcPriceType	PreSettlementPrice;
	///本次结算价
	TThostFtdcPriceType	SettlementPrice;
	///交易日
	TThostFtdcDateType	TradingDay;
	///结算编号
	TThostFtdcSettlementIDType	SettlementID;
	///开仓成本
	TThostFtdcMoneyType	OpenCost;
	///交易所保证金
	TThostFtdcMoneyType	ExchangeMargin;
	///组合成交形成的持仓
	TThostFtdcVolumeType	CombPosition;
	///组合多头冻结
	TThostFtdcVolumeType	CombLongFrozen;
	///组合空头冻结
	TThostFtdcVolumeType	CombShortFrozen;
	///逐日盯市平仓盈亏
	TThostFtdcMoneyType	CloseProfitByDate;
	///逐笔对冲平仓盈亏
	TThostFtdcMoneyType	CloseProfitByTrade;
	///今日持仓
	TThostFtdcVolumeType	TodayPosition;
	///保证金率
	TThostFtdcRatioType	MarginRateByMoney;
	///保证金率(按手数)
	TThostFtdcRatioType	MarginRateByVolume;
	///执行冻结
	TThostFtdcVolumeType	StrikeFrozen;
	///执行冻结金额
	TThostFtdcMoneyType	StrikeFrozenAmount;
	///放弃执行冻结
	TThostFtdcVolumeType	AbandonFrozen;
	///交易所代码
	TThostFtdcExchangeIDType	ExchangeID;
	///执行冻结的昨仓
	TThostFtdcVolumeType	YdStrikeFrozen;
};

///资金账户
struct CThostFtdcTradingAccountField
{
	///经纪公司代码
	TThostFtdcBrokerIDType	BrokerID;
	///投资者帐号
	TThostFtdcAccountIDType	AccountID;
	///上次质押金额
	TThostFtdcMoneyType	PreMortgage;
	///上次信用额度
	TThostFtdcMoneyType	PreCredit;
	///上次存款额
	TThostFtdcMoneyType	PreDeposit;
	///上次结算准备金
	TThostFtdcMoneyType	PreBalance;
	///上次占用的保证金
	TThostFtdcMoneyType	PreMargin;
	///利息基数
	TThostFtdcMoneyType	InterestBase;
	///利息收入
	TThostFtdcMoneyType	Interest;
	///入金金额
	TThostFtdcMoneyType	Deposit;
	///出金金额
	TThostFtdcMoneyType	Withdraw;
	///冻结的保证金
	TThostFtdcMoneyType	FrozenMargin;
	///冻结的资金
	TThostFtdcMoneyType	FrozenCash;
	///冻结的手续费
	TThostFtdcMoneyType	FrozenCommission;
	///当前保证金总额
	TThostFtdcMoneyType	CurrMargin;
	///资金差额
	TThostFtdcMoneyType	CashIn;
	///手续费
	TThostFtdcMoneyType	Commission;
	///平仓盈亏
	TThostFtdcMoneyType	CloseProfit;
	///持仓盈亏
	TThostFtdcMoneyType	PositionProfit;
	///期货结算准备金
	TThostFtdcMoneyType	Balance;
	///可用资金
	TThostFtdcMoneyType	Available;
	///可取资金
	TThostFtdcMoneyType	WithdrawQuota;
	///基本准备金
	TThostFtdcMoneyType	Reserve;
	///交易日
	TThostFtdcDateType	TradingDay;
	///结算编号
	TThostFtdcSettlementIDType	SettlementID;
	///信用额度
	TThostFtdcMoneyType	Credit;
	///质押金额
	TThostFtdcMoneyType	Mortgage;
	///交易所保证金
	TThostFtdcMoneyType	ExchangeMargin;
	///投资者交割保证金
	TThostFtdcMoneyType	DeliveryMargin;
	///交易所交割保证金
	TThostFtdcMoneyType	ExchangeDeliveryMargin;
	///保底期货结算准备金
	TThostFtdcMoneyType	ReserveBalance;
	///币种代码
	TThostFtdcCurrencyIDType	CurrencyID;
	///上次货币质入金额
	TThostFtdcMoneyType	PreFundMortgageIn;
	///上次货币质出金额
	TThostFtdcMoneyType	PreFundMortgageOut;
	///货币质入金额
	TThostFtdcMoneyType	FundMortgageIn;
	///货币质出金额
	TThostFtdcMoneyType	FundMortgageOut;
	///货币质押余额
	TThostFtdcMoneyType	FundMortgageAvailable;
	///可质押货币金额
	TThostFtdcMoneyType	MortgageableFund;
	///特殊产品占用保证金
	TThostFtdcMoneyType	SpecProductMargin;
	///特殊产品冻结保证金
	TThostFtdcMoneyType	SpecProductFrozenMargin;
	///特殊产品手续费
	TThostFtdcMoneyType	SpecProductCommission;
	///特殊产品冻结手续费
	TThostFtdcMoneyType	SpecProductFrozenCommission;
	///特殊产品持仓盈亏
	TThostFtdcMoneyType	SpecProductPositionProfit;
	///特殊产品平仓盈亏
	TThostFtdcMoneyType	SpecProductCloseProfit;
	///根据持仓盈亏算法计算的特殊产品持仓盈亏
	TThostFtdcMoneyType	SpecProductPositionProfitByAlg;
	///特殊产品交易所保证金
	TThostFtdcMoneyType	SpecProductExchangeMargin;
	///业务类型
	TThostFtdcBizTypeType	BizType;
};

 

///合约手续费率
struct CThostFtdcInstrumentCommissionRateField
{
	///合约代码
	TThostFtdcInstrumentIDType	InstrumentID;
	///投资者范围
	TThostFtdcInvestorRangeType	InvestorRange;
	///经纪公司代码
	TThostFtdcBrokerIDType	BrokerID;
	///投资者代码
	TThostFtdcInvestorIDType	InvestorID;
	///开仓手续费率
	TThostFtdcRatioType	OpenRatioByMoney;
	///开仓手续费
	TThostFtdcRatioType	OpenRatioByVolume;
	///平仓手续费率
	TThostFtdcRatioType	CloseRatioByMoney;
	///平仓手续费
	TThostFtdcRatioType	CloseRatioByVolume;
	///平今手续费率
	TThostFtdcRatioType	CloseTodayRatioByMoney;
	///平今手续费
	TThostFtdcRatioType	CloseTodayRatioByVolume;
	///交易所代码
	TThostFtdcExchangeIDType	ExchangeID;
	///业务类型
	TThostFtdcBizTypeType	BizType;
};

 

///合约保证金率
struct CThostFtdcInstrumentMarginRateField
{
	///合约代码
	TThostFtdcInstrumentIDType	InstrumentID;
	///投资者范围
	TThostFtdcInvestorRangeType	InvestorRange;
	///经纪公司代码
	TThostFtdcBrokerIDType	BrokerID;
	///投资者代码
	TThostFtdcInvestorIDType	InvestorID;
	///投机套保标志
	TThostFtdcHedgeFlagType	HedgeFlag;
	///多头保证金率
	TThostFtdcRatioType	LongMarginRatioByMoney;
	///多头保证金费
	TThostFtdcMoneyType	LongMarginRatioByVolume;
	///空头保证金率
	TThostFtdcRatioType	ShortMarginRatioByMoney;
	///空头保证金费
	TThostFtdcMoneyType	ShortMarginRatioByVolume;
	///是否相对交易所收取
	TThostFtdcBoolType	IsRelative;
};

 
///成交
struct CThostFtdcTradeField
{
	///经纪公司代码
	TThostFtdcBrokerIDType	BrokerID;
	///投资者代码
	TThostFtdcInvestorIDType	InvestorID;
	///合约代码
	TThostFtdcInstrumentIDType	InstrumentID;
	///报单引用
	TThostFtdcOrderRefType	OrderRef;
	///用户代码
	TThostFtdcUserIDType	UserID;
	///交易所代码
	TThostFtdcExchangeIDType	ExchangeID;
	///成交编号
	TThostFtdcTradeIDType	TradeID;
	///买卖方向
	TThostFtdcDirectionType	Direction;
	///报单编号
	TThostFtdcOrderSysIDType	OrderSysID;
	///会员代码
	TThostFtdcParticipantIDType	ParticipantID;
	///客户代码
	TThostFtdcClientIDType	ClientID;
	///交易角色
	TThostFtdcTradingRoleType	TradingRole;
	///合约在交易所的代码
	TThostFtdcExchangeInstIDType	ExchangeInstID;
	///开平标志
	TThostFtdcOffsetFlagType	OffsetFlag;
	///投机套保标志
	TThostFtdcHedgeFlagType	HedgeFlag;
	///价格
	TThostFtdcPriceType	Price;
	///数量
	TThostFtdcVolumeType	Volume;
	///成交时期
	TThostFtdcDateType	TradeDate;
	///成交时间
	TThostFtdcTimeType	TradeTime;
	///成交类型
	TThostFtdcTradeTypeType	TradeType;
	///成交价来源
	TThostFtdcPriceSourceType	PriceSource;
	///交易所交易员代码
	TThostFtdcTraderIDType	TraderID;
	///本地报单编号
	TThostFtdcOrderLocalIDType	OrderLocalID;
	///结算会员编号
	TThostFtdcParticipantIDType	ClearingPartID;
	///业务单元
	TThostFtdcBusinessUnitType	BusinessUnit;
	///序号
	TThostFtdcSequenceNoType	SequenceNo;
	///交易日
	TThostFtdcDateType	TradingDay;
	///结算编号
	TThostFtdcSettlementIDType	SettlementID;
	///经纪公司报单编号
	TThostFtdcSequenceNoType	BrokerOrderSeq;
	///成交来源
	TThostFtdcTradeSourceType	TradeSource;
};

 

 
'''